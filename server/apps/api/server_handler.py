import tornado.ioloop
import tornado.web

from services.database_conector.database_connector import DatabaseConnector

class GetAllUsersHandler(tornado.web.RequestHandler):
    def initialize(self, database_connector: DatabaseConnector):
        self._database_connector = database_connector

    def get(self):
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(self.users))