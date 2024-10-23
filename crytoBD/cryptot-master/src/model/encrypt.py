from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64

# Función para formatear la salida en varios formatos
def format_output(data, format_type):
    if format_type == "1":  # Base64
        return base64.b64encode(data).decode('utf-8')
    elif format_type == "2":  # Hexadecimal
        return data.hex()
    elif format_type == "3":  # Binary
        return ''.join(format(byte, '08b') for byte in data)
    elif format_type == "4":  # Decimal
        return ' '.join(str(byte) for byte in data)
    elif format_type == "5":  # Octal
        return ' '.join(format(byte, 'o') for byte in data)
    else:
        raise ValueError(f"Unsupported format type: {format_type}")

# Función para convertir una cadena binaria a bytes
def binary_to_bytes(binary_str):
    byte_array = bytearray()
    for i in range(0, len(binary_str), 8):
        byte_array.append(int(binary_str[i:i+8], 2))
    return bytes(byte_array)

# Función para añadir padding al mensaje (AES trabaja con bloques de tamaño fijo)
def pad_message(message):
    block_size = algorithms.AES.block_size  # Bloque de 16 bytes para AES
    padding = block_size - len(message) % block_size
    return message + (chr(padding) * padding).encode()

# Función para remover el padding del mensaje desencriptado
def unpad_message(message):
    padding = message[-1]
    return message[:-padding]

# Función para encriptar un mensaje usando AES en modo CBC
def encrypt_message(message, key):
    """Encrypts a message using AES in CBC mode with a provided key."""
    if len(key) not in [16, 24, 32]:
        raise ValueError("Invalid key length. Key must be 16, 24, or 32 bytes long.")

    iv = os.urandom(16)  # Genera un vector de inicialización aleatorio
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Aplicar padding al mensaje
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    encrypted_message = iv + encryptor.update(padded_data) + encryptor.finalize()

    return encrypted_message

# Función para desencriptar un mensaje
def decrypt_message(encrypted_message, key):
    """Decrypts an encrypted message using AES in CBC mode with the same key."""
    if len(key) not in [16, 24, 32]:
        raise ValueError("Invalid key length. Key must be 16, 24, or 32 bytes long.")
    
    iv = encrypted_message[:16]  # Extrae el vector de inicialización
    actual_encrypted_message = encrypted_message[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded_message = decryptor.update(actual_encrypted_message) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()

    return decrypted_message.decode()


