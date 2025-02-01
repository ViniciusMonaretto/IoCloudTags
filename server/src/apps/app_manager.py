import asyncio
from time import sleep
from services.database_conector.database_connector import DatabaseConnector
from services.user_event_scheduler.user_event_scheduler import UserEventScheduler
from .api.api_handler import ApiServer
from .mqtt_client.mqtt_client import IoCLoudMqttCLient


class AppManager:
    def __init__(self, database_connector: DatabaseConnector, user_scheduler: UserEventScheduler):
        self._database_connector = database_connector
        self._user_scheduler = user_scheduler
        self._api_server = ApiServer(self._database_connector, self._user_scheduler)
        self._mqtt_client = IoCLoudMqttCLient(self._database_connector)
        
        #self._mqtt = ApiServer(self._database_connector)
        
    async def run(self):
        self._tornado_task = asyncio.create_task(self._api_server.run())
        self._mqtt_task = asyncio.create_task(self._mqtt_client.run())
        #mqtt_task = asyncio.create_task(self.start_mqtt_client())

        try:
            await asyncio.gather(self._tornado_task, self._mqtt_task)
        except asyncio.CancelledError:
            print("Shutting down...")
            await self.stop()
    
    async def stop(self):
        """Stop Tornado and MQTT services."""
        if self._api_server:
            self._api_server.stop()
            print("API server stopped.")
        if self._mqtt_client:
            await self._mqtt_client.stop()
            print("MQTT client disconnected.")
    