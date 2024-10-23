# Message Encryption and Decryption
____________________________  
This project is a desktop application that allows encrypting and decrypting messages using symmetric cryptographic algorithms. It is developed in Python using the Kivy framework for the graphical user interface (GUI).

## Authors
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
- Install `pycryptodome`:

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

- `psycopg2`  
- `sys`  
- `os`  
- `cryptography`  
- `base64`  

## How to Run the Project
____________________________  

**Step 1:** Clone this repository to your local machine using:

```bash
git clone https://github.com/your-username/cryptot.git
```

1. Navigate to the project directory:

   ```bash
   cd cryptot
   ```

2. Go to the `src/view` folder:

   ```bash
   cd src/view
   ```

3. Run the `consola.py` script:

   ```bash
   python consola.py
   ```

4. Run the unit tests:

   ```bash
   python -m unittest test.controllertest
   ```

5. Run the console controller:

   ```bash
   python src/view/consolacontrolador.py
   ```

6. Run the `kivy_test.py` file from the `Gui` folder:

   ```bash
   python src/model/Gui/kivy_test.py
   ```

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

