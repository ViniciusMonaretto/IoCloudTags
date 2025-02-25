import json
import tornado.ioloop
import tornado.web

from datetime import datetime

from src.services.database_conector.database_connector import DatabaseConnector
from src.Model.location_model import Location
from .base_handler import BaseHandler
from src.Model.user_model import TypeOfUser

class LocationHandler(BaseHandler):
    def initialize(self, database: DatabaseConnector):
        self._database_connector = database

    async def get(self, location_id=None):
            
        self.set_header("Content-Type", "application/json")
        condition = {"id": location_id} if location_id and location_id!="all" else None
        if(self.current_user["userType"] != TypeOfUser.Admin):
            condition = {"AdminUserId": self.current_user["userId"]}
        
        markings = await self._database_connector.find_info_from_table("Locations", condition)
        self.write(str([str(mark) for mark in markings]))

    async def post(self, location_id=None):
        # Parse JSON body to create a new user
        try:
            new_location_info = json.loads(self.request.body)
            if location_id:
                location = await self._database_connector.find_info_from_table("Locations", {"id": location_id})
                if len(location) == 0:
                    self.set_status(500)
                    self.write("Location not found")
                id = await self._database_connector.update_table_model(location, new_location_info)
                self.write(str(id))

            else:
                location = Location()
                location.initialize(new_location_info["Name"], new_location_info["Block"], new_location_info["Sector"], new_location_info["Uuid"], new_location_info["AdminUserId"])
                id = await self._database_connector.add_info_to_table(location)
                self.write(str(id))

        except json.JSONDecodeError:
            self.set_status(400)
            self.write("Invalid JSON data")
    
    async def delete(self, location_id):
        # Parse JSON body to create a new user
        try:
            id = await self._database_connector.remove_info_from_table("Locations", location_id)
            self.write("Sucess")
        except json.JSONDecodeError:
            self.set_status(400)
            self.write("Invalid JSON data")