import aiosqlite
import os
import json

from .database_config_model import DatabaseConfigModel
from Model.model_interface import ModelInterface

DB_NAME = "IoCloudDatabank.db"
DB_CONFIG = "database_config.json"

class DatabaseConnector:

    _config_models: dict[str, DatabaseConfigModel]
    def __init__(self, database_path: str):
        self._database_path = database_path

    async def initialize_data_bank(self):
        conn = await aiosqlite.connect(DB_NAME)
        cursor = await conn.cursor()

        self._config_models: dict[str, DatabaseConfigModel] = {}

        script_directory = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(script_directory, DB_CONFIG)
            
        with open(filename, 'r') as json_file:
            try:
                data = json.load(json_file) 
                
                for config in data["TableConfigs"]:
                    databaseConfig = DatabaseConfigModel(config)
                    self._config_models[databaseConfig.name] = databaseConfig
                    await cursor.execute(databaseConfig.createCommand) 

                await conn.commit()
                await conn.close()
            except json.JSONDecodeError as e:
                print(f"Error processing file {filename}: {e}")

    async def init_service(self):
        await self.initialize_data_bank()

    async def add_info_to_table(self, model: ModelInterface):
        model_obj = model.getModelObject()

        columns = ", ".join(model_obj.keys())
        placeholders = ", ".join(["?" for _ in model_obj.values()])
        query = f"INSERT INTO {model.getCollectionName()} ({columns}) VALUES ({placeholders})"

        async with aiosqlite.connect(DB_NAME) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, tuple(model_obj.values()))
                await conn.commit()
                last = cursor.lastrowid
                return last
    
    async def update_table_model(self, model: ModelInterface, keys_to_change: list[str]):
        conn = await aiosqlite.connect(DB_NAME)
        cursor = await conn.cursor()

        model_obj = model.getModelObject()

        columns = ""

        values = []
        length = len(keys_to_change)
        count = 0
        for key in keys_to_change:
            columns += key
            columns += " = ?"
            if length > count + 1:
                columns += ", "
            count+=1

            values.append(model_obj[key])

        query = f"UPDATE {model.getCollectionName()} SET {columns} WHERE id = ?"
        
        values.append(model._id)
        async with aiosqlite.connect(DB_NAME) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, tuple(values))
                await conn.commit()
                return True
    
    async def find_info_from_table(self, table_name, conditions: dict[str, str] = None):
        query = f"SELECT * FROM {table_name}"
        values = []

        if conditions:
            where_clause = " AND ".join([f"{col} = ?" for col in conditions.keys()])
            query += f" WHERE {where_clause}"
            values = list(conditions.values())

        async with aiosqlite.connect(DB_NAME) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)

                query_result: list[ModelInterface] = await cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                model_constructor: ModelInterface = self._config_models[table_name].model

                list_of_models = []
                for row in query_result:
                    model = model_constructor()
                    model.setModelObject(dict(zip(columns, row)))
                    list_of_models.append( model )

                return list_of_models
                    

    
    async def remove_info_from_table(self, table_name, id):
        query = f"DELETE FROM {table_name} WHERE id = ?"
        async with aiosqlite.connect(DB_NAME) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (id,))
                await conn.commit()
                count = cursor.rowcount
                return count
       