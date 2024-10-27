import sys
sys.path.append("src")
import os
import unittest
from base64 import b64decode, b64encode

# Add the root directory to PYTHONPATH to import the encrypt module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the functions to test from the encryption module
from src.model.encrypt import encrypt_message, decrypt_message, format_output

class TestCryptoMethods(unittest.TestCase):
    
    def setUp(self):
        # Set up test data and valid keys of different lengths
        self.message = "This is a test message"
        self.valid_key_16 = os.urandom(16)  # 16 bytes key
        self.valid_key_24 = os.urandom(24)  # 24 bytes key
        self.valid_key_32 = os.urandom(32)  # 32 bytes key
        self.invalid_key = os.urandom(8)    # Invalid key length (8 bytes)
        self.format_type = "Base64"          # Default format type for testing

    def test_encrypt_valid_key_length_16(self):
        encrypted = encrypt_message(self.message, self.valid_key_16)
        self.assertTrue(encrypted)  # Ensure encryption produces a result

    def test_encrypt_valid_key_length_24(self):
        encrypted = encrypt_message(self.message, self.valid_key_24)
        self.assertTrue(encrypted)  # Ensure encryption produces a result

    def test_encrypt_valid_key_length_32(self):
        encrypted = encrypt_message(self.message, self.valid_key_32)
        self.assertTrue(encrypted)  # Ensure encryption produces a result

    def test_decrypt_valid_key_length_16(self):
        encrypted = encrypt_message(self.message, self.valid_key_16)
        decrypted = decrypt_message(encrypted, self.valid_key_16)
        self.assertEqual(decrypted, self.message)  # Check if decrypted message matches original

    def test_decrypt_valid_key_length_24(self):
        encrypted = encrypt_message(self.message, self.valid_key_24)
        decrypted = decrypt_message(encrypted, self.valid_key_24)
        self.assertEqual(decrypted, self.message)  # Check if decrypted message matches original

    def test_decrypt_valid_key_length_32(self):
        encrypted = encrypt_message(self.message, self.valid_key_32)
        decrypted = decrypt_message(encrypted, self.valid_key_32)
        self.assertEqual(decrypted, self.message)  # Check if decrypted message matches original

    def test_invalid_key_length(self):
        with self.assertRaises(ValueError):
            encrypt_message(self.message, self.invalid_key)  # Expecting a ValueError

    def test_decrypt_with_invalid_key(self):
        encrypted = encrypt_message(self.message, self.valid_key_16)
        with self.assertRaises(ValueError):
            decrypt_message(encrypted, self.invalid_key)  # Expecting a ValueError

    def test_format_output_base64(self):
        data = b"data to format"
        formatted = format_output(data, "Base64")
        self.assertEqual(formatted, b64encode(data).decode('utf-8'))  # Check if the formatting is correct

    def test_format_output_hexadecimal(self):
        data = b"data to format"
        formatted = format_output(data, "Hexadecimal")
        self.assertEqual(formatted, data.hex())  # Check if the formatting is correct

    def test_format_output_binario(self):
        data = b"\x01\x02"
        formatted = format_output(data, "Binario")
        self.assertEqual(formatted, '00000001' + '00000010')  # Check if the formatting is correct

    def test_format_output_decimal(self):
        data = b"\x01\x02\x03"
        formatted = format_output(data, "Decimal")
        self.assertEqual(formatted, '1 2 3')  # Check if the formatting is correct

    def test_format_output_octal(self):
        data = b"\x01\x02\x03"
        formatted = format_output(data, "Octal")
        self.assertEqual(formatted, '1 2 3')  # Check if the formatting is correct

    def test_decrypt_invalid_base64(self):
        # Test decryption with an invalid base64 string
        invalid_base64_bytes = b"invalid_base64"  # This should be a bytes object
        with self.assertRaises(ValueError):
            decrypt_message(invalid_base64_bytes, self.valid_key_16)  # Expecting a ValueError

    def test_encrypt_empty_message(self):
        encrypted = encrypt_message("", self.valid_key_16)
        self.assertTrue(encrypted)  # Ensure encryption produces a result

    def test_decrypt_empty_message(self):
        encrypted = encrypt_message("", self.valid_key_16)
        decrypted = decrypt_message(encrypted, self.valid_key_16)
        self.assertEqual(decrypted, "")  # Check if decrypted message is still empty

    def test_encrypt_special_characters(self):
        special_message = "!@#$%^&*()_+"
        encrypted = encrypt_message(special_message, self.valid_key_16)
        self.assertTrue(encrypted)  # Ensure encryption produces a result

    def test_decrypt_special_characters(self):
        special_message = "!@#$%^&*()_+"
        encrypted = encrypt_message(special_message, self.valid_key_16)
        decrypted = decrypt_message(encrypted, self.valid_key_16)
        self.assertEqual(decrypted, special_message)  # Check if decrypted message matches original

    def test_encrypt_long_message(self):
        long_message = "A" * 1000  
        encrypted = encrypt_message(long_message, self.valid_key_32)
        self.assertTrue(encrypted)  # Ensure encryption produces a result

    def test_decrypt_long_message(self):
        long_message = "A" * 1000  
        encrypted = encrypt_message(long_message, self.valid_key_32)
        decrypted = decrypt_message(encrypted, self.valid_key_32)
        self.assertEqual(decrypted, long_message)  # Check if decrypted message matches original

if __name__ == "__main__":
    unittest.main()  # Run all tests
