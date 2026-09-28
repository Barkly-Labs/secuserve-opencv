"""
User stas this is where i have the seperate classes for the main opencv 

TODO: time to create unit tests for these methods in the class
"""

import cv2
import util.const as const
import time
from util import consoleLog


class UserStats(object):

    # this is for Handling User Admin Stats
    def userAdmin(
        self,
        status,
        name,
        frame,
        font,
        imagename,
        imagepath,
        left,
        right,
        bottom,
        top,
        recperesntage,
    ):

        print(status)
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.putText(frame, name, (left, top), font, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "Known Person..", (0, 430), font, 0.5, (255, 255, 255), 1)
        cv2.putText(
            frame,
            "Face Accuracy" + str(recperesntage),
            (0, 450),
            font,
            0.5,
            (255, 255, 255),
            1,
        )

        time.sleep(0.5)
        cv2.imshow("admin",frame)
        cv2.waitKey(1)
        consoleLog.PipeLine_Data("Admin Path = " + str(const.adminPath))

        self.saveImage(
            self, imagepath=const.adminPath, imagename=imagename, frame=frame
        )

    # User Grade Status
    # this is for Handling User Stats
    def userUser(
        self,
        status,
        name,
        frame,
        font,
        left,
        right,
        bottom,
        top,
        recperesntage,
        imagename,
        imagepath,
    ):

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 0), 2)

        cv2.putText(frame, name, (left, top), font, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "Known Person..", (0, 430), font, 0.5, (255, 255, 255), 1)

        cv2.putText(
            frame,
            "Face accuracy" + str(recperesntage),
            (0, 450),
            font,
            0.5,
            (255, 255, 255),
            1,
        )

        time.sleep(0.5)
        cv2.imshow("user",frame)
        cv2.waitKey(1)
        consoleLog.PipeLine_Data("User Path = " + str(const.usrPath))
        self.saveImage(self, imagepath=const.usrPath, imagename=imagename, frame=frame)

    # Handles Unwanted Usr Stats
    def userUnwanted(
        self,
        status,
        name,
        frame,
        font,
        imagename,
        imagePath,
        left,
        right,
        bottom,
        top,
        recperesntage,
    ):

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, top), font, 0.5, (255, 255, 255), 1)
        cv2.putText(
            frame,
            "Face accuracy" + str(recperesntage),
            (0, 480),
            font,
            0.5,
            (255, 255, 255),
            1,
        )
        cv2.imshow("unwanted",frame)
        cv2.waitKey(1)
        consoleLog.PipeLine_Data("unwated Path = " + str(const.unwantedPath))
        self.saveImage(
            self, imagepath=const.unwantedPath, imagename=imagename, frame=frame
        )

    # Handles unKnown User
    def userUnknown(
        self,
        opencvconfig,
        name,
        frame,
        font,
        imagepath,
        imagename,
        left,
        right,
        bottom,
        top,
        framenum,
        recperesntage,
    ):

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, top), font, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "Unknown Person..", (0, 430), font, 0.5, (255, 255, 255), 1)
        cv2.putText(
            frame,
            "Face Accuracy" + str(recperesntage),
            (0, 450),
            font,
            0.5,
            (255, 255, 255),
            1,
        )

        time.sleep(0.5)

        consoleLog.PipeLine_Data("Unknown Path = " + str(const.unknownPath))
        cv2.imshow("Unknown",frame)
        cv2.waitKey(1)
        self.saveImage(
            self, imagepath=const.unknownPath, imagename=imagename, frame=frame
        )

    # User Groups
    def userGroup(self, frame, font, imagepath, imagename, left, right, bottom, top):

        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 255), 2)
        cv2.putText(frame, "Group", (left, top), font, 0.5, (255, 255, 255), 1)

        # Distance info
        cv2.putText(
            frame,
            "There's a Cutie..",
            (474, 430),
            font,
            0.5,
            (255, 255, 255),
            1,
        )
        cv2.putText(
            frame,
            "be carfull now!",
            (474, 450),
            font,
            0.5,
            (255, 255, 255),
            1,
        )
        cv2.imshow("Unknown",frame)
        cv2.waitKey(1)
        self.saveImage(
            self, imagepath=const.groupPath, imagename=imagename, frame=frame
        )

    # saves owner images and sends Frame
    def saveImage(self, imagepath, imagename, frame):
        cv2.imwrite(imagepath + imagename + ".jpg", frame)
