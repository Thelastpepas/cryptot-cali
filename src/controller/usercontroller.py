# src/controller/usercontroller.py

from src.controller.users import User, insert_user, search_user_by_id, update_user, delete_user

def create_new_user_web(firstname, surname, idnumber, mail):
    user = User(firstname, surname, idnumber, mail)
    return insert_user(user)

def search_user(idnumber):
    return search_user_by_id(idnumber)

# src/controller/usercontroller.py
def update_user_info_web(firstname, surname, idnumber, mail):
    user = User(firstname, surname, idnumber, mail)
    return update_user(user)  # Asegúrate de que update_user reciba un objeto User


def delete_existing_user(idnumber):
    return delete_user(idnumber)  # Retorna el resultado de la función delete_user

