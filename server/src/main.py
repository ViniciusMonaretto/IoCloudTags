from src.services.database_conector.database_connector import DatabaseConnector
from src.Model.user_model import User, TypeOfUser
from apps.app_manager import AppManager
from src.services.user_event_scheduler.user_event_scheduler import UserEventScheduler
import asyncio
from datetime import datetime, timedelta

def prt(user_id = 1, message = ""):
    print(f"Event triggered for user {user_id}: {message}")


async def CreateAdminUser(dat: DatabaseConnector):
    userFound = await dat.find_info_from_table("Users", conditions={"Name": "admin"})
    if(len(userFound) == 0):
        user = User()
        user.initialize("admin", "here", "werwer", TypeOfUser.Admin, "admin", "")
        await dat.add_info_to_table(user)

async def main():
    dat = DatabaseConnector("")
    await dat.init_service()

    await CreateAdminUser(dat)

    user_scheduler = UserEventScheduler(dat)
    await user_scheduler.init_scheduler()

    app_manager = AppManager(dat, user_scheduler)

    await app_manager.run()

    # now = datetime.now()

    # user_scheduler.add_user_event(1, now + timedelta(seconds=20), prt)

    # print(user.verify_password("teste"))
    # print(user.verify_password("teste1"))

    # await dat.remove_info_from_table(user.getCollectionName(), 2)
    # await dat.add_info_to_table(user)
    # users = await dat.find_info_from_table(user.getCollectionName())
    # print(users)
    # print(await dat.find_info_from_table(user.getCollectionName(), {"Name": "Joaquim Barbosa"}))
    # print(await dat.find_info_from_table(user.getCollectionName(), {"Name": "Joaquim Barbosa1"}))


asyncio.run(main())
