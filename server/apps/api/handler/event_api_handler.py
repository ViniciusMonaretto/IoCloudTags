import json
import tornado.ioloop
import tornado.web

from datetime import datetime

from services.database_conector.database_connector import DatabaseConnector
from services.user_event_scheduler.user_event_scheduler import UserEventScheduler
from Model.event_model import EventModel

class EventApiHandler(tornado.web.RequestHandler):
    def initialize(self, database: DatabaseConnector, userSchedule: UserEventScheduler):
        self._database_connector = database
        self._event_schedule = userSchedule

    async def getAllEvents(self, conditions):
        return await self._database_connector.find_info_from_table("EventModels", conditions)

    async def get(self):
        self.set_header("Content-Type", "application/json")
        event_info = json.loads(self.request.body.count() > 0) if self.request.body else None
        events = await self._database_connector.find_info_from_table("EventModels", event_info)
        self.write(str([str(evt) for evt in events]))

    async def post(self):
        try:
            new_event = json.loads(self.request.body)
            user = await self._database_connector.find_info_from_table("Users", {"id": new_event["UserId"]})
            if len(user) != 1:
                self.set_status(500)
                self.write("User not found")
                return 

            location = await self._database_connector.find_info_from_table("Locations", {"id": new_event["LocationId"]})
            if len(location) != 1:
                self.set_status(500)
                self.write("Location not found")
                return 
            
            begin_date = datetime.strptime(new_event["BeginDate"], "%Y-%m-%d %H:%M:%S")
            end_date = datetime.strptime(new_event["EndDate"], "%Y-%m-%d %H:%M:%S")

            evt = EventModel()
            evt.initialize(location[0], user[0], begin_date, end_date)

            id = await self._database_connector.add_info_to_table(evt)

            await self._event_schedule.check_event_for_user(user[0]._id)
            self.write(str(id))
        except json.JSONDecodeError:
            self.set_status(400)
            self.write("Invalid JSON data")
    
    async def delete(self, marking_id):
        # Parse JSON body to create a new user
        try:
            id = await self._database_connector.remove_info_from_table("EventModels", marking_id)
            self.write("Sucess")
        except json.JSONDecodeError:
            self.set_status(400)
            self.write("Invalid JSON data")