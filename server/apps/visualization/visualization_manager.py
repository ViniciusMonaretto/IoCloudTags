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
        self.render("../../webApp/index.html")

class VisualizationWebSocketHandler(tornado.websocket.WebSocketHandler):
    _panels_count = 1

    def check_origin(self, origin):
        return True

    def initialize(self, database_connector):
        self.id = str(uuid.uuid4())
        self._middleware:ClientMiddleware  = middleware
        self._status_subscribers: dict[str, SubscriberInterface] = {}

        ui_visualizer_lock.acquire()

        script_directory = os.path.dirname(os.path.abspath(__file__))
        json_directory = os.path.join(script_directory, "ui_config.json")

        with open(json_directory, 'r') as json_file:
            try:
                data = json.load(json_file)  # Load the JSON data
                # Process the JSON data (replace this with your logic)
                self.add_panels(data)
                self._ui_config = data

                print(f"Processing file: {json_directory}")
            except json.JSONDecodeError as e:
                print(f"Error processing file {json_directory}: {e}")
        ui_visualizer_lock.release()
    
    def open(self):
        print("WebSocket opened")
        self._is_init = True
        self.send_message_to_ui("uiConfig", self._ui_config)

    def on_message(self, message):
        print("You said: " + message)
        messageObj = json.loads(message)
        payload = messageObj["payload"]
        try:
            if("addPanel" in messageObj["commandName"]):
                self.add_new_panel(payload)
            elif "removePanel" in messageObj["commandName"]:
                self.remove_panel(payload)
            elif "getStatusHistory" in messageObj["commandName"]:
                self.request_status(payload)
            else:
                print("unknown command: " + messageObj["commandName"])
        except Exception as e:
            print(f"Exception occured on panel message: {e}")

    def on_close(self):
        print("WebSocket closed")
        for subscriber_topic in self._status_subscribers:
            self._middleware.remove_subscribe_from_status(self._status_subscribers[subscriber_topic], subscriber_topic)