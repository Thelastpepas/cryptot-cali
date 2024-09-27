from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from Crypto.Cipher import AES
import os
import base64

class CryptoApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.message_input = TextInput(hint_text='Ingrese el mensaje aquí', multiline=False)
        self.key_spinner = Spinner(
            text='Seleccione tamaño de clave',
            values=('16', '32'),
            size_hint=(None, None),
            size=(200, 44)
        )

        self.action_spinner = Spinner(
            text='Seleccione acción',
            values=('Encriptar', 'Desencriptar'),
            size_hint=(None, None),
            size=(200, 44)
        )

        self.result_label = Label(text='Resultado:', size_hint_y=None, height=44)

        encrypt_button = Button(text='Ejecutar', on_press=self.process_message)

        self.layout.add_widget(self.message_input)
        self.layout.add_widget(self.key_spinner)
        self.layout.add_widget(self.action_spinner)
        self.layout.add_widget(encrypt_button)
        self.layout.add_widget(self.result_label)

        return self.layout

    def pad(self, s):
        return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)

    def unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

    def process_message(self, instance):
        action = self.action_spinner.text
        message = self.message_input.text
        key_size = int(self.key_spinner.text)

        # Validar el tamaño de la clave
        if key_size not in [16, 32]:
            self.result_label.text = "Seleccione un tamaño de clave válido (16 o 32)."
            return

        # Generar una clave basada en el tamaño seleccionado
        key = os.urandom(key_size)

        if action == 'Encriptar':
            cipher = AES.new(key, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(self.pad(message).encode())
            iv = base64.b64encode(cipher.iv).decode('utf-8')
            ct = base64.b64encode(ct_bytes).decode('utf-8')
            self.result_label.text = f'Encriptado: {iv}:{ct}'

        elif action == 'Desencriptar':
            try:
                # Verificar si el mensaje tiene el formato correcto
                if ':' not in message:
                    self.result_label.text = "Error: El formato debe ser 'IV:CT'."
                    return

                iv, ct = message.split(':')
                iv = base64.b64decode(iv)
                ct = base64.b64decode(ct)
                cipher = AES.new(key, AES.MODE_CBC, iv)
                decrypted_message = self.unpad(cipher.decrypt(ct)).decode()
                self.result_label.text = f'Desencriptado: {decrypted_message}'
            except Exception as e:
                self.result_label.text = f'Error al desencriptar: {str(e)}'

if __name__ == '__main__':
    CryptoApp().run()





