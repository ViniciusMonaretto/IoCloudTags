from services.database_conector.database_connector import DatabaseConnector
from Model.user_model import User, TypeOfUser


if __name__ == "__main__":
    dat = DatabaseConnector("")
    dat.init_service()

    user = User("Joaquim Barbosa", "joaquim@gmail.com", "5199999999", TypeOfUser.Guard, "teste")

    print(user.verify_password("teste"))
    print(user.verify_password("teste1"))

    dat.remove_info_from_table(user.getCollectionName(), 1)
    dat.add_info_to_table(user)
    users = dat.find_info_from_table(user.getCollectionName())
    print()
    print(dat.find_info_from_table(user.getCollectionName(), {"Name": "Joaquim Barbosa"}))
    print(dat.find_info_from_table(user.getCollectionName(), {"Name": "Joaquim Barbosa1"}))
    
