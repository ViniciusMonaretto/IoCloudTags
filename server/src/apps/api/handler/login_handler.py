import tornado.web
import json

from datetime import datetime

from src.services.database_conector.database_connector import DatabaseConnector
from src.Model.user_model import User
from .base_handler import BaseHandler
from ..token_manager import TokenManager

class LoginHandler(tornado.web.RequestHandler):
    def initialize(self, database: DatabaseConnector):
        self._database_connector = database

    async def post(self):
        login_info = json.loads(self.request.body)
        username = login_info["username"]
        password = login_info["password"]

        token_manager = TokenManager()

        userFound: list[User] = await self._database_connector.find_info_from_table("Users", conditions={"Name": username})

        if len(userFound) == 1 and userFound[0].verify_password(password):
            token = token_manager.add_token(username)
            self.write({"message": "Login successful", "token": token})
        else:
            self.set_status(401)
            self.write({"error": "Invalid username or password"})

class LogoutHandler(BaseHandler):
    def post(self):
        token = self.request.headers.get("Authorization")
        token_manager = TokenManager()
        if token:
            token_manager.remove_token(token)
        self.write({"message": "Logged out successfully"})