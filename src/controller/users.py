#controller/users.py
import psycopg2
import sys
sys.path.append("src")

from controller.SecretConfig import PGHOST, PGDATABASE, PGUSER, PGPASSWORD

class User:
    def __init__(self, firstname, surname, idnumber, mail):
        self.firstname = firstname
        self.surname = surname
        self.idnumber = idnumber
        self.mail = mail

    def __eq__(self, other):
        if isinstance(other, User):
            return (self.firstname == other.firstname and 
                    self.surname == other.surname and 
                    self.idnumber == other.idnumber and 
                    self.mail == other.mail)
        return False

def conectar_a_base_datos():
    try:
        conexion = psycopg2.connect(
            host=PGHOST,
            database=PGDATABASE,
            user=PGUSER,
            password=PGPASSWORD
        )
        
        return conexion
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def crear_tabla_users():
    try:
        connection = conectar_a_base_datos()
        if connection is None:
            return
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(100) NOT NULL,
            surname VARCHAR(100) NOT NULL,
            idnumber VARCHAR(50) UNIQUE NOT NULL,
            mail VARCHAR(100) NOT NULL
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
    
    except Exception as e:
        print("Error creando la tabla 'users':", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def insert_user(user):
    try:
        crear_tabla_users()
        connection = conectar_a_base_datos()
        if connection is None:
            return None
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO users (firstname, surname, idnumber, mail)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """
        cursor.execute(insert_query, (user.firstname, user.surname, user.idnumber, user.mail))
        user_id = cursor.fetchone()[0]
        connection.commit()
        print(f"Usuario insertado con ID: {user_id}")
        return user  # o puedes retornar user_id si prefieres devolver solo el ID
    except Exception as e:
        print("Error insertando usuario:", e)
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# src/controller/users.py
def update_user(firstname, surname, idnumber, mail):
    try:
        connection = conectar_a_base_datos()
        if connection is None:
            return False
        cursor = connection.cursor()
        update_query = """
        UPDATE users 
        SET firstname = %s, surname = %s, mail = %s
        WHERE idnumber = %s;
        """
        cursor.execute(update_query, (firstname, surname, mail, idnumber))
        connection.commit()
        if cursor.rowcount > 0:
            print("Usuario actualizado exitosamente.")
            return True
        else:
            print("Usuario no encontrado.")
            return False
    except Exception as e:
        print("Error actualizando usuario:", e)
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def delete_user(idnumber):
    try:
        connection = conectar_a_base_datos()
        if connection is None:
            return False  # Retorna False si la conexión falla
        cursor = connection.cursor()
        delete_query = "DELETE FROM users WHERE idnumber = %s;"
        cursor.execute(delete_query, (idnumber,))
        connection.commit()
        if cursor.rowcount > 0:
            print("Usuario eliminado exitosamente.")
            return True  # Retorna True si el usuario fue eliminado
        else:
            print("Usuario no encontrado.")
            return False  # Retorna False si el usuario no fue encontrado
    except Exception as e:
        print("Error eliminando usuario:", e)
        return False  # Retorna False si hubo un error
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def search_user_by_id(idnumber):
    try:
        connection = conectar_a_base_datos()
        if connection is None:
            return None
        cursor = connection.cursor()
        search_query = "SELECT * FROM users WHERE idnumber = %s;"
        cursor.execute(search_query, (idnumber,))
        result = cursor.fetchone()
        if result:
            user = User(result[1], result[2], result[3], result[4])
            print(f"Usuario encontrado: {user.firstname} {user.surname}, ID: {user.idnumber}, Email: {user.mail}")
            return user
        else:
            print("Usuario no encontrado.")
            return None
    except Exception as e:
        print("Error buscando usuario:", e)
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def search_user_by_name(firstname, surname):
    try:
        connection = conectar_a_base_datos()
        if connection is None:
            return None
        cursor = connection.cursor()
        search_query = "SELECT * FROM users WHERE firstname = %s AND surname = %s;"
        cursor.execute(search_query, (firstname, surname))
        result = cursor.fetchone()
        if result:
            user = User(result[1], result[2], result[3], result[4])
            print(f"Usuario encontrado: {user.firstname} {user.surname}, ID: {user.idnumber}, Email: {user.mail}")
            return user
        else:
            print("Usuario no encontrado.")
            return None
    except Exception as e:
        print("Error buscando usuario:", e)
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Función para pedir los datos por consola
def pedir_datos_usuario():
    firstname = input("Ingresa el nombre: ")
    surname = input("Ingresa el apellido: ")
    idnumber = input("Ingresa el número de identificación: ")
    mail = input("Ingresa el correo electrónico: ")
    
    # Crear una instancia de la clase User con los datos proporcionados
    usuario_nuevo = User(firstname, surname, idnumber, mail)
    
    # Mostrar el usuario creado
    print(f"Usuario creado: {usuario_nuevo.firstname} {usuario_nuevo.surname}, ID: {usuario_nuevo.idnumber}, Email: {usuario_nuevo.mail}")
    
    return usuario_nuevo

# Crear la tabla de usuarios al cargar el módulo
crear_tabla_users()
