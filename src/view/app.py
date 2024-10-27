import sys
sys.path.append("src")
import os

from src.model.encrypt import encrypt_message, format_output, base64, binary_to_bytes, decrypt_message
from src.controller.usercontroller import create_new_user, search_user, update_user_info, delete_existing_user

def encryption_menu():
    while True:
        print("\nEncryption Menu:")
        print("1. Encrypt message")
        print("2. Decrypt message")
        print("3. Return to main menu")

        choice = input("Enter your option (1, 2, or 3): ")

        if choice == '3':
            break

        if choice == '1':
            message = input("Enter the message you want to encrypt: ")
            key_length = int(input("Select the key length (16, 24, or 32): "))
            if key_length not in [16, 24, 32]:
                print("Invalid key length. Please try again.")
                continue
            
            key = os.urandom(key_length)

            print("\nSelect the output format:")
            print("1. Base64")
            print("2. Hexadecimal")
            print("3. Binary")
            print("4. Decimal")
            print("5. Octal")
            
            format_type = input("Enter the format number (1, 2, 3, 4, or 5): ")

            encrypted_message = encrypt_message(message, key)
            try:
                formatted_output = format_output(encrypted_message, format_type)
                print(f'Encrypted Message: {formatted_output}')
                print(f'Key used (base64): {base64.b64encode(key).decode("utf-8")}')
            except ValueError as ve:
                print(f"Error: {str(ve)}")

        elif choice == '2':
            encrypted_message = input("Enter the encrypted message: ")
            key_length = int(input("Select the key length (16, 24, or 32): "))
            if key_length not in [16, 24, 32]:
                print("Invalid key length. Please try again.")
                continue
            
            key_b64 = input(f"Enter the key of {key_length} bytes in base64: ")
            try:
                key = base64.b64decode(key_b64)
                if len(key) != key_length:
                    print(f"Error: The key must be exactly {key_length} bytes.")
                    continue
            except Exception as e:
                print(f"Error decoding the key: {str(e)}")
                continue

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

            try:
                decrypted_message = decrypt_message(encrypted_message, key)
                print(f'Decrypted Message: {decrypted_message}')
            except Exception as e:
                print(f'Error decrypting: {str(e)}')

def user_management_menu():
    while True:
        print("\nUser Management Menu:")
        print("1. Create new user")
        print("2. Search user")
        print("3. Update user information")
        print("4. Delete user")
        print("5. Return to main menu")

        choice = input("Enter your option (1, 2, 3, 4, or 5): ")

        if choice == '5':
            break
        elif choice == '1':
            create_new_user()
        elif choice == '2':
            search_user()
        elif choice == '3':
            update_user_info()
        elif choice == '4':
            delete_existing_user()
        else:
            print("Invalid option. Please try again.")

def main():
    print("\nWelcome to the AES encryption and User Management system.")
    while True:
        print("\nMain Menu:")
        print("1. Encryption Operations")
        print("2. User Management")
        print("3. Exit")

        choice = input("Enter your option (1, 2, or 3): ")

        if choice == '3':
            print("Exiting...")
            break
        elif choice == '1':
            encryption_menu()
        elif choice == '2':
            user_management_menu()
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()