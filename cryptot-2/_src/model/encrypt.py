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

# Función principal del sistema de encriptación
def main():
    print("Welcome to the AES encryption system.")
    
    while True:
        print("\nSelect an option:")
        print("1. Encrypt message")
        print("2. Decrypt message")
        print("3. Exit")

        choice = input("Enter your option (1, 2, or 3): ")

        if choice == '3':
            print("Exiting...")
            break

        if choice == '1':
            message = input("Enter the message you want to encrypt: ")
            key_length = int(input("Select the key length (16, 24, or 32): "))
            if key_length not in [16, 24, 32]:
                print("Invalid key length. Please try again.")
                continue
            
            # Generate a random key
            key = os.urandom(key_length)

            # Mostrar las opciones de formato en inglés y con números
            print("\nSelect the output format:")
            print("1. Base64")
            print("2. Hexadecimal")
            print("3. Binary")
            print("4. Decimal")
            print("5. Octal")
            
            format_type = input("Enter the format number (1, 2, 3, 4, or 5): ")

            # Encrypt
            encrypted_message = encrypt_message(message, key)
            try:
                formatted_output = format_output(encrypted_message, format_type)
                print(f'Encrypted Message: {formatted_output}')  # Display the encrypted message in the selected format
                # Show the key in base64 for later use
                print(f'Key used (base64): {base64.b64encode(key).decode("utf-8")}')
            except ValueError as ve:
                print(f"Error: {str(ve)}")

        elif choice == '2':
            encrypted_message = input("Enter the encrypted message: ")
            key_length = int(input("Select the key length (16, 24, or 32): "))
            if key_length not in [16, 24, 32]:
                print("Invalid key length. Please try again.")
                continue
            
            # Ask the user for the key in base64 format
            key_b64 = input(f"Enter the key of {key_length} bytes in base64: ")
            try:
                key = base64.b64decode(key_b64)
                if len(key) != key_length:
                    print(f"Error: The key must be exactly {key_length} bytes.")
                    continue
            except Exception as e:
                print(f"Error decoding the key: {str(e)}")
                continue

            # Ask for the format in which the encrypted message is provided
            print("\nSelect the format of the encrypted message:")
            print("1. Base64")
            print("2. Hexadecimal")
            print("3. Binary")
            print("4. Decimal")
            print("5. Octal")

            format_type = input("Enter the format number (1, 2, 3, 4, or 5): ")

            try:
                if format_type == "1":
                    encrypted_message = base64.b64decode(encrypted_message)
                elif format_type == "2":
                    encrypted_message = bytes.fromhex(encrypted_message)
                elif format_type == "3":
                    encrypted_message = binary_to_bytes(encrypted_message)
                elif format_type == "4":
                    encrypted_message = bytes(int(b) for b in encrypted_message.split())
                elif format_type == "5":
                    encrypted_message = bytes(int(b, 8) for b in encrypted_message.split())
                else:
                    raise ValueError("Invalid format selected")
            except Exception as e:
                print(f"Error processing the encrypted message: {str(e)}")
                continue

            # Decrypt
            try:
                decrypted_message = decrypt_message(encrypted_message, key)
                print(f'Decrypted Message: {decrypted_message}')
            except Exception as e:
                print(f'Error decrypting: {str(e)}')

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
