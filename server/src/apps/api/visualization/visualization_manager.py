import tornado.ioloop
import tornado.web
import tornado.websocket
import os
import json
import uuid

from threading import Thread
from threading import Lock

ui_visualizer_lock = Lock()

class Visualization(tornado.web.RequestHandler):
    def get(self):
        self.render("../../../webApp/index.html")