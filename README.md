# Message Encryption and Decryption
____________________________  
This project is a desktop application that allows encrypting and decrypting messages using symmetric cryptographic algorithms. It is developed in Python using the Kivy framework for the graphical user interface (GUI).
## Previous Author
Santiago Cano Ocampo


## Current authors
____________________________  
- Anderson Monsalve Monsalve  
- Juan Felipe Ruiz Yepes  

## Description
____________________________  
The application allows users to encrypt and decrypt messages using a cryptographic key. The available algorithms for encryption are: Twofish, Serpent, AES (Rijndael), Camellia, Salsa20, ChaCha20, Blowfish, CAST5, Kuznyechik, RC4, DES, 3DES, Skipjack, Safer, and IDEA.

## Requirements
____________________________  
- Python 3.9.13  
- Kivy 2.3.0  
- Kivy dependencies: `kivy-deps.angle`, `kivy-deps.glew`, `kivy-deps.gstreamer`, `kivy-deps.sdl2`  

  ```bash
  pip install pycryptodome
  ```

- Install Kivy:

  ```bash
  pip install kivy
  ```

- Install `cryptography`:

  ```bash
  pip install cryptography
  ```

- Run the encryption module:

  ```bash
  python aes_encryption.py
  ```

## Installation
____________________________  
1. Clone this repository or download the source code.  
2. Make sure you have Python 3.9.13 installed on your system.  
3. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   ```

   For Windows:

   ```bash
   venv\Scripts\activate
   ```

   For Linux/Mac:

   ```bash
   source venv/bin/activate
   ```

## GUI Execution
____________________________  
1. Install `pycryptodome`:

   ```bash
   pip install pycryptodome
   ```

2. Run the main module:

   ```bash
   python main.py
   ```

## Database Setup
____________________________  
Install the following libraries for database operations:  
```bash
  pip install psycopg2 sys os base64
   ```
## How to Run the Project
____________________________  

To run this folder, you must first open
the test cases use test/tes_crypto.py
for the console it is in the main folder, and you put app.py
the database test is executed through the main folder test_BD.py
for the graphical interface it is in src/view/crypto.py
## Database Configuration
____________________________  
Update your database credentials in the `SecretConfig` folder:

```plaintext
PGHOST='******'
PGDATABASE='*****'
PGUSER='****'
PGPASSWORD='****'
```

## Execution
____________________________  
Once you've completed the previous steps, execute the `app.py` module either from the command line or using Visual Studio Code. If you are running it from the command line, it is recommended to place the project folder on your desktop, navigate to the directory using:

```bash
cd [project folder path]
```

una vez echo lo anterior ejecutar el modulo app.py 
ya sea desde el cmd o visual code 
si es desde el cmd se recomienda ponerla en escritorio y acceder a la carpeta con el comando cd 

