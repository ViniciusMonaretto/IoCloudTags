import json
import tornado.ioloop
import tornado.web

from src.services.database_conector.database_connector import DatabaseConnector
from src.Model.user_model import User
from .admin_only import AdminHandler

class UserChange(AdminHandler):
    def initialize(self, database: DatabaseConnector):
        self._database_connector = database

    async def post(self):
        self.set_header("Content-Type", "application/json")
        body = json.loads(self.request.body)
        condition = {"id": body["id"]} if body["id"] and body["id"]!="all" else None
        users = await self._database_connector.find_info_from_table("Users", condition)
        if len(users) == 0:
            self.set_status(500)
            self.write("User not found")   
            return 
    
        user = users[0]

        await self._database_connector.update_table_model(user, body["Changes"])

        self.write("Sucess")

class UserHandler(AdminHandler):
    def initialize(self, database: DatabaseConnector):
        self._database_connector = database

    async def get(self, user_id=None):
        self.set_header("Content-Type", "application/json")
        condition = {"id": user_id} if user_id and user_id!="all" else None
        users = await self._database_connector.find_info_from_table("Users", condition)
        self.write(str([str(user) for user in users]))

    async def post(self):
        # Parse JSON body to create a new user
        try:
            new_user_model = json.loads(self.request.body)
            user = User()
            user.initialize(new_user_model["Name"], 
                            new_user_model["Email"], 
                            new_user_model["PhoneNumber"],
                            new_user_model["Type"],
                            new_user_model["Password"],
                            new_user_model['Rfid'])
            id = await self._database_connector.add_info_to_table(user)
            self.write(str(id))
        except json.JSONDecodeError:
            self.set_status(400)
            self.write("Invalid JSON data")
    
    async def delete(self, user_id):
        # Parse JSON body to create a new user
        try:
            id = await self._database_connector.remove_info_from_table("Users", user_id)
            self.write(str(id))
        except json.JSONDecodeError:
            self.set_status(400)
            self.write("Invalid JSON data")