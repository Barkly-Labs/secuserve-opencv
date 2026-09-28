"""
Tests The Pipeline Using Mocks
TODO: what does set up correctly mean? -> me anseer

TODO: TEST DRIVEN DEV For Setup of pipe line 
SETUP FOR PIPELINE:

 read config file 
 read config file if none create one 
 
 try to connect to zmq messaging backend 
 try to connect to zmq messaging backend if fails see why it faild
  
 check config file for requrid entrys 
 check config file has no entrys create some 
 check to see if basic file strucure is set up 
 check to see if basic file strucure is not setup set it up
 
 Connects to database and see if the data is not null and returns the userData
 Connects to database and see if the data is null reread 4 times  data if still null throws acception cant continue to run
 Checks to see if data was added to database
 
 Created DataStruct to store data from Database to be used
 Created DataStruct is has empty entryes in it try to fill the DataStruct again
 Created DataStruct is null throws acception cant continue to run
 
 TRAINS MODEL FOR PIPELINE:
 
 loads up all trained models 
 loads up all trained models and sees if the model is a vaild model
 loads up all trained models if correpet retrain it
 loades up all trained models if none train one 
 loads up all trained models if there is an new user in the db train a new model
 
 Reconizes Faces PipeLine:
 
 Connects to rtsp camera and check if the stream is a vaild stream continue to use stream
 Connects to rtsp camera if the rtsp camera stream is empty retrys connection 4 times
 Connects to rtsp fails throws acception cant continue to run because cant cannect to cam
 
 checks for a face in the rtsp stream
 checks for a face in the rtsp stream if there is no face go into idle mode (waits till face is seen) and set status led light to static on
 
 checks for a face in the rtsp stream if there is a face it pass the frame to the face reconition and set status led light to Blinking on
 checks for a face in the rtsp stream if the frame is corrupt grab new frame
 
 Uses the Face Recontion model to see if the  face is in the model return the faces identifyer
 Uses the Face Recontion model to see if the  face is  not in the model return unknown
 Uses the Face Recontion model to see if are no faces in model thow error 
 
 Checks to see if the output from the Face Rec is null throws execption this should not be null
 Checks to see if the output from the Face Rec is a identifer then get the data that from UserDataStruct that goes with the retreived identitfyer
 
 Checks for a group of people 
 Checks for a group of people if there is more than 2 people return both face identifyers 
 Checks for a group of people if there is more less 2 people return the face identifyer
 
 Retrives Status of each seen person every 250ms and set processing led to blink on
 Retrives Status, Name, phonenumber of each seen person Seen from the UserDataStruct Reconized by the Model
 Retrives Status of each seen person if there are no people return status equles none 
 Retrives Status of each seen person if the seen person is admin,user,unwanted,unknown save captured frame with time stamp and user status 
 Retrives Status of each seen person if the seen person is  admin,user,unwanted,unknown send zmq messge to Texting Module 
 
 
 
"""
from configparser import ConfigParser
import unittest
from unittest.mock import Mock
from pathlib import Path
from util.configcreator import Config as creator
import util.consoleLog as consoleLog


class TestConfig(unittest.TestCase):

    mock = Mock()

    """
    this is for testing the reading the config for the pipeline
    """

    def test_config_reading(self):

        conf = ConfigParser()
        config = conf.read(str(Path().absolute()) + "/data/" + "Config.ini")
        self.assertIsNotNone(config)
