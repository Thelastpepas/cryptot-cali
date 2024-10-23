# Encriptación y Desencriptación de Mensajes
## ____________________________
Este proyecto es una aplicación de escritorio que permite encriptar y desencriptar mensajes utilizando algoritmos criptográficos simétricos. Está desarrollada en Python usando el framework Kivy para la interfaz gráfica de usuario (GUI).

## Autores
## ____________________________
-Anderson Monsalve Monsalve 

-Juan Felipe Ruiz Yepes
## Descripción
## ____________________________
La aplicación permite a los usuarios encriptar y desencriptar mensajes utilizando una clave criptográfica. Los algoritmos disponibles para la encriptación son: Twofish, Serpent, AES (Rijndael), Camellia, Salsa20, ChaCha20, Blowfish, CAST5, Kuznyechik, RC4, DES, 3DES, Skipjack, Safer e IDEA.

## Requisitos
## ____________________________
- Python 3.9.13
- Kivy 2.3.0
- Dependencias de Kivy: kivy-deps.angle, kivy-deps.glew, kivy-deps.gstreamer, kivy-deps.sdl2
- pip install pycryptodome
- Python 3.9.13
- pip install kivy 
- pip install cryptography
- python aes_encryption.py

## Instalación
## ____________________________
1. Clona este repositorio o descarga el código fuente.
2. Asegúrate de tener Python 3.9.13 instalado en tu sistema.
3. Crea un entorno virtual y activa el entorno:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
## ejecutar interfaz 
## ____________________________
1. instala la carpeta pip install pycryptodome
2. python main.py en la terminal o la consola

## base de datos
# instalar las siguientes librerias:
- psycopg2
- sys
- os
- ryptography
- base64
How to Run the Project
Step 1: Clone the repository
Clone this repository to your local machine using
 # 1. Clona el repositorio del proyecto:
git clone https://github.com/your-username/cryptot.git

# 2. Navega al directorio principal del proyecto:
cd cryptot

# 3. Accede a la carpeta src/view:
cd src/view

# 4. Ejecuta el archivo consola.py:
python consola.py

# 5. Ejecuta las pruebas unitarias (opcional):
python -m unittest test.controllertest

# 6. Ejecuta el controlador de la consola:
python src/view/consolacontrolador.py

# 7. Ejecuta el archivo kivy_test.py en la carpeta Gui:
python src/model/Gui/kivy_test.py


## coloca tus datos de tu base de datos en la carpeta secretconfig:
PGHOST='******
PGDATABASE=*****
PGUSER=****
PGPASSWORD=****

## ejecucion

una vez echo lo anterior ejecutar el modulo app.py 
ya sea desde el cmd o visual code 
si es desde el cmd se recomienda ponerla en escritorio y acceder a la carpeta con el comando cd 

