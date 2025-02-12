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
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  # Allow all origins
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")  # Allow specific methods
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")  # Allow specific headers

    def get(self):
        self.render("../../../webApp/index.html")