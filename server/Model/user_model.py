from .model_interface import ModelInterface
from enum import Enum
import bcrypt

class TypeOfUser(Enum):
    Unknow = 0
    Guard = 1
    Manager = 2
    Admin = 3
    

class User(ModelInterface):
    _name: str
    _email: str
    _phone_number: str
    _passwd_hash: str
    _type: TypeOfUser
    _rfid: str

    def __init__(self):
        self._name = None
        self._passwd_hash = None
        self._email = ""
        self._phone_number = ""
        self._type = TypeOfUser.Unknow
        self._rfid = None

    def initialize(self, name: str, email: str, phone_number:str, type_of_user: TypeOfUser, password: str, rfid: str):
        self._name = name
        self._email = email
        self._phone_number = phone_number
        self._type = TypeOfUser(type_of_user)
        self._passwd_hash = self.hash_password(password)
        self._rfid = rfid

    def set_rfid(self, rfid: str):
        self._rfid = rfid
    
    def getCollectionName(self) -> str:
        return "Users"

    def getModelObject(self) -> dict[str, object]:
        model = {}
        model["Name"] = self._name
        model["Email"] = self._email 
        model["PhoneNumber"] = self._phone_number
        model["Type"] = self._type.value
        model["HashedPassword"] = self._passwd_hash
        model["Rfid"] = self._rfid
        return model

    def setModelObject(self, model_gen_object: dict[str, object]):
        self._id = int(model_gen_object["id"])
        self._name = model_gen_object["Name"]
        self._email = model_gen_object["Email"]
        self._phone_number = model_gen_object["PhoneNumber"]
        self._type = TypeOfUser(model_gen_object["Type"])
        self._passwd_hash = model_gen_object["HashedPassword"]
        self._rfid = model_gen_object["Rfid"]
    
    def toStr(self) -> str:
        json = {
            "id": self._id,
            "Name": self._name,
            "Email": self._email,
            "PhoneNumber": self._phone_number,
            "Type": self._type.value,
            "Rfid": self._rfid
        }

        return str(json)
    
    def __str__(self):
        return self.toStr()

    def hash_password(self, password):
        # Convert username and password to bytes

        combined = f"{self._name}{password}".encode('utf-8')

        # Generate a salt
        salt = bcrypt.gensalt()

        # Hash the combined string with the generated salt
        hashed_password = bcrypt.hashpw(combined, salt)
        return hashed_password.decode('utf-8')

    def verify_password(self, password):
        combined = f"{self._name}{password}".encode('utf-8')

        # Verify the combined string against the stored hash
        return bcrypt.checkpw(combined, self._passwd_hash.encode('utf-8'))