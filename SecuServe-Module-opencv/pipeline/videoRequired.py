"""
This class is for the required opencv
parts 
State machine -> Discreet Finite States of of operations and clear transitions of states, seperation of states, trigger signals

TODO: work on getting the total of reconized and unreconized peole there are in the group
TODO: NEED TO REMOVE ANY FOLDER ROM THE TRANING DIR AFTER MODEL BEEN TRAINED
TODO: Check to see if any Users were added to the database so then we can see if the model needs retrained or not


TODO: Need to add model only being trained on adding or removeing of user from database 

TODO: Need to check too see if running on a jetson nano or dev pc so i can run pipeline on dev pc without crassing 

"""


from enum import Enum
from os import stat
from pickle import TRUE
import cv2
from numpy.core.records import recarray
from numpy.lib import utils

# from Jetson.GPIO.gpio import UNKNOWN

import time
import gc
import sys
import os
import face_recognition
import wget
from zmq import asyncio
from zmq.sugar import poll


from util import const
from pathlib import Path
from datetime import date, datetime
from util.faceDataStruture import UserData
from util import database as mydb
from os.path import exists
from util import consoleLog

import pipeline.pipelineStates as pipelineStates
import pipeline.knnClasifiyer as knnClasifiyer
import pipeline.videoThread as videoThread
import pipeline.userStats as userStats

import pipeline.userStats as userstat
import util.configcreator as configCreator
from multiprocessing import Process

class Status:
    # enums for the user status
    ADMIN = 0
    USER = 1
    UNWANTED = 2
    UNKNOWN = 3
    NotSuppostToBeHere = 4


