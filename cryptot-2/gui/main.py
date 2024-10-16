from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64

class CryptoApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Sección de Encriptación
        self.layout.add_widget(Label(text='--- ENCRIPTACIÓN ---', size_hint_y=None, height=40))
        self.message_input = TextInput(hint_text='Ingrese el mensaje a encriptar', multiline=False)
        self.layout.add_widget(self.message_input)

        self.key_length_spinner = Spinner(
            text='16',
            values=('16', '24', '32'),
            size_hint=(None, None),
            size=(100, 44)
        )
        self.layout.add_widget(self.key_length_spinner)

        self.format_spinner = Spinner(
            text='Base64',
            values=('Base64', 'Hexadecimal', 'Binario', 'Decimal', 'Octal'),
            size_hint=(None, None),
            size=(100, 44)
        )
        self.layout.add_widget(self.format_spinner)

        self.encrypt_button = Button(text='Encriptar', size_hint=(1, None), height=50)
        self.encrypt_button.bind(on_press=self.encrypt_message)
        self.layout.add_widget(self.encrypt_button)

        self.key_label = TextInput(hint_text='Clave generada: ', multiline=False, readonly=True)
        self.layout.add_widget(self.key_label)

        # Sección de Desencriptación
        self.layout.add_widget(Label(text='--- DESENCRIPTACIÓN ---', size_hint_y=None, height=40))
        self.key_input = TextInput(hint_text='Ingrese la clave en base64', multiline=False)
        self.layout.add_widget(self.key_input)

        self.encrypted_message_input = TextInput(hint_text='Ingrese el mensaje encriptado', multiline=False)
        self.layout.add_widget(self.encrypted_message_input)

        self.decrypt_button = Button(text='Desencriptar', size_hint=(1, None), height=50)
        self.decrypt_button.bind(on_press=self.decrypt_message)
        self.layout.add_widget(self.decrypt_button)

        # ScrollView para mostrar el resultado
        self.result_scroll = ScrollView(size_hint=(1, None), size=(400, 200))
        self.result_output = TextInput(hint_text='Resultado', multiline=True, readonly=True)
        self.result_scroll.add_widget(self.result_output)
        self.layout.add_widget(self.result_scroll)

        return self.layout

    def encrypt_message(self, instance):
        message = self.message_input.text
        key_length = int(self.key_length_spinner.text)

        if not message:
            self.result_output.text = "Por favor, ingrese un mensaje."
            return

        key = os.urandom(key_length)
        format_type = self.format_spinner.text
        encrypted_message = self.encrypt(message, key)
        formatted_message = self.format_output(base64.b64decode(encrypted_message), format_type)
        key_b64 = base64.b64encode(key).decode('utf-8')

        self.result_output.text = f'Mensaje Encriptado: {formatted_message}'
        self.key_label.text = f'Clave generada: {key_b64}'

    def decrypt_message(self, instance):
        encrypted_message = self.encrypted_message_input.text
        key_b64 = self.key_input.text
        key_length = int(self.key_length_spinner.text)

        if not encrypted_message or not key_b64:
            self.result_output.text = "Por favor, ingrese un mensaje encriptado y una clave."
            return

        try:
            key = base64.b64decode(key_b64)
            if len(key) != key_length:
                self.result_output.text = f"Error: La clave debe tener exactamente {key_length} bytes."
                return
        except Exception:
            self.result_output.text = "Error: La clave no es válida. Asegúrate de que sea base64."
            return

        format_type = self.format_spinner.text

        try:
            encrypted_message_bytes = self.process_encrypted_message(encrypted_message, format_type)
            decrypted_message = self.decrypt(encrypted_message_bytes, key)
            self.result_output.text = f'Mensaje Desencriptado: {decrypted_message}'
        except Exception as e:
            self.result_output.text = f'Error al desencriptar: {str(e)}'

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

        return base64.b64encode(encrypted_message).decode('utf-8')

    def decrypt(self, encrypted_message_b64, key):
        encrypted_message = base64.b64decode(encrypted_message_b64)

        iv = encrypted_message[:16]
        actual_encrypted_message = encrypted_message[16:]

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        decrypted_padded_message = decryptor.update(actual_encrypted_message) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()

        return decrypted_message.decode()

    def format_output(self, data, format_type):
        if format_type == 'Base64':
            return base64.b64encode(data).decode('utf-8')
        elif format_type == 'Hexadecimal':
            return data.hex()
        elif format_type == 'Binario':
            return ''.join(format(byte, '08b') for byte in data)
        elif format_type == 'Decimal':
            return ' '.join(str(byte) for byte in data)
        elif format_type == 'Octal':
            return ' '.join(format(byte, 'o') for byte in data)
        else:
            raise ValueError("Invalid format type.")

    def process_encrypted_message(self, encrypted_message, format_type):
        if format_type == 'Base64':
            return base64.b64decode(encrypted_message)
        elif format_type == 'Hexadecimal':
            return bytes.fromhex(encrypted_message)
        elif format_type == 'Binario':
            return bytes(int(encrypted_message[i:i + 8], 2) for i in range(0, len(encrypted_message), 8))
        elif format_type == 'Decimal':
            return bytes(int(byte) for byte in encrypted_message.split())
        elif format_type == 'Octal':
            return bytes(int(encrypted_message[i:i + 3], 8) for i in range(0, len(encrypted_message), 3))
        else:
            raise ValueError("Invalid format type.")

if __name__ == '__main__':
    CryptoApp().run()
