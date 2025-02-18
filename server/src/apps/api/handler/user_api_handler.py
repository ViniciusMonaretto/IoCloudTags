import json
import tornado.ioloop
import tornado.web

from src.services.database_conector.database_connector import DatabaseConnector
from src.Model.user_model import User
from .base_handler import BaseHandler

class UserChange(BaseHandler):
    def initialize(self, database: DatabaseConnector):
        self._database_connector = database
    
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  # Allow all origins
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")  # Allow specific methods
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")  # Allow specific headers

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

class UserHandler(BaseHandler):
    def initialize(self, database: DatabaseConnector):
        self._database_connector = database
    
    def options(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")  # Allow all origins, or specify allowed origins
        self.set_header("Access-Control-Allow-Methods", "POST, DELETE, GET, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.set_status(204)  # No Content for preflight
        self.finish()

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  # Allow all origins
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")  # Allow specific methods
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")  # Allow specific headers

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
                            None)
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