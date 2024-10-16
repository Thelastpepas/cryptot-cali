from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64

def encrypt_message(message, key):
    """Encrypts a message using AES in CBC mode with a provided key."""
    valid_lengths = [16, 24, 32]
    if len(key) not in valid_lengths:
        raise ValueError("Invalid key length. Key must be 16, 24, or 32 bytes long.")

    iv = os.urandom(16)  # Generate a random initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Apply padding to the message
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    encrypted_message = iv + encryptor.update(padded_data) + encryptor.finalize()

    # Return the encrypted message in base64
    return base64.b64encode(encrypted_message).decode('utf-8')

def decrypt_message(encrypted_message_b64, key):
    """Decrypts an encrypted message using AES in CBC mode with the same key."""
    # Decode the encrypted message from base64
    encrypted_message = base64.b64decode(encrypted_message_b64)

    iv = encrypted_message[:16]  # Extract the IV
    actual_encrypted_message = encrypted_message[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded_message = decryptor.update(actual_encrypted_message) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()

    return decrypted_message.decode()

def format_output(data, format_type):
    """Converts data into the specified format."""
    if format_type == 'Base64':
        return base64.b64encode(data).decode('utf-8')
    elif format_type == 'Hexadecimal':
        return data.hex()
    elif format_type == 'Binary' or format_type == 'Binario':  # Acepta ambos
        return ''.join(format(byte, '08b') for byte in data)
    elif format_type == 'Decimal':
        return ' '.join(str(byte) for byte in data)
    elif format_type == 'Octal':
        return ' '.join(format(byte, 'o') for byte in data)
    else:
        raise ValueError("Invalid format type.")

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

            # Encrypt
            encrypted_message = encrypt_message(message, key)
            print(f'Encrypted Message (Base64): {encrypted_message}')  # Display the encrypted message in Base64
            
            # Convert encrypted message to bytes for formatting
            encrypted_message_bytes = base64.b64decode(encrypted_message)
            
            # Select the output format
            format_type = input("Select the output format (Base64, Hexadecimal, Binary, Decimal, Octal): ")
            
            # Format the encrypted message as requested
            formatted_message = format_output(encrypted_message_bytes, format_type)
            print(f'Encrypted Message ({format_type}): {formatted_message}')  # Display in the requested format
            
            # Show the key in base64 for later use
            print(f'Key used (base64): {base64.b64encode(key).decode("utf-8")}')

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

            # Ensure that the encrypted message is in base64 format
            try:
                # Try to decode as base64 to validate
                encrypted_message = base64.b64decode(encrypted_message)
            except Exception as e:
                print(f"Error decoding the encrypted message: {str(e)}")
                continue

            # Decrypt
            try:
                decrypted_message = decrypt_message(base64.b64encode(encrypted_message).decode('utf-8'), key)
                print(f'Decrypted Message: {decrypted_message}')
            except Exception as e:
                print(f'Error decrypting: {str(e)}')

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()

