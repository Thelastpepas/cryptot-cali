
#test/test_crypto.py
import sys
import os
import unittest
from base64 import b64decode, b64encode

# Añadir el directorio raíz a PYTHONPATH para importar el módulo encrypt
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar las funciones a probar del módulo de encriptación
from src.model.encrypt import encrypt_message, decrypt_message, format_output

class TestCryptoMethods(unittest.TestCase):
    
    def setUp(self):
        # Establecer datos de prueba y claves válidas de diferentes longitudes
        self.message = "Este es un mensaje de prueba."
        self.valid_key_16 = os.urandom(16)  # Clave de 16 bytes
        self.valid_key_24 = os.urandom(24)  # Clave de 24 bytes
        self.valid_key_32 = os.urandom(32)  # Clave de 32 bytes
        self.invalid_key = os.urandom(8)    # Longitud de clave inválida (8 bytes)

    def test_encrypt_valid_key_length_16(self):
        encrypted = encrypt_message(self.message, self.valid_key_16)
        self.assertTrue(encrypted)  # Asegurarse de que la encriptación produzca un resultado

    def test_encrypt_valid_key_length_24(self):
        encrypted = encrypt_message(self.message, self.valid_key_24)
        self.assertTrue(encrypted)  # Asegurarse de que la encriptación produzca un resultado

    def test_encrypt_valid_key_length_32(self):
        encrypted = encrypt_message(self.message, self.valid_key_32)
        self.assertTrue(encrypted)  # Asegurarse de que la encriptación produzca un resultado

    def test_decrypt_valid_key_length_16(self):
        encrypted = encrypt_message(self.message, self.valid_key_16)
        decrypted = decrypt_message(encrypted, self.valid_key_16)
        self.assertEqual(decrypted, self.message)  # Verificar si el mensaje desencriptado coincide con el original

    def test_decrypt_valid_key_length_24(self):
        encrypted = encrypt_message(self.message, self.valid_key_24)
        decrypted = decrypt_message(encrypted, self.valid_key_24)
        self.assertEqual(decrypted, self.message)  # Verificar si el mensaje desencriptado coincide con el original

    def test_decrypt_valid_key_length_32(self):
        encrypted = encrypt_message(self.message, self.valid_key_32)
        decrypted = decrypt_message(encrypted, self.valid_key_32)
        self.assertEqual(decrypted, self.message)  # Verificar si el mensaje desencriptado coincide con el original

    def test_invalid_key_length(self):
        with self.assertRaises(ValueError):
            encrypt_message(self.message, self.invalid_key)  # Se espera un ValueError

    def test_decrypt_with_invalid_key(self):
        encrypted = encrypt_message(self.message, self.valid_key_16)
        with self.assertRaises(ValueError):
            decrypt_message(encrypted, self.invalid_key)  # Se espera un ValueError

    def test_format_output_base64(self):
        data = b"data to format"
        formatted = format_output(data, "1")  # Usar "1" para Base64
        self.assertEqual(formatted, b64encode(data).decode('utf-8'))  # Verificar si el formato es correcto

    def test_format_output_hexadecimal(self):
        data = b"data to format"
        formatted = format_output(data, "2")  # Usar "2" para Hexadecimal
        self.assertEqual(formatted, data.hex())  # Verificar si el formato es correcto

    def test_format_output_binario(self):
        data = b"\x01\x02"
        formatted = format_output(data, "3")  # Usar "3" para Binario
        self.assertEqual(formatted, '00000001' + '00000010')  # Verificar si el formato es correcto

    def test_format_output_decimal(self):
        data = b"\x01\x02\x03"
        formatted = format_output(data, "4")  # Usar "4" para Decimal
        self.assertEqual(formatted, '1 2 3')  # Verificar si el formato es correcto

    def test_format_output_octal(self):
        data = b"\x01\x02\x03"
        formatted = format_output(data, "5")  # Usar "5" para Octal
        self.assertEqual(formatted, '1 2 3')  # Verificar si el formato es correcto

    def test_format_output_invalid(self):
        with self.assertRaises(ValueError):
            format_output(b"data", "invalid")  # Se espera un ValueError

    def test_decrypt_invalid_base64(self):
        invalid_base64_bytes = b"invalid_base64"
        with self.assertRaises(ValueError):
            decrypt_message(invalid_base64_bytes, self.valid_key_16)  # Se espera un ValueError

    def test_encrypt_empty_message(self):
        encrypted = encrypt_message("", self.valid_key_16)
        self.assertTrue(encrypted)  # Asegurarse de que la encriptación produzca un resultado

    def test_decrypt_empty_message(self):
        encrypted = encrypt_message("", self.valid_key_16)
        decrypted = decrypt_message(encrypted, self.valid_key_16)
        self.assertEqual(decrypted, "")  # Verificar si el mensaje desencriptado sigue siendo vacío

    def test_encrypt_special_characters(self):
        special_message = "!@#$%^&*()_+"
        encrypted = encrypt_message(special_message, self.valid_key_16)
        self.assertTrue(encrypted)  # Asegurarse de que la encriptación produzca un resultado

    def test_decrypt_special_characters(self):
        special_message = "!@#$%^&*()_+"
        encrypted = encrypt_message(special_message, self.valid_key_16)
        decrypted = decrypt_message(encrypted, self.valid_key_16)
        self.assertEqual(decrypted, special_message)  # Verificar si el mensaje desencriptado coincide con el original

    def test_encrypt_long_message(self):
        long_message = "A" * 1000  # Mensaje largo
        encrypted = encrypt_message(long_message, self.valid_key_32)
        self.assertTrue(encrypted)  # Asegurarse de que la encriptación produzca un resultado

    def test_decrypt_long_message(self):
        long_message = "A" * 1000  # Mensaje largo
        encrypted = encrypt_message(long_message, self.valid_key_32)
        decrypted = decrypt_message(encrypted, self.valid_key_32)
        self.assertEqual(decrypted, long_message)  # Verificar si el mensaje desencriptado coincide con el original

if __name__ == "__main__":
    unittest.main()  # Ejecutar todas las pruebas
