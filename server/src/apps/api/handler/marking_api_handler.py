import json
import tornado.ioloop
import tornado.web

from datetime import datetime

from src.services.database_conector.database_connector import DatabaseConnector
from src.Model.tag_mark_model import TagMark
from .base_handler import BaseHandler

class TagMarkHandler(BaseHandler):
    def initialize(self, database: DatabaseConnector):
        self._database_connector = database

    async def get(self, user_id=None):
        self.set_header("Content-Type", "application/json")
        condition = {"UserId": user_id} if user_id and user_id!="all" else None
        markings = await self._database_connector.find_info_from_table("TagMarks", condition)
        self.write(str([str(mark) for mark in markings]))

    async def post(self):
        # Parse JSON body to create a new user
        try:
            new_mark_info = json.loads(self.request.body)
            user = await self._database_connector.find_info_from_table("Users", {"id": new_mark_info["UserId"]})
            if len(user) != 1:
                self.set_status(500)
                self.write("User not found")
                return 

            location = await self._database_connector.find_info_from_table("Locations", {"id": new_mark_info["LocationId"]})
            if len(location) != 1:
                self.set_status(500)
                self.write("Location not found")
                return 
            
            time = datetime.strptime(new_mark_info["Timestamp"], "%Y-%m-%d %H:%M:%S")

            new_mark = TagMark()
            new_mark.initialize(location[0]._id, user[0], time)

            id = await self._database_connector.add_info_to_table(new_mark)
            self.write(str(id))
        except json.JSONDecodeError:
            self.set_status(400)
            self.write("Invalid JSON data")
    
    async def delete(self, marking_id):
        # Parse JSON body to create a new user
        try:
            id = await self._database_connector.remove_info_from_table("TagMarks", marking_id)
            self.write("Sucess")
        except json.JSONDecodeError:
            self.set_status(400)
            self.write("Invalid JSON data")