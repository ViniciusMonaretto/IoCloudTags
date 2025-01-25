import tornado.ioloop
import tornado.web
import tornado.platform.asyncio
import os
import asyncio
import json

from services.database_conector.database_connector import DatabaseConnector
from Model.user_model import User

class RfidSet(tornado.web.RequestHandler):
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

        user.set_rfid(body["Rfid"])

        await self._database_connector.update_table_model(user, ["Rfid"])

        self.write(str([str(user) for user in users]))

class UserHandler(tornado.web.RequestHandler):
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
            self.write("Sucess")
        except json.JSONDecodeError:
            self.set_status(400)
            self.write("Invalid JSON data")

class ApiServer:
    def __init__(self, database_connector: DatabaseConnector):
        tornado.platform.asyncio.AsyncIOMainLoop().install()
        self._database_connector = database_connector
        self._app = self.make_app()       

    async def run(self):
        self.value = 10
        self._server = self._app.listen(8888)  # Listen on port 8888
        print("Server is running on http://localhost:8888")
        await asyncio.Event().wait()

    def stop(self):
        self._server.stop()

    def make_app(self):
        base_dir = os.path.dirname(__file__)  # Current directory of the server script
        angular_dist = os.path.join(base_dir, "../webApp")
        return tornado.web.Application([
           # (r"/", Visualization),
           # (r"/websocket", VisualizationWebSocketHandler, {'middleware': self._middleware}),
            (r"/user", UserHandler, {'database': self._database_connector}),
            (r"/user/rfid", RfidSet, {'database': self._database_connector}),
            (r"/user/all", UserHandler, {'database': self._database_connector}),
            (r"/user/(\d+)", UserHandler, {'database': self._database_connector}),
            (r"/(.*\.(js|css|ico|png|jpg|jpeg|woff|woff2|ttf|svg))", tornado.web.StaticFileHandler, {"path": angular_dist})
        ])