"""
this class is for creating a config ini with default settings without having the user create one themselves
"""

import configparser


class Config(object):

    config = configparser.ConfigParser()

    # * this is the InI file Key So i can create all the Default for files
    config["FILE"] = {
        "rootDirPath": "../SecuServeFiles/",
        "configPath": "Config/",
        "imagePath": "caughtImages/",
        "platePath": "caughtPlates/",
        "imagePathusers": "user/people/",
        "loggingPath": "logging/",
        "adminimg": "Admin/",
        "usrimg": "user/",
        "unknownimg": "unknown/",
        "unwantedimg": "unwanted/",
        "groupimg": "group/",
    }

    # * this is the Opencv Config Stream
    config["OPENCV"] = {
        "unreconizedPerson": "Unkown Human?",
        "Stream_intro": "rtsp://",
        "Stream_ip": "Example_IP",
        "Stream_port": "554",
        "Stream_local": "output.h264",
    }

    # * This is the Logging key of the config file
    config["LOGGING"] = {"filename": "OpencvServer", "launcher": "Launcher"}

    # * Zmq key for config
    config["ZMQ"] = {"ip": "127.0.0.1", "port-recv": "5000", "port-send": "5001"}

    # * Default phone number key
    config["PHONE"] = {"default_num": "ENTER NUMBER"}

    #! this creates custom config file
    def createDefaultConfig(self):
        # * this is the InI file Key So i can create all the Default for files
        self.config["FILE"]

        # * this is the Opencv Config Stream
        self.config["OPENCV"]
        self.config["LOGGING"]

        # * Zmq key for config
        self.config["ZMQ"]
        self.config["PHONE"]

        with open("../SecuServeFiles/Config/Config.ini", "w") as configfile:
            self.config.write(configfile)

    # * returns new config
    def getConfig(self):
        return "../SecuServeFiles/Config/Config.ini"


    