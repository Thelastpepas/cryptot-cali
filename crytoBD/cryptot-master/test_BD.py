import unittest
from unittest.mock import patch, MagicMock
import psycopg2
import sys
sys.path.append("src")
from src.model.users import User, insert_user, search_user_by_id, update_user, delete_user, conectar_a_base_datos, crear_tabla_users,search_user_by_name
from src.controller.usercontroller import create_new_user, search_user, update_user_info, delete_existing_user



class TestUserFunctions(unittest.TestCase):

    @patch('src.model.users.insert_user')
    def test_create_new_user(self, mock_insert_user):
        # Simulamos una entrada de datos del usuario
        with patch('builtins.input', side_effect=['John', 'Doe', '12345', 'john@example.com']):
            create_new_user()
        
        # Verificamos que insert_user fue llamado con un objeto User correcto
        mock_insert_user.assert_called_once()
        user = mock_insert_user.call_args[0][0]
        self.assertEqual(user.firstname, 'John')
        self.assertEqual(user.surname, 'Doe')
        self.assertEqual(user.idnumber, '12345')
        self.assertEqual(user.mail, 'john@example.com')

    @patch('src.model.users.search_user_by_id')
    def test_search_user(self, mock_search_user_by_id):
        # Simulamos una entrada de datos del usuario
        with patch('builtins.input', side_effect=['12345']):
            search_user()
        
        # Verificamos que search_user_by_id fue llamado con el ID correcto
        mock_search_user_by_id.assert_called_once_with('12345')

    @patch('src.model.users.update_user')
    def test_update_user_info(self, mock_update_user):
        # Simulamos una entrada de datos del usuario
        with patch('builtins.input', side_effect=['12345', 'Jane', 'Smith', 'jane@example.com']):
            update_user_info()
        
        # Verificamos que update_user fue llamado con un objeto User correcto
        mock_update_user.assert_called_once()
        user = mock_update_user.call_args[0][0]
        self.assertEqual(user.firstname, 'Jane')
        self.assertEqual(user.surname, 'Smith')
        self.assertEqual(user.idnumber, '12345')
        self.assertEqual(user.mail, 'jane@example.com')

    @patch('src.model.users.delete_user')
    def test_delete_existing_user(self, mock_delete_user):
        # Simulamos una entrada de datos del usuario
        with patch('builtins.input', side_effect=['12345']):
            delete_existing_user()
        
        # Verificamos que delete_user fue llamado con el ID correcto
        mock_delete_user.assert_called_once_with('12345')


    @patch('psycopg2.connect')
    def test_conectar_a_base_datos_exito(self, mock_connect):
        # Simular una conexión exitosa
        mock_connect.return_value = MagicMock()
        conexion = conectar_a_base_datos()
        self.assertIsNotNone(conexion)
        print("Prueba de conexión exitosa ejecutada.")

    @patch('psycopg2.connect')
    def test_conectar_a_base_datos_falla(self, mock_connect):
        # Simular un error en la conexión
        mock_connect.side_effect = psycopg2.OperationalError
        conexion = conectar_a_base_datos()
        self.assertIsNone(conexion)
        print("Prueba de error en la conexión ejecutada.")

    @patch('psycopg2.connect')
    def test_crear_tabla_users(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        crear_tabla_users()
        mock_conn.cursor().execute.assert_called_once()
        print("Prueba de creación de tabla ejecutada.")

    @patch('psycopg2.connect')
    def test_insert_user(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        user = User("John", "Doe", "12345", "johndoe@example.com")
        insert_user(user)
        mock_conn.cursor().execute.assert_called_once()
        print("Prueba de inserción de usuario ejecutada.")

    @patch('psycopg2.connect')
    def test_update_user(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        user = User("John", "Doe", "12345", "johndoe@example.com")
        update_user(user)
        mock_conn.cursor().execute.assert_called_once()
        print("Prueba de actualización de usuario ejecutada.")

    @patch('psycopg2.connect')
    def test_delete_user(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        delete_user("12345")
        mock_conn.cursor().execute.assert_called_once_with("DELETE FROM users WHERE idnumber = %s;", ("12345",))
        print("Prueba de eliminación de usuario ejecutada.")

    @patch('psycopg2.connect')
    def test_search_user_by_id(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor().fetchone.return_value = ("1", "John", "Doe", "12345", "johndoe@example.com")
        search_user_by_id("12345")
        mock_conn.cursor().execute.assert_called_once_with("SELECT * FROM users WHERE idnumber = %s;", ("12345",))
        print("Prueba de búsqueda por ID ejecutada.")

    @patch('psycopg2.connect')
    def test_search_user_by_name(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor().fetchone.return_value = ("1", "John", "Doe", "12345", "johndoe@example.com")
        search_user_by_name("John", "Doe")
        mock_conn.cursor().execute.assert_called_once_with("SELECT * FROM users WHERE firstname = %s AND surname = %s;", ("John", "Doe"))
        print("Prueba de búsqueda por nombre ejecutada.")


if __name__ == '__main__':
    unittest.main()
