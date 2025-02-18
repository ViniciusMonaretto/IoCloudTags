import tornado.ioloop
import tornado.web
import tornado.platform.asyncio
import os
import asyncio
import json

from src.services.database_conector.database_connector import DatabaseConnector
from src.services.user_event_scheduler.user_event_scheduler import UserEventScheduler
from .handler.user_api_handler import UserChange, UserHandler
from .handler.marking_api_handler import TagMarkHandler
from .handler.location_api_handler import LocationHandler
from .handler.event_api_handler import EventApiHandler

from .visualization.visualization_manager import Visualization

from .handler.login_handler import LoginHandler, LogoutHandler


class ApiServer:
    def __init__(self, database_connector: DatabaseConnector,  user_scheduler: UserEventScheduler):
        tornado.platform.asyncio.AsyncIOMainLoop().install()
        self._database_connector = database_connector
        self._user_scheduler = user_scheduler
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
        angular_dist = os.path.join(base_dir, "../../webApp")
        return tornado.web.Application([
            (r"/", Visualization),
           # (r"/websocket", VisualizationWebSocketHandler, {'middleware': self._middleware}),
            (r"/location", LocationHandler, {'database': self._database_connector}),
            (r"/location/(\d+)", LocationHandler, {'database': self._database_connector}),
            (r"/tagmark", TagMarkHandler, {'database': self._database_connector}),
            (r"/tagmark/(\d+)", TagMarkHandler, {'database': self._database_connector}),
            (r"/user", UserHandler, {'database': self._database_connector}),
            (r"/user/change", UserChange, {'database': self._database_connector}),
            (r"/user/all", UserHandler, {'database': self._database_connector}),
            (r"/user/(\d+)", UserHandler, {'database': self._database_connector}),
            (r"/event", EventApiHandler, {'database': self._database_connector, 'userSchedule': self._user_scheduler}),
            (r"/login", LoginHandler, {'database': self._database_connector}),
            (r"/login", LogoutHandler, {'database': self._database_connector}),
            (r"/(.*\.(js|css|ico|png|jpg|jpeg|woff|woff2|ttf|svg))", tornado.web.StaticFileHandler, {"path": angular_dist})
        ])