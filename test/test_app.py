import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from app import app
from src.controller.users import insert_user, delete_user, User

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        # Inserta un usuario de prueba en la base de datos para usar en las pruebas
        self.test_user = User('Test', 'User', '12345', 'testuser@example.com')
        insert_user(self.test_user)

    def tearDown(self):
        # Elimina el usuario de prueba después de las pruebas
        delete_user(self.test_user.idnumber)
        delete_user('67890')  # Elimina cualquier usuario creado con este ID durante las pruebas

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bienvenido a la Aplicación de Gestión y Encriptación'.encode('utf-8'), response.data)

    def test_create_user_route(self):
        response = self.client.post('/users/create', data={
            'firstname': 'New',
            'surname': 'User',
            'idnumber': '67890',
            'mail': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Verifica redirección después de crear un usuario
        follow_response = self.client.get('/')
        self.assertIn(b'Usuario creado exitosamente', follow_response.data)

    def test_search_user_route(self):
        response = self.client.post('/users/search', data={
            'idnumber': '12345'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Nombre: Test', response.data)
        self.assertIn(b'Apellido: User', response.data)
        self.assertIn(b'ID: 12345', response.data)
        self.assertIn(b'Email: testuser@example.com', response.data)

    def test_update_user_route(self):
        response = self.client.post('/users/update', data={
            'idnumber': '12345',
            'firstname': 'Updated',
            'surname': 'User',
            'mail': 'updateduser@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Usuario actualizado exitosamente'.encode('utf-8'), response.data)

    def test_delete_user_route(self):
        response = self.client.post('/users/delete', data={
            'idnumber': '12345'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Usuario eliminado exitosamente'.encode('utf-8'), response.data)

    def test_user_not_found(self):
        response = self.client.post('/users/delete', data={
            'idnumber': '99999'  # Un ID que no existe
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Usuario no encontrado o error al eliminar'.encode('utf-8'), response.data)

    def test_invalid_key_length_encryption(self):
        response = self.client.post('/encryption', data={
            'message': 'Hello World',
            'key_length': '10',  # Longitud de clave inválida
            'format_type': '1'
        })
        self.assertEqual(response.status_code, 302)  # Redirigido debido a un flash de error



if __name__ == '__main__':
    unittest.main()
