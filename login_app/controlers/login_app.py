from flask import Flask, render_template, request, redirect, url_for, flash, session,app
from login_app.models.login import Login
from login_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)  # we are creating an object called bcrypt,

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', name=session['user'])
    else:
        return redirect(url_for('index'))

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))
    

@app.route('/login', methods=['POST'])
def login():
    # Get form information.
    print(request.form)
    user = {
        'email': request.form['Email'],
        'password': request.form['Password']
    }

    # Check if the user is valid.
    if Login.verify_login(user):
        #search user in database
        user_in_db = Login.search_by_email(user['email'])
        #check password
        if user_in_db:
            if bcrypt.check_password_hash(user_in_db['password'], user['password']):
                session['user'] = user_in_db['first_name'] + " " + user_in_db['last_name']
                print(session['user'])
                return redirect(url_for('dashboard'))
            else:
                flash("Password is incorrect", "errorLogin")
                return redirect(url_for('index'))
        else:
            flash("Email is incorrect", "errorLogin")
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

