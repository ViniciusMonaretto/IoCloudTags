from services.database_conector.database_connector import DatabaseConnector
from Model.user_model import User, TypeOfUser
from apps.app_manager import AppManager
import asyncio

async def main():
    dat = DatabaseConnector("")
    await dat.init_service()

    app_manager = AppManager(dat)

    await app_manager.run()

    # user = User("Joaquim Barbosa", "joaquim@gmail.com", "5199999999", TypeOfUser.Guard, "teste")

    # print(user.verify_password("teste"))
    # print(user.verify_password("teste1"))

    # await dat.remove_info_from_table(user.getCollectionName(), 2)
    # await dat.add_info_to_table(user)
    # users = await dat.find_info_from_table(user.getCollectionName())
    # print(users)
    # print(await dat.find_info_from_table(user.getCollectionName(), {"Name": "Joaquim Barbosa"}))
    # print(await dat.find_info_from_table(user.getCollectionName(), {"Name": "Joaquim Barbosa1"}))


asyncio.run(main())
