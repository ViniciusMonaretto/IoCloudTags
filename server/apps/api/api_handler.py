import tornado.ioloop
import tornado.web
import tornado.platform.asyncio
import os
import asyncio
import json

from services.database_conector.database_connector import DatabaseConnector
from .handler.user_api_handler import UserChange, UserHandler
from .handler.marking_api_handler import TagMarkHandler


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
            (r"/tagmark", TagMarkHandler, {'database': self._database_connector}),
            (r"/tagmark/(\d+)", TagMarkHandler, {'database': self._database_connector}),
            (r"/user", UserHandler, {'database': self._database_connector}),
            (r"/user/change", UserChange, {'database': self._database_connector}),
            (r"/user/all", UserHandler, {'database': self._database_connector}),
            (r"/user/(\d+)", UserHandler, {'database': self._database_connector}),
            (r"/(.*\.(js|css|ico|png|jpg|jpeg|woff|woff2|ttf|svg))", tornado.web.StaticFileHandler, {"path": angular_dist})
        ])