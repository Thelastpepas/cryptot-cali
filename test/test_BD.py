import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.controller.users import  crear_tabla_users, insert_user

from src.controller.users import conectar_a_base_datos 
from src.controller.usercontroller import *

class TestDatabaseApp(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.connection = conectar_a_base_datos()
        if cls.connection is None:
            raise RuntimeError("No se pudo establecer la conexión con la base de datos")
        crear_tabla_users()

    @classmethod
    def tearDownClass(cls):
        cursor = cls.connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS users;")
        cls.connection.commit()
        cursor.close()
        cls.connection.close()
    
    def test_insert_user(self):
        user = User(firstname='Jane', surname='Smith', idnumber='98765', mail='jane.smith@example.com')
        result = insert_user(user)
        self.assertIsNotNone(result, "El usuario debería haberse insertado correctamente")
    
    def test_search_user_by_id(self):
        user = User(firstname='John', surname='Doe', idnumber='12345', mail='john.doe@example.com')
        insert_user(user)
        result = search_user_by_id('12345')
        self.assertIsNotNone(result, "Debería encontrarse el usuario con ID 12345")

    def test_update_user(self):
        user = User(firstname='Alice', surname='Wonder', idnumber='11111', mail='alice.wonder@example.com')
        insert_user(user)
        updated_user = User(firstname='Alice', surname='Wonderland', idnumber='11111', mail='alice.wonderland@example.com')
        update_user(updated_user)
        result = search_user_by_id('11111')
        self.assertEqual(result.surname, 'Wonderland', "El apellido debería haberse actualizado a 'Wonderland'")

    def test_delete_user(self):
        user = User(firstname='Bob', surname='Builder', idnumber='22222', mail='bob.builder@example.com')
        insert_user(user)
        delete_user('22222')
        result = search_user_by_id('22222')
        self.assertIsNone(result, "El usuario debería haberse eliminado")

if __name__ == '__main__':
    unittest.main()