class RequiredCode(object):

    i = 0

    # these are vars for storing the num faces that are seen
    Total = 0
    Reconized = 0
    Unreconized = 0

    liveness = True

    statusmsg = []
    topic = ""

    poller = None 
    receiver = None 

    # this allows me to set up pipe line easyerly  but for the cv module
    def setupPipeline(self, sender,recv,poller):
        const.watchdog = 0
    
        consoleLog.PipeLine_init("Starting up Opencv PipeLine.....")
        pipeline_start_setup = datetime.now()
        self.sendProgramStatus(
            sender,
            "SETUP_PIPELINE",
            "Starting to run pipleline",
            datetime.now() - pipeline_start_setup,
        )

        gc.enable()

        consoleLog.Debug("Dev Config" + " " + str(const.PATH))
        consoleLog.Debug("Release Config" + " " + str(const.CONFIG))

        # * Creates the file nesissary for the stuff
        if not os.path.exists(const.rootDirPath):
            consoleLog.Warning("creating Dirs")
            self.makefiledirs()
            consoleLog.PipeLine_Ok("Created Folder Structure....")

        # * creates the Relese Config
        if not exists(const.CONFIG):
            consoleLog.Warning("Creating Release config file...")
            configCreator.Config.createDefaultConfig(configCreator.Config)
            consoleLog.PipeLine_Ok("Created Release Config....")

        # prints Config of program, the opencv build info and if opencv is optimized
        consoleLog.Debug("is opencv optimized" + " " + str(cv2.useOptimized()))

        # Database connection handing
        consoleLog.Debug("Connecting to the Database Faces")
        consoleLog.PipeLine_Data(mydb.getFaces())
        consoleLog.Debug("connected to database Faces")

        # Updates Data in the Usable data list uwu
        consoleLog.Debug("Updating User list Data...")
        self.UserDataList()
        consoleLog.PipeLine_Ok("Updated User data.....")

        consoleLog.Warning("Setting up cv")

        # Downlaods all the Faces
        self.downloadUserFaces(const.imagePathusers)

        consoleLog.info("Downloading images one more time~")
        self.downloadUserFaces(const.imagePathusers)

        consoleLog.PipeLine_Ok(
            "STAGE COMPLETE" + str(datetime.now() - pipeline_start_setup)
        )
        # updates stats message
        self.sendProgramStatus(
            sender,
            "SETUP_PIPELINE",
            "finishes setup pipeline to run",
            datetime.now() - pipeline_start_setup,
        )
       
        return

    # This trains the face model for the  pipeline
    def trainPipeLine(self, sender):

        pipeline_train_knn = datetime.now()
        # updates stats message
        self.sendProgramStatus(
            sender,
            "TRAIN_MODEL",
            "starting  to train model",
            datetime.now() - pipeline_train_knn,
        )

        consoleLog.Warning("Training Model Going to take a while UwU..... ")

        knnClasifiyer.train(
            train_dir=const.imagePathusers,
            model_save_path=const.Modelpath,
            n_neighbors=2,
        )

        consoleLog.PipeLine_Ok(
            "Done Train Knn pipeline timer" + str(datetime.now() - pipeline_train_knn)
        )
        consoleLog.Warning("Done Training Model.....")
        self.sendProgramStatus(
            sender,
            "STAGE_COMPLETE",
            "done training model",
            datetime.now() - pipeline_train_knn,
        )
        return

    # * this is were rhe bulk of the vision pipline is ran and created
    def reconitionPipeline(self, sender,receiver,poller,imagesocket):
     
        
        self.sendProgramStatus(
            sender, "SETUP_PIPELINE", "Starting Face rec", datetime.now()
        )
        # cleans mess as we keep prosessing
        gc.collect()

        #TODO: MAKE MUTLI CAMERA SETUP WORK WITH IT
        # Camera Stream gst setup
        gst_str = str(
            const.opencvconfig["Stream_intro"]
            + const.opencvconfig["Stream_ip"]
            + ":"
            + const.opencvconfig["Stream_port"]
        )

        consoleLog.Warning("Looking for Faces...")

        consoleLog.PipeLine_Data("User list size is  " + " " + str(len(const.userList)))

        process_this_frame = 5

        pipeline_video_prossesing = datetime.now()

        cap = videoThread.ThreadingClass(gst_str)

        pipe = pipelineStates.PipeLine()

        status = const.status

        while True:
           
                    
            process_this_frame = process_this_frame + 1

            if const.watchdog == 10:
                print("WATCHDOG OVERRAIN")
                self.sendProgramStatus(
                    sender, "ERROR", "WATCHDOG OVERRRAN", datetime.now()
                )
                break

            self.faceIdentify(
                process_this_frame=process_this_frame,
                cap=cap,
                sender=sender,
                pipe=pipe,
                status=status,
              
                imagesocket=imagesocket,
                recv=receiver,
                poller = poller
                
            )

  
    # returns ammount of seenfaces
    
    def getAmmountOfFaces(self, image):
        return len(
            face_recognition.face_locations(
                image, model="cnn", number_of_times_to_upsample=0
            )
        )

    # Makes startup dirs

    def makefiledirs(self):
        consoleLog.Warning("Creating Folder Dirs")
        # sets up base file structure
        Path(const.rootDirPath).mkdir(parents=True, exist_ok=True)
        Path(const.imagePath).mkdir(parents=True, exist_ok=True)
        Path(const.configPath).mkdir(parents=True, exist_ok=True)
        Path(const.plateImagePath).mkdir(parents=True, exist_ok=True)
        Path(const.imagePathusers).mkdir(parents=True, exist_ok=True)

        # the captured images sorted by status path
        Path(const.adminPath).mkdir(parents=True, exist_ok=True)
        Path(const.usrPath).mkdir(parents=True, exist_ok=True)
        Path(const.unknownPath).mkdir(parents=True, exist_ok=True)
        Path(const.unwantedPath).mkdir(parents=True, exist_ok=True)

        consoleLog.Warning("Made Folder Dirs")

    def covertDictUserData(self, i):
        user = const.userList[i][UserData()]
        print(user)

    #!Encodes all the Nessiscary User info into Json String so it can be easly moved arround

    def UserDataList(self):
        i = 0

        while True:
            # example Json string  [{"uuid":"Tesla", "name":2, "status":"New York",image:none, url:}]

            # this is Where the Data gets Wrapped into am DataList with uuid First key

            #TODO: change to using api server
            userinfo = UserData(
                mydb.getName(mydb.getUsers(), i),
                mydb.getStatus(mydb.getUsers(),i),
                mydb.getImageName(mydb.getFaces(),i),
                mydb.getImageUrl(mydb.getFaces(),i),
                mydb.getPhoneNum(mydb.getUsers(),i ),
            )
            local_data = {mydb.getUserUUID(mydb.getUsers()): userinfo.__repr__()}

            const.userList.append(local_data)

            i += 1

            # Checks to see if i == the database amount hehe
            if i == mydb.getAmountOfEntrys():
                return

    # saves downloaded Image

    def downloadFacesAndProssesThem(self, data, filepath):
        # pulls right info from data
        filename = str(data[2])
        url = str(data[3])
        print(url)

        Path(filepath + "/").mkdir(parents=True, exist_ok=True)

        if not os.path.exists(filepath + filename):
            wget.download(url, str(filepath))

    # *Fully Downloades USer Images
    def downloadUserFaces(self, imagePath):

        index = 0

        # gets users names statuses face iamges and the urls from the tuples
        while True:
            userinfo = const.userList[index][mydb.getUserUUID(mydb.getFaces(), index)]

            print(const.userList[index][mydb.getUserUUID(mydb.getFaces(), index)])

            self.downloadFacesAndProssesThem(
                const.userList[index][mydb.getUserUUID(mydb.getFaces(), index)],
                imagePath + str(mydb.getUserUUID(mydb.getFaces(), index)),
            )
            consoleLog.PipeLine_Data(
                "downloaded"
                + " "
                + str(index + 1)
                + " out of "
                + str(mydb.getAmountOfEntrys())
                + "\n"
            )

            index += 1

            if index == mydb.getAmountOfEntrys():
                consoleLog.Warning("Done Downloading Images UWU....")
                return

                # Add names of the ecodings to thw end of list

    # Sends Program Status to Socket
    def sendProgramStatus(self, sender, status, pipelinePos, currenttime):
        consoleLog.Debug("sending Program status to zmq socket")
        sender.send_string("PIPELINE")
        sender.send_json(
            {
                "status": str(status),
                "pipelinePos": str(pipelinePos),
                "time": str(currenttime),
            }
        )
        time.sleep(0.5)
        consoleLog.PipeLine_Ok("Sent Program status to zmq socket")

    # Sends Face count to the web server to create database entryies
    def sendFaceCount(self, sender, total, unknown, reconized, currenttime):
        consoleLog.Debug("sending Face count to zmq")
        sender.send_string("FACECOUNT")
        sender.send_json(
            {
                "total": int(total),
                "unknown": int(unknown),
                "reconized": str(reconized),
                "time": str(currenttime),
            }
        )
        time.sleep(0.5)
        consoleLog.PipeLine_Ok("sent Face Count to zmq socket")

    # Sends Seen Users Info to Socket
    def sendUserInfoToSocket(
        self, sender, status, user, image, currenttime, phonenumber
    ):
        consoleLog.Debug("sending User indo to zmq")
        sender.send_string("USERS")
        sender.send_json(
            {
                "usr": str(user),
                "status": str(status),
                "image": str(image),
                "phone": str(phonenumber),
                "Accuracy": str(const.facepredict),
                "time": str(currenttime),
            }
        )
        time.sleep(0.5)
        consoleLog.PipeLine_Ok("sent User info to zmq socket")

    # * this is where the pipeline displays that the user is Unknown
    def StatusUnknown(
        self,
        sender,
        name,
        phone,
        frame,
        left,
        right,
        bottom,
        top,
        face_processing_pipeline_timer,
        process_this_frame,
    ):
        userstat.UserStats.userUnknown(
            self=userstat.UserStats,
            opencvconfig=const.opencvconfig,
            name=name,
            frame=frame,
            font=const.font,
            imagename=datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%f"),
            imagepath=const.imagePath,
            left=left,
            right=right,
            bottom=bottom,
            top=top,
            framenum=process_this_frame,
            recperesntage=const.facepredict,
        )
        ("unknowns Here UwU!")
        self.sendUserInfoToSocket(
            sender=sender,
            status="Unknown`",
            user=name,
            image=const.unknown_pic_url,
            currenttime=datetime.now(),
            phonenumber=phone,
        )
        consoleLog.PipeLine_Ok(
            "stop face prossesing timer unknown"
            + str(datetime.now() - face_processing_pipeline_timer)
        )

        self.sendFaceCount(
            sender, self.Total, self.Unreconized, self.Reconized, datetime.now()
        )

    def StatusCutie(
        self,
        sender,
        name,
        phone,
        frame,
        left,
        right,
        bottom,
        top,
        face_processing_pipeline_timer,
    ):
        userstat.UserStats.userGroup(
            self=userstat.UserStats,
            opencvconfig=const.opencvconfig,
            name=name,
            frame=frame,
            font=const.font,
            imagename=datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%f"),
            imagepath=const.imagePath,
            left=left,
            right=right,
            bottom=bottom,
            top=top,
            recperesntage=const.facepredict,
        )
        ("unknowns Here UwU!")
        self.sendUserInfoToSocket(
            sender=sender,
            status="Cutie`",
            user=name,
            image=const.unknown_pic_url,
            currenttime=datetime.now(),
            phonenumber=phone,
        )
        consoleLog.PipeLine_Ok(
            "stop face prossesing timer unknown"
            + str(datetime.now() - face_processing_pipeline_timer)
        )

        self.sendFaceCount(
            sender, self.Total, self.Unreconized, self.Reconized, datetime.now()
        )

    # * this is where the pipeline displays that the user reconized and classifiyed as admin
    def StatusAdmin(
        self,
        sender,
        status,
        usrname,
        phone,
        frame,
        left,
        right,
        bottom,
        top,
        face_processing_pipeline_timer,
    ):
        self.sendUserInfoToSocket(
            sender=sender,
            status=status,
            user=usrname,
            image=const.admin_pic_url,
            currenttime=datetime.now(),
            phonenumber=phone,
        )
        # logging.info("got an Admin The name is"+str(usrname))
        userstat.UserStats.userAdmin(
            self=userstat.UserStats,
            status="Admin",
            name=str(usrname),
            frame=frame,
            font=const.font,
            imagename=datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%f"),
            imagepath=const.imagePath,
            left=left,
            right=right,
            bottom=bottom,
            top=top,
            recperesntage=const.facepredict,
        )
        consoleLog.PipeLine_Ok(
            const.StopingMess
            + "admin"
            + str(datetime.now() - face_processing_pipeline_timer)
        )

    # * this is where the pipeline displays that the user reconized and classifiyed as User
    def StatusUser(
        self,
        sender,
        status,
        usrname,
        phone,
        frame,
        left,
        right,
        bottom,
        top,
        face_processing_pipeline_timer,
    ):
        self.sendUserInfoToSocket(
            sender=sender,
            status=status,
            user=usrname,
            image=const.user_pic_url,
            currenttime=datetime.now(),
            phonenumber=phone,
        )
        consoleLog.info("got an User Human The name is" + str(usrname))
        userstat.UserStats.userUser(
            self=userstat.UserStats,
            status="User",
            name=usrname,
            frame=frame,
            font=const.font,
            imagename=datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%f"),
            imagepath=const.imagePath,
            left=left,
            right=right,
            bottom=bottom,
            top=top,
            recperesntage=const.facepredict,
        )
        consoleLog.Warning(
            "eeeep there is an User They Might be evil so um let them in"
            + "  `"
            + "There Name is:"
            + str(usrname)
        )
        consoleLog.PipeLine_Ok(
            const.StopingMess
            + "user"
            + str(datetime.now() - face_processing_pipeline_timer)
        )

    # * R # * this is where the pipeline displays that the user reconized and classifiyed as Unwanted

    def StatusUnwanted(
        self,
        sender,
        status,
        usrname,
        phone,
        frame,
        left,
        right,
        bottom,
        top,
        face_processing_pipeline_timer,
    ):
        self.sendUserInfoToSocket(
            sender=sender,
            status=status,
            user=usrname,
            image=const.unwanted_pic_url,
            currenttime=datetime.now(),
            phonenumber=phone,
        )
        userstat.UserStats.userUnwanted(
            self=userstat.UserStats,
            status="Unwanted",
            name=usrname,
            frame=frame,
            font=const.font,
            imagename=datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%f"),
            imagepath=const.imagePath,
            left=left,
            right=right,
            bottom=bottom,
            top=top,
            recperesntage=const.facepredict,
        )

        consoleLog.PipeLine_Ok(
            const.StopingMess
            + "unwanted"
            + str(datetime.now() - face_processing_pipeline_timer)
        )

    # * this is the main part of face rec pipeline

    def faceIdentify(self, process_this_frame, cap, sender, pipe, status,imagesocket,recv,poller):

        if process_this_frame % 10 == 0:
            # cap.read()
            frame = cap.read()

            img = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

            predictions = knnClasifiyer.predict(
                img,
                knn_clf=knnClasifiyer.loadTrainedModel(
                    knn_clf=None, model_path=const.Modelpath
                ),
                distance_threshold=const.faceTolorace,
            )
            
            #* this allows me to convert frames caputred to the network allowing me to send them to other modules 
            #TODO: get image socket to acutally send images over the network 
            ret_code, jpg_buffer = cv2.imencode(
                ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 98])

            """
                This Section is Dedicated to dealing with user Seperatation via the User Stats data tag
            """
            evts = dict(poller.poll(timeout=100))
            if recv in evts:
                    self.topic = str( recv.recv_string())
                    self.statusmsg =  recv.recv_json()
                    time.sleep(0.2)

            # runs like an idle stage so program can wait for face to be recived
            if self.getAmmountOfFaces(frame) <= 0:

                time.sleep(0.5)
                pipe.on_event(event=pipelineStates.States.IDLE, sender=sender,receiver=recv, poller=self.poller,imagesocket=imagesocket)

            # processes faces when seen
            if self.getAmmountOfFaces(frame) > 0:
                face_processing_pipeline_timer = datetime.now()

                # allows total var to incrament All Seen Faces
                self.Total += self.getAmmountOfFaces(frame)

                #*Sends images over zmq
                imagesocket.send_jpg('IMAGE', jpg_buffer)
                
                #* only runs when recvices messages from the live rec
                if self.topic == "LIVENESS":
                        
                    if self.statusmsg['alive'] == False:
                        
                        if(const.isdevpc):
                            
                            consoleLog.Pipeline_Data_Block("Data recved from liveness...",
                            "Time M"+ "essage Sent "+ str(self.statusmsg['time']),
                            "Blinked about"+ " "+str(self.statusmsg['times_blinked']),
                            "IS Alive "+ " "+ "True",
                            "Has a body "+ " "+ str(self.statusmsg['hasBody']),
                            "End of data dump from liveness"+"\n")

                            time.sleep(.2)

                            self.liveness = False
                       
                        if(self.statusmsg['hasBody'] == True):
                            
                            consoleLog.Pipeline_Data_Block("Data recved from liveness...",
                            "Time M"+ "essage Sent "+ str(self.statusmsg['time']),
                            "Blinked about"+ " "+str(self.statusmsg['times_blinked']),
                            "IS Alive "+ " "+ "True",
                            "Has a body "+ " "+ str(self.statusmsg['hasBody']),
                            "End of data dump from liveness"+"\n")

                            time.sleep(.2)
                            
                            self.liveness = False
                        
                    else:
                        self.liveness = True
                        
                    
                
                   
                
                #* this allows me to only un check face status when the face liveness is true allows pipline to continue
                if( self.liveness == False):

                    consoleLog.PipeLine_Ok("LiveNess is Active so Its time to process data")
                    
                    self.checkFaceStatus(
                        predictions=predictions,
                        sender=sender,
                        frame=frame,
                        face_processing_pipeline_timer=face_processing_pipeline_timer,
                        process_this_frame=process_this_frame,
                        status=status,
                        liveness=self.liveness
                    )
                else:
                    time.sleep(0.5)
                    pipe.on_event(event=pipelineStates.States.IDLE, sender=sender,receiver=self.receiver, poller=self.poller,imagesocket=imagesocket)

    # this should check to see if the module is alive if not it will set the info to true so it does not run 
            if const.liveness_watchdog == 2:
                consoleLog.Error("liveness module not respsonding setting liveness module boolean to false...")
                self.topic = ""
                self.liveness = False

            if const.watchdog == 10:
                self.sendProgramStatus(
                    sender, "ERROR", "WATCHDOG OVERRRAN", datetime.now()
                )
                return pipelineStates.States.ERROR

    # * this will loop through and check face statuss
    def checkFaceStatus(
        self,
        predictions,
        sender,
        frame,
        face_processing_pipeline_timer,
        process_this_frame,
        status,
        liveness
    ):

        # Display t he results
        for name, (top, right, bottom, left) in predictions:

            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            if name != None:

                if name not in const.userList[self.i]:

                    phone = int(const.phoneconfig["default_num"])

                    if name == "unknown":
                        status = Status.UNKNOWN

                    if status == Status.UNKNOWN:
                        self.Unreconized += self.getAmmountOfFaces(frame)

                        self.StatusUnknown(
                            sender,
                            name=name,
                            phone=phone,
                            frame=frame,
                            left=left,
                            right=right,
                            bottom=bottom,
                            top=top,
                            face_processing_pipeline_timer=face_processing_pipeline_timer,
                            process_this_frame=process_this_frame,
                        )

                    if self.i < len(const.userList):
                        self.i += 1

                    if self.i == len(const.userList):
                        self.i = 0

                if name in const.userList[self.i]:

                    self.Reconized += self.getAmmountOfFaces(frame)

                    userinfo = const.userList[self.i][name]

                    status = userinfo[1]
                    usrname = userinfo[0]
                    phone = userinfo[4]

                    status = int(status)

                    if phone == None or 0000000000 or 0:
                        phone = int(const.phoneconfig["default_num"])

                    if status == Status.ADMIN:
                        self.StatusAdmin(
                            sender,
                            status=status,
                            usrname=usrname,
                            phone=phone,
                            frame=frame,
                            left=left,
                            right=right,
                            bottom=bottom,
                            top=top,
                            face_processing_pipeline_timer=face_processing_pipeline_timer,
                        )

                    if status == Status.USER:
                        self.StatusUser(
                            sender,
                            status=status,
                            usrname=usrname,
                            phone=phone,
                            frame=frame,
                            left=left,
                            right=right,
                            bottom=bottom,
                            top=top,
                            face_processing_pipeline_timer=face_processing_pipeline_timer,
                        )

                    if status == Status.UNWANTED:
                        self.StatusUnwanted(
                            sender,
                            status=status,
                            usrname=usrname,
                            phone=phone,
                            frame=frame,
                            left=left,
                            right=right,
                            bottom=bottom,
                            top=top,
                            face_processing_pipeline_timer=face_processing_pipeline_timer,
                        )

                    if self.getAmmountOfFaces(frame) > 2:
                        pass

                    self.sendFaceCount(
                        sender,
                        self.Total,
                        self.Unreconized,
                        self.Reconized,
                        datetime.now(),
                    )

            else:

                consoleLog.PipeLine_Ok(
                    "Time For non Face processed frames"
                    + str(datetime.now() - face_processing_pipeline_timer)
                )

                return
