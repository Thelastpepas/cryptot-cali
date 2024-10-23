from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import pyperclip

class CryptoApp(App):
    def build(self):
        # Cambia el color de fondo a azul claro
        Window.clearcolor = (0.68, 0.85, 0.90, 1)

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Sección de Encriptación
        self.layout.add_widget(Label(text='--- ENCRYPTION ---', size_hint_y=None, height=40))

        self.message_input = TextInput(hint_text='Enter the message to encrypt', multiline=False, size_hint_y=None, height=40)
        self.layout.add_widget(self.message_input)

        self.key_length_spinner = Spinner(
            text='16',
            values=('16', '24', '32'),
            size_hint=(None, None),
            size=(100, 40)
        )
        self.layout.add_widget(self.key_length_spinner)

        self.format_spinner = Spinner(
            text='Base64',
            values=('Base64', 'Binary'),
            size_hint=(None, None),
            size=(150, 40)
        )
        self.layout.add_widget(self.format_spinner)

        self.encrypt_button = Button(text='Encrypt', size_hint=(1, None), height=40)
        self.encrypt_button.bind(on_press=self.encrypt_message)
        self.layout.add_widget(self.encrypt_button)

        # Clave generada
        self.key_label = TextInput(hint_text='Generated Key: ', multiline=False, readonly=True, size_hint_y=None, height=40)
        self.layout.add_widget(self.key_label)

        # Mensaje encriptado
        self.encrypted_message_label = TextInput(hint_text='Encrypted Message: ', multiline=False, readonly=True, size_hint_y=None, height=40)
        self.layout.add_widget(self.encrypted_message_label)

        # Botón para copiar mensaje encriptado
        self.copy_encrypted_button = Button(text='Copy Encrypted Message', size_hint=(1, None), height=40)
        self.copy_encrypted_button.bind(on_press=self.copy_encrypted_message)
        self.layout.add_widget(self.copy_encrypted_button)

        # Sección de Desencriptación
        self.layout.add_widget(Label(text='--- DECRYPTION ---', size_hint_y=None, height=40))

        self.key_input = TextInput(hint_text='Enter the key in base64', multiline=False, size_hint_y=None, height=40)
        self.layout.add_widget(self.key_input)

        self.encrypted_message_input = TextInput(hint_text='Enter the encrypted message', multiline=False, size_hint_y=None, height=40)
        self.layout.add_widget(self.encrypted_message_input)

        self.decrypt_button = Button(text='Decrypt', size_hint=(1, None), height=40)
        self.decrypt_button.bind(on_press=self.decrypt_message)
        self.layout.add_widget(self.decrypt_button)

        # Resultado de la desencriptación
        self.decrypted_message_label = TextInput(hint_text='Decrypted Message: ', multiline=False, readonly=True, size_hint_y=None, height=40)
        self.layout.add_widget(self.decrypted_message_label)

        # Botón para copiar mensaje desencriptado
        self.copy_decrypted_button = Button(text='Copy Decrypted Message', size_hint=(1, None), height=40)
        self.copy_decrypted_button.bind(on_press=self.copy_decrypted_message)
        self.layout.add_widget(self.copy_decrypted_button)

        # Botón para borrar todo
        self.clear_button = Button(text='Clear All', size_hint=(1, None), height=40)
        self.clear_button.bind(on_press=self.clear_all)
        self.layout.add_widget(self.clear_button)

        return self.layout

    def encrypt_message(self, instance):
        message = self.message_input.text
        key_length = int(self.key_length_spinner.text)
        format_type = self.format_spinner.text

        if not message:
            self.encrypted_message_label.text = "Please enter a message."
            return

        key = os.urandom(key_length)
        encrypted_message = self.encrypt(message, key)

        # Formatear el mensaje encriptado según el formato seleccionado
        formatted_output = self.format_output(encrypted_message, format_type)
        key_b64 = base64.b64encode(key).decode('utf-8')

        self.encrypted_message_label.text = formatted_output
        self.key_label.text = f'Generated Key: {key_b64}'

    def decrypt_message(self, instance):
        encrypted_message_str = self.encrypted_message_input.text
        key_b64 = self.key_input.text
        key_length = int(self.key_length_spinner.text)

        if not encrypted_message_str or not key_b64:
            self.decrypted_message_label.text = "Please enter an encrypted message and a key."
            return

        try:
            # Convertir la cadena de entrada en formato de bytes
            encrypted_message = self.convert_input_format(encrypted_message_str)

            key = base64.b64decode(key_b64)
            if len(key) != key_length:
                self.decrypted_message_label.text = f"Error: Key must be exactly {key_length} bytes."
                return
        except (ValueError, base64.binascii.Error):
            self.decrypted_message_label.text = "Error: Invalid key. Ensure it is base64 encoded."
            return
        except Exception as e:
            self.decrypted_message_label.text = f"Error: {str(e)}"
            return

        try:
            decrypted_message = self.decrypt(encrypted_message, key)
            self.decrypted_message_label.text = decrypted_message
        except Exception as e:
            self.decrypted_message_label.text = f'Error decrypting: {str(e)}'

    def encrypt(self, message, key):
        valid_lengths = [16, 24, 32]
        if len(key) not in valid_lengths:
            raise ValueError("Invalid key length. Key must be 16, 24, or 32 bytes long.")

        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(message.encode()) + padder.finalize()
        encrypted_message = iv + encryptor.update(padded_data) + encryptor.finalize()

        return encrypted_message

    def decrypt(self, encrypted_message, key):
        iv = encrypted_message[:16]
        actual_encrypted_message = encrypted_message[16:]

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        decrypted_padded_message = decryptor.update(actual_encrypted_message) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()

        return decrypted_message.decode()

    def format_output(self, data, format_type):
        """Formatea la salida del mensaje encriptado según el tipo de formato especificado."""
        if format_type == "Base64":
            return base64.b64encode(data).decode('utf-8')
        elif format_type == "Binary":
            return ''.join(format(byte, '08b') for byte in data)
        else:
            raise ValueError(f"Unsupported format type: {format_type}")

    def convert_input_format(self, encrypted_message_str):
        """Convierte el mensaje encriptado a bytes dependiendo de su formato."""
        if self.format_spinner.text == "Base64":
            return base64.b64decode(encrypted_message_str)
        elif self.format_spinner.text == "Binary":
            # Convertir la cadena binaria en bytes
            return bytes(int(encrypted_message_str[i:i + 8], 2) for i in range(0, len(encrypted_message_str), 8))
        else:
            raise ValueError("Unsupported format type for input.")

    def copy_encrypted_message(self, instance):
        encrypted_message = self.encrypted_message_label.text
        pyperclip.copy(encrypted_message)
        print("Copied to clipboard:", encrypted_message)

    def copy_decrypted_message(self, instance):
        decrypted_message = self.decrypted_message_label.text
        pyperclip.copy(decrypted_message)
        print("Copied to clipboard:", decrypted_message)

    def clear_all(self, instance):
        """Limpia todos los campos de texto."""
        self.message_input.text = ''
        self.key_label.text = 'Generated Key: '
        self.encrypted_message_label.text = 'Encrypted Message: '
        self.key_input.text = ''
        self.encrypted_message_input.text = ''
        self.decrypted_message_label.text = 'Decrypted Message: '



if __name__ == '__main__':
    CryptoApp().run()
