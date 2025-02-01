from .model_interface import ModelInterface
from .user_model import User
from .location_model import Location

from datetime import datetime

    
class EventModel(ModelInterface):
    _location_id: int
    _user_id: int
    _begin_date: datetime
    _end_date: datetime

    def __init__(self):
        self._location_id = None
        self._user_id = None
        self._begin_date = None
        self._end_date = None

    def initialize(self, location: Location, user: User, begin_date: datetime, end_date: datetime):
        self._location_id = location._id
        self._user_id = user._id
        self._begin_date = begin_date
        self._end_date = end_date
    
    def getCollectionName(self) -> str:
        return "EventModels"

    def getModelObject(self) -> dict[str, object]:
        model = {}
        model["UserId"] = self._user_id
        model["LocationId"] = self._location_id 
        model["BeginDate"] = self._begin_date 
        model["EndDate"] = self._end_date 

        return model

    def setModelObject(self, model_gen_object: dict[str, object]):
        self._id = model_gen_object["id"]
        self._user_id = model_gen_object["UserId"]
        self._location_id = model_gen_object["LocationId"]
        self._begin_date = model_gen_object["BeginDate"]
        self._end_date = model_gen_object["EndDate"]
    
    def toStr(self) -> str:
        json = {
            "id": self._id,
            "UserId": self._user_id,
            "LocationId": self._location_id,
            "BeginDate": str(self._begin_date),
            "EndDate": str(self._end_date)
        }

        return str(json)
    
    def __str__(self):
        return self.toStr()