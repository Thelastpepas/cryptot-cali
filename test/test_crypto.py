import unittest
from crypto.encrypt import encrypt_message, decrypt_message


class TestCryptoMethods(unittest.TestCase):

    def test_encrypt_valid_key_length_16(self):
        key = b'sixteen_byte_key'
        message = 'Hello World!'
        encrypted = encrypt_message(message, key)
        self.assertIsNotNone(encrypted)

    def test_encrypt_valid_key_length_24(self):
        key = b'twenty_four_byte_key_123'
        message = 'Hello World!'
        encrypted = encrypt_message(message, key)
        self.assertIsNotNone(encrypted)

    def test_encrypt_valid_key_length_32(self):
        key = b'thirty_two_byte_key_12345678'
        message = 'Hello World!'
        encrypted = encrypt_message(message, key)
        self.assertIsNotNone(encrypted)

    def test_decrypt_valid_key_length_16(self):
        key = b'sixteen_byte_key'
        message = 'Hello World!'
        encrypted = encrypt_message(message, key)
        decrypted = decrypt_message(encrypted, key)
        self.assertEqual(decrypted, message)

    def test_decrypt_valid_key_length_24(self):
        key = b'twenty_four_byte_key_123'
        message = 'Hello World!'
        encrypted = encrypt_message(message, key)
        decrypted = decrypt_message(encrypted, key)
        self.assertEqual(decrypted, message)

    def test_decrypt_valid_key_length_32(self):
        key = b'thirty_two_byte_key_12345678'
        message = 'Hello World!'
        encrypted = encrypt_message(message, key)
        decrypted = decrypt_message(encrypted, key)
        self.assertEqual(decrypted, message)

    def test_encrypt_invalid_key_length(self):
        key = b'short_key'
        with self.assertRaises(ValueError):
            encrypt_message('Hello', key)

    def test_decrypt_invalid_key_length(self):
        key = b'short_key'
        encrypted = b'\x00' * 32  # Dummy encrypted data
        with self.assertRaises(ValueError):
            decrypt_message(encrypted, key)

    def test_encrypt_empty_message(self):
        key = b'sixteen_byte_key'
        message = ''
        encrypted = encrypt_message(message, key)
        self.assertIsNotNone(encrypted)

    def test_decrypt_empty_message(self):
        key = b'sixteen_byte_key'
        encrypted = encrypt_message('', key)
        decrypted = decrypt_message(encrypted, key)
        self.assertEqual(decrypted, '')

    def test_decrypt_with_wrong_key(self):
        key1 = b'sixteen_byte_key'
        key2 = b'another_key_1234'
        message = 'Hello World!'
        encrypted = encrypt_message(message, key1)
        with self.assertRaises(ValueError):
            decrypt_message(encrypted, key2)

    def test_encrypt_long_message(self):
        key = b'sixteen_byte_key'
        message = 'A' * 1000  # Long message
        encrypted = encrypt_message(message, key)
        self.assertIsNotNone(encrypted)

    def test_decrypt_long_message(self):
        key = b'sixteen_byte_key'
        message = 'A' * 1000
        encrypted = encrypt_message(message, key)
        decrypted = decrypt_message(encrypted, key)
        self.assertEqual(decrypted, message)

    def test_encrypt_special_characters(self):
        key = b'sixteen_byte_key'
        message = '!@#$%^&*()_+'
        encrypted = encrypt_message(message, key)
        self.assertIsNotNone(encrypted)

    def test_decrypt_special_characters(self):
        key = b'sixteen_byte_key'
        message = '!@#$%^&*()_+'
        encrypted = encrypt_message(message, key)
        decrypted = decrypt_message(encrypted, key)
        self.assertEqual(decrypted, message)

    def test_encrypt_numerical_message(self):
        key = b'sixteen_byte_key'
        message = '1234567890'
        encrypted = encrypt_message(message, key)
        self.assertIsNotNone(encrypted)

    def test_decrypt_numerical_message(self):
        key = b'sixteen_byte_key'
        message = '1234567890'
        encrypted = encrypt_message(message, key)
        decrypted = decrypt_message(encrypted, key)
        self.assertEqual(decrypted, message)

    def test_decrypt_with_invalid_data(self):
        key = b'sixteen_byte_key'
        invalid_data = b'not_encrypted_data'
        with self.assertRaises(ValueError):
            decrypt_message(invalid_data, key)

    def test_encrypt_unicode_message(self):
        key = b'sixteen_byte_key'
        message = 'こんにちは'  # Japanese for "Hello"
        encrypted = encrypt_message(message, key)
        self.assertIsNotNone(encrypted)

    def test_decrypt_unicode_message(self):
        key = b'sixteen_byte_key'
        message = 'こんにちは'
        encrypted = encrypt_message(message, key)
        decrypted = decrypt_message(encrypted, key)
        self.assertEqual(decrypted, message)

    def test_decrypt_short_encrypted_data(self):
        key = b'sixteen_byte_key'
        short_encrypted = b'\x00' * 10  # Dummy short data
        with self.assertRaises(ValueError):
            decrypt_message(short_encrypted, key)


if __name__ == '__main__':
    unittest.main()


