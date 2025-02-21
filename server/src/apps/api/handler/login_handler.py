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
    
    def options(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")  # Allow all origins, or specify allowed origins
        self.set_header("Access-Control-Allow-Methods", "POST, DELETE, GET, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Skip-Error-Log")
        self.set_status(204)  # No Content for preflight
        self.finish()

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  # Allow all origins
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")  # Allow specific methods
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Skip-Error-Log")  # Allow specific headers

    async def post(self):
        login_info = json.loads(self.request.body)
        username = login_info["username"]
        password = login_info["password"]

        token_manager = TokenManager()

        userFound: list[User] = await self._database_connector.find_info_from_table("Users", conditions={"Name": username})

        if len(userFound) == 1 and userFound[0].verify_password(password):
            token = token_manager.add_token(userFound[0]._type, userFound[0]._id)
            self.write({"message": "Login successful", "token": token})
        else:
            self.set_status(401)
            self.write({"error": "Invalid username or password"})

class LogoutHandler(BaseHandler):
    def get(self):
        self.set_header("Content-Type", "application/json")
        user = self.current_user
        obj = {"userId": user['userId'],
               "userType": user['userType'].value}
        self.write(obj)

    def post(self):
        token = self.request.headers.get("Authorization")
        token_manager = TokenManager()
        if token:
            token_manager.remove_token(token)
        self.write({"message": "Logged out successfully"})