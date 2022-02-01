from flask import Flask, render_template, request, redirect, url_for, flash,app, session
from login_app.models.login import Login
from login_app.models.register import Register
from login_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)  # we are creating an object called bcrypt,


@app.route('/register', methods=['POST'])
def register():
    # Get form information.
    print(request.form)
    newUser = {
        'first_name': request.form['Firstname'],
        'last_name': request.form['Lastname'],
        'email': request.form['Email'],
        'password': request.form['Password'],
        'confirm_password': request.form['Cpassword']
    }

    # Check if the user is valid.
    if Register.verify_register(newUser):
        # encrypt password
        pw_hash = bcrypt.generate_password_hash(newUser['password'])
        newUser['password'] = pw_hash
        # Add user to database.
        Register.add_user(newUser)
        session['user'] = newUser['first_name'] + " " + newUser['last_name']
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('index'))
    
    