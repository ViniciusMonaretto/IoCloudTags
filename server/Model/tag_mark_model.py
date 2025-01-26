from .model_interface import ModelInterface
from .user_model import User

from datetime import datetime

    
class TagMark(ModelInterface):
    _location: str
    _user_id: int
    _timestamp: datetime

    def __init__(self):
        self._location = ""
        self._user_id = None
        self._timestamp = None

    def initialize(self, location: str, user: User, timestamp: datetime):
        self._location = location
        self._user_id = user._id
        self._timestamp = timestamp
    
    def getCollectionName(self) -> str:
        return "TagMarks"

    def getModelObject(self) -> dict[str, object]:
        model = {}
        model["UserId"] = self._user_id
        model["Location"] = self._location 
        model["Timestamp"] = self._timestamp 

        return model

    def setModelObject(self, model_gen_object: dict[str, object]):
        self._id = model_gen_object["id"]
        self._user_id = model_gen_object["UserId"]
        self._location = model_gen_object["Location"]
        self._timestamp = model_gen_object["Timestamp"]
    
    def toStr(self) -> str:
        json = {
            "id": self._id,
            "UserId": self._user_id,
            "Location": self._location,
            "Timestamp": str(self._timestamp)
        }

        return str(json)
    
    def __str__(self):
        return self.toStr()