import asyncio
from time import sleep
from services.database_conector.database_connector import DatabaseConnector
from .api.api_handler import ApiServer


class AppManager:
    def __init__(self, database_connector: DatabaseConnector):
        self._database_connector = database_connector
        self._api_server = ApiServer(self._database_connector)
        #self._mqtt = ApiServer(self._database_connector)
        
    async def run(self):
        tornado_task = asyncio.create_task(self._api_server.run())
        #mqtt_task = asyncio.create_task(self.start_mqtt_client())

        try:
            await asyncio.gather(tornado_task) #mqtt_task)
        except asyncio.CancelledError:
            print("Shutting down...")
            await self.stop()
    
    async def stop(self):
        """Stop Tornado and MQTT services."""
        if self._api_server:
            self._api_server.stop()
            print("API server stopped.")
        if self.mqtt_client:
            await self.mqtt_client.disconnect()
            print("MQTT client disconnected.")
    