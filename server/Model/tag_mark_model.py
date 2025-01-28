from .model_interface import ModelInterface
from .user_model import User

from datetime import datetime

    
class TagMark(ModelInterface):
    _location_id: int
    _user_id: int
    _timestamp: datetime

    def __init__(self):
        self._location_id = None
        self._user_id = None
        self._timestamp = None

    def initialize(self, location: int, user: User, timestamp: datetime):
        self._location_id = location
        self._user_id = user._id
        self._timestamp = timestamp
    
    def getCollectionName(self) -> str:
        return "TagMarks"

    def getModelObject(self) -> dict[str, object]:
        model = {}
        model["UserId"] = self._user_id
        model["LocationId"] = self._location_id 
        model["Timestamp"] = self._timestamp 

        return model

    def setModelObject(self, model_gen_object: dict[str, object]):
        self._id = model_gen_object["id"]
        self._user_id = model_gen_object["UserId"]
        self._location_id = model_gen_object["LocationId"]
        self._timestamp = model_gen_object["Timestamp"]
    
    def toStr(self) -> str:
        json = {
            "id": self._id,
            "UserId": self._user_id,
            "LocationId": self._location_id,
            "Timestamp": str(self._timestamp)
        }

        return str(json)
    
    def __str__(self):
        return self.toStr()