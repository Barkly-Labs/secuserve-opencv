"""
this class is for handling the User data 
Passes data into class validate class data
like if the user daya is empty i test the data if its 

"""


class UserData:

    _user: str
    _status: str
    _image: str
    _downloadUrl: str
    _phonenum: str

    USA_PHONE_NUMBER_DIGIT_COUNT = 10

    def __init__(
        self, name: str, status: str, image: str, downloadurl: str, phonenumber: str
    ) -> list:
        self.setUserName(name)
        self.setUserStatus(status)
        self.setUserImg(image)
        self.setUserUrl(downloadurl)
        self.setUserPhoneNumber(phonenumber)

    # this gets the  number of digits in the phone number
    def getSumOfDigits(self, phonenumber) -> int:
        return sum(c.isdigit() for c in phonenumber)

    # sets user name in structure

    def setUserName(self, name) -> str:
        Username = name

        if Username == "" or None:
            raise (TypeError("Cant have No Name the user name"))
        if Username.isnumeric():
            raise (TypeError("Cant have a number user name "))
        else:
            self._user = Username

        # sets user status in structure

    def setUserStatus(self, status) -> int:
        stat = str(status)

        if stat == "" or None:
            raise (TypeError("Cant have No Name status"))
        else:
            self._status = int(stat)

        # sets user image in structure

    def setUserImg(self, img) -> str:
        imgage = str(img)

        if imgage == "" or None:
            raise (TypeError("Cant have No Image"))
        else:
            self._image = imgage

    # checks url to see if tis formatted correctly
    def setUserUrl(self, url):
        checkyurl = str(url)

        if checkyurl == "" or None:
            raise (TypeError("Cant have No URL"))

        else:
            self._downloadUrl = str(url)

    # checks phone to see if tis formatted correctly
    def setUserPhoneNumber(self, phonenumber) -> int:
        phonenum = str(phonenumber)

        if phonenum == "" or None:
            raise (TypeError("Cant have No PhoneNumber"))

        if (
            phonenum.isnumeric()
            and self.getSumOfDigits(phonenum) > self.USA_PHONE_NUMBER_DIGIT_COUNT
            or self.getSumOfDigits(phonenum) < self.USA_PHONE_NUMBER_DIGIT_COUNT
        ):
            # this is the default no Number in the database for non admin users so this should return
            if int(phonenum) == 0000000000:
                self._phonenum = int(phonenum)

            print(
                IndexError(
                    "Number needs to be at "
                    + " "
                    + str(self.USA_PHONE_NUMBER_DIGIT_COUNT)
                    + " "
                    + "Long!"
                )
            )

        else:
            self._phonenum = int(phonenum)

    # gets user name in structure
    def getUserName(self):
        return self._user

    # gets user status in structure

    def getUserStatus(self):
        return self._status

        # gets user image in structure

    def getUserImg(self):
        return self._image

    # checks url to see if tis formatted correctly

    def getUserUrl(self):
        return self._downloadUrl

    # checks url to see if tis formatted correctly

    def getUserPhoneNumber(self):
        return self._phonenum

    def __repr__(self) -> list:

        return [
            self.getUserName(),
            self.getUserStatus(),
            self.getUserImg(),
            self.getUserUrl(),
            self.getUserPhoneNumber(),
        ]
