import asyncio
from time import sleep
from services.database_conector.database_connector import DatabaseConnector
#from .visualization.visualization_manager import Visualization, VisualizationWebSocketHandler


import tornado.web
import os

class AppManager:
    def __init__(self, database_connector: DatabaseConnector):
        self._database_connector = database_connector
        self.m_Server = AppServer(self._database_connector)
        self.thread = Thread(target = self.threaded_function, args = (10, ))   

    def threaded_function(self, args):
        self.m_Server.run()
    
    def run(self):
        self.thread.start()

    async def join(self):
        await asyncio.Event().wait()

class AppServer:
    def __init__(self, database_connector: DatabaseConnector):
        self._database_connector = database_connector
        self.app = self.make_app()       

    def run(self):
        self.value = 10
        self.app.listen(8888)  # Listen on port 8888
        print("Server is running on http://localhost:8888")
        tornado.ioloop.PeriodicCallback(self.send_test_messages, 200).start()
        tornado.ioloop.IOLoop.current().start()

    def send_test_messages(self):
        self._middleware.run_middleware_update()

    def make_app(self):
        base_dir = os.path.dirname(__file__)  # Current directory of the server script
        angular_dist = os.path.join(base_dir, "../webApp")
        return tornado.web.Application([
           # (r"/", Visualization),
           # (r"/websocket", VisualizationWebSocketHandler, {'middleware': self._middleware}),
            (r"/test", ServerHandler),
            (r"/(.*\.(js|css|ico|png|jpg|jpeg|woff|woff2|ttf|svg))", tornado.web.StaticFileHandler, {"path": angular_dist})
        ],
        static_path="C:/Titanium/TitaniumServer/web/titanium-server/dist/titanium-server")
    