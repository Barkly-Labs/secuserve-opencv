""" 
this file is for testing the datasturue for handing faces
#author Nicholas 
"""
import unittest
import pipeline.faceDataStruture as face
from sklearn import neighbors


class TestFaceData(unittest.TestCase):

    """
    This is for only testing the name is correct
    """

    def test_data_structure_user_name_(self):

        data = face.UserData(
            name="nick",
            status=0,
            image="image",
            downloadurl="https://example.com",
            phonenumber=4123891615,
        )
        self.assertEqual(
            str("nick"), str(face.UserData.getUserName(data)), "should Return name "
        )

    """
    This is for only testing the user is correct
    """

    def test_data_structure_user_status(self):

        data = face.UserData(
            name="nick",
            status=0,
            image="image",
            downloadurl="https://example.com",
            phonenumber=4123891615,
        )
        self.assertEqual(
            str(0),
            str(face.UserData.getUserStatus(data)),
            "should Return userStatus ",
        )

    """
    This is for only testing the image is correct
    """

    def test_data_structure_user_image(self):

        data = face.UserData(
            name="nick",
            status=0,
            image="image",
            downloadurl="https://example.com",
            phonenumber=4123891615,
        )
        self.assertEqual(
            str("image"),
            str(face.UserData.getUserImg(data)),
            "should Return userImage ",
        )

    """
    This is for only testing the downloadurl is correct
    """

    def test_data_structure_user_image_url(self):

        data = face.UserData(
            name="nick",
            status=0,
            image="image",
            downloadurl="https://example.com",
            phonenumber=4123891615,
        )
        self.assertEqual(
            str("https://example.com"),
            str(face.UserData.getUserUrl(data)),
            "should Return user Url ",
        )

    """
    This is for only testing the phonenumber is correct
    """

    def test_data_structure_user_phonenumber(self):

        data = face.UserData(
            name="nick",
            status=0,
            image="image",
            downloadurl="https://example.com",
            phonenumber=4123891615,
        )
        self.assertEqual(
            4123891615,
            face.UserData.getUserPhoneNumber(data),
            "should Return user phone number ",
        )
