# utils.py

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64

def encrypt_message(message, key):
    """Encripta un mensaje usando AES en modo CBC con una clave proporcionada."""
    valid_lengths = [16, 24, 32]
    if len(key) not in valid_lengths:
        raise ValueError("Invalid key length. Key must be 16, 24, or 32 bytes long.")

    iv = os.urandom(16)  # Genera un vector de inicialización aleatorio
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Aplicar padding al mensaje
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    encrypted_message = iv + encryptor.update(padded_data) + encryptor.finalize()

    # Devolver el mensaje encriptado y el IV en base64
    return base64.b64encode(encrypted_message).decode('utf-8')

def decrypt_message(encrypted_message_b64, key):
    """Desencripta un mensaje encriptado usando AES en modo CBC con la misma clave."""
    # Decodificar el mensaje encriptado de base64
    encrypted_message = base64.b64decode(encrypted_message_b64)

    iv = encrypted_message[:16]  # Extraer el IV
    actual_encrypted_message = encrypted_message[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded_message = decryptor.update(actual_encrypted_message) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()

    return decrypted_message.decode()
