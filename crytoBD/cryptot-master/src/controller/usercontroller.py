
from src.model.users import User, insert_user, search_user_by_id, update_user, delete_user

def create_new_user():
    firstname = input("Ingresa el nombre: ")
    surname = input("Ingresa el apellido: ")
    idnumber = input("Ingresa el número de identificación: ")
    mail = input("Ingresa el correo electrónico: ")
    
    user = User(firstname, surname, idnumber, mail)
    insert_user(user)

def search_user():
    idnumber = input("Ingresa el número de identificación: ")
    search_user_by_id(idnumber)

def update_user_info():
    idnumber = input("Ingresa el número de identificación: ")
    firstname = input("Ingresa el nuevo nombre (deja en blanco para no cambiar): ")
    surname = input("Ingresa el nuevo apellido (deja en blanco para no cambiar): ")
    mail = input("Ingresa el nuevo correo electrónico (deja en blanco para no cambiar): ")
    
    user = User(firstname, surname, idnumber, mail)
    update_user(user)

def delete_existing_user():
    idnumber = input("Ingresa el número de identificación: ")
    delete_user(idnumber)