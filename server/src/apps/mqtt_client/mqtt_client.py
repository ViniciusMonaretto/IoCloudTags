from asyncio_mqtt import Client as MqttClient, MqttError
from asyncio_mqtt.client import Message
import asyncio
from datetime import datetime
import json

from src.services.database_conector.database_connector import DatabaseConnector

from src.Model.tag_mark_model import TagMark


SUBSCRIBE_TOPIC = "/ioCLoud/#"

MQTT_SERVER = "mqtt.eclipseprojects.io"

MQTT_PORT = 1883


class IoCLoudMqttCLient:
    def __init__(self, database_connector: DatabaseConnector):
        self._database_connector = database_connector
        self._stop_event = asyncio.Event()
            
    async def on_message(self, msg:Message):
        topic = msg.topic.value
        payload =  json.loads(msg.payload.decode())
        msg_split = topic.split('/')

        if not len(msg_split) == 4:
            print(f"IoCloud::on_message: mqtt topic {topic} not valid")
            return

        id = str(msg_split[2])

        print(f"Received message: {topic} {payload} {id}")

        user_query = (await self._database_connector.find_info_from_table("Users", {"Rfid": payload["rfid"]}))
        if len(user_query) == 0:
            return
        
        location_query = await self._database_connector.find_info_from_table("Locations", {"GatewayUuid": id})
        if len(location_query) != 1:
            self.set_status(500)
            self.write("Location not found")
            return 
        
        user = user_query[0]
        time = datetime.fromisoformat(payload["timestamp"])

        tag_mark = TagMark()
        tag_mark.initialize(location_query[0]._id, user, time)
        await self._database_connector.add_info_to_table(tag_mark)
        

    async def mqtt_receiver(self):
        """Task to receive MQTT messages."""
        await self._client.subscribe(SUBSCRIBE_TOPIC)
        print(f"Subscribed to {SUBSCRIBE_TOPIC}")

        try:
            async with self._client.messages() as messages:
                async for message in messages:
                    await self.on_message(message)
                    if self._stop_event.is_set():
                        print("Stop event set, exiting receiver...")
                        break
        except MqttError as e:
            print(f"MQTT error while receiving: {e}")

    async def mqtt_sender(client):
        """Task to send MQTT messages."""
        try:
            count = 0
            while True:
                topic = f"/topicIo/test/{count}"
                message = f"Message {count}"
                await client.publish(topic, message)
                print(f"Published to {topic}: {message}")
                count += 1
                await asyncio.sleep(5)  # Send a message every 5 seconds
        except MqttError as e:
            print(f"MQTT error while sending: {e}")

    async def run(self):
        async with MqttClient(MQTT_SERVER, MQTT_PORT) as client:
            # Create tasks for receiving and sending
            self._client = client
            self._receiver_task = asyncio.create_task(self.mqtt_receiver())

            try:
                await asyncio.gather(self._receiver_task)
            except KeyboardInterrupt:
                print("Stopping tasks...")
            finally:
                self._receiver_task.cancel()

    def stop(self):
        self._stop_event.set()
    
    def execute(self, command):
        topic = self.get_topic_from_command(command.name)
        self.client.publish(topic, command.message)
    
    def get_topic_from_command(self, command):
        if command in  self._publish_topics_list:
            return self._publish_topics_list["command"]
        return command

    @staticmethod
    def get_topic_from_mosquitto_obj(mosquitto_id, cls):
        return mosquitto_id + '/' + cls['name']