# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import base64

from src.model.encrypt import encrypt_message, decrypt_message, format_output, binary_to_bytes
from src.controller.usercontroller import (
    create_new_user_web,
    search_user as search_user_controller,
    update_user as update_user_controller,
    delete_user as delete_user_controller
)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.urandom(24)  

@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el menú de gestión de usuarios
@app.route('/users', methods=['GET'])
def user_management():
    return render_template('users/user_management.html')

# Rutas para Gestión de Usuarios
@app.route('/users/create', methods=['GET', 'POST'])
@app.route('/users/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        firstname = request.form['firstname']
        surname = request.form['surname']
        idnumber = request.form['idnumber']
        mail = request.form['mail']
        
        user = create_new_user_web(firstname, surname, idnumber, mail)
        if user:
            flash('Usuario creado exitosamente.')
            return redirect(url_for('index'))  
        else:
            flash('Error al crear el usuario.')
    return render_template('users/create_user.html')


@app.route('/users/search', methods=['GET', 'POST'])
def search_user():
    user = None
    searched = False
    if request.method == 'POST':
        idnumber = request.form['idnumber']
        user = search_user_controller(idnumber)
        searched = True
    return render_template('users/search_user.html', user=user, searched=searched)

@app.route('/users/update', methods=['GET', 'POST'])
def update_user():
    message = None
    if request.method == 'POST':
        idnumber = request.form['idnumber']
        firstname = request.form.get('firstname', '')
        surname = request.form.get('surname', '')
        mail = request.form.get('mail', '')
        
        success = update_user_controller(firstname, surname, idnumber, mail)
        if success:
            message = 'Usuario actualizado exitosamente.'
        else:
            message = 'Usuario no encontrado o error al actualizar.'
    return render_template('users/update_user.html', message=message)

@app.route('/users/delete', methods=['GET', 'POST'])
def delete_user():
    message = None
    if request.method == 'POST':
        idnumber = request.form['idnumber']
        success = delete_user_controller(idnumber)
        if success:
            message = 'Usuario eliminado exitosamente.'
        else:
            message = 'Usuario no encontrado o error al eliminar.'
    return render_template('users/delete_user.html', message=message)

# Rutas para Encriptación
@app.route('/encryption', methods=['GET', 'POST'])
def encryption():
    if request.method == 'POST':
        message = request.form['message']
        key_length = int(request.form['key_length'])
        format_type = request.form['format_type']
        
        if key_length not in [16, 24, 32]:
            flash("Longitud de clave inválida.")
            return redirect(url_for('encryption'))
        
        key = os.urandom(key_length)
        encrypted_message = encrypt_message(message, key)
        
        try:
            formatted_output = format_output(encrypted_message, format_type)
            key_b64 = base64.b64encode(key).decode("utf-8")
            return render_template('encryption/encrypt.html', encrypted_message=formatted_output, key_b64=key_b64)
        except ValueError as ve:
            flash(str(ve))
            return redirect(url_for('encryption'))
    
    return render_template('encryption/encrypt.html')

@app.route('/encryption/decrypt', methods=['GET', 'POST'])
def decrypt():
    decrypted_message = None
    error = None
    if request.method == 'POST':
        encrypted_message_input = request.form['encrypted_message']
        key_length = int(request.form['key_length'])
        key_b64 = request.form['key_b64']
        format_type = request.form['format_type']
        
        if key_length not in [16, 24, 32]:
            error = "Longitud de clave inválida."
            return render_template('encryption/decrypt.html', error=error)
        
        try:
            key = base64.b64decode(key_b64)
            if len(key) != key_length:
                error = f"La clave debe tener exactamente {key_length} bytes."
                return render_template('encryption/decrypt.html', error=error)
        except Exception as e:
            error = f"Error decodificando la clave: {str(e)}"
            return render_template('encryption/decrypt.html', error=error)
        
        try:
            if format_type == "1":
                encrypted_message = base64.b64decode(encrypted_message_input)
            elif format_type == "2":
                encrypted_message = bytes.fromhex(encrypted_message_input)
            elif format_type == "3":
                encrypted_message = binary_to_bytes(encrypted_message_input)
            elif format_type == "4":
                encrypted_message = bytes(int(b) for b in encrypted_message_input.split())
            elif format_type == "5":
                encrypted_message = bytes(int(b, 8) for b in encrypted_message_input.split())
            else:
                raise ValueError("Formato inválido seleccionado.")
        except Exception as e:
            error = f"Error procesando el mensaje encriptado: {str(e)}"
            return render_template('encryption/decrypt.html', error=error)
        
        try:
            decrypted_message = decrypt_message(encrypted_message, key)
        except Exception as e:
            error = f"Error desencriptando: {str(e)}"
    
    return render_template('encryption/decrypt.html', decrypted_message=decrypted_message, error=error)

if __name__ == '__main__':
    app.run(debug=True)
