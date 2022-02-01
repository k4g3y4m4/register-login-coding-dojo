from login_app.configDB.mysqlconnection import connectToMySQL
from flask import flash
from login_app.models.login import Login
import re

EMAIL_REGEX =  re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')


class Register:
    def __init__(self, userid,Firstname, Lastname, Email, Password, Cpassword):
        self.userid = userid
        self.first_name = Firstname
        self.last_name = Lastname
        self.email = Email
        self.password = Password
        self.confirm_password = Cpassword
    
    @classmethod
    def add_user(cls,newUser):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        db = connectToMySQL('db_users')
        db.query_db(query, newUser)


    @staticmethod
    def verify_register(newUser):
        is_valid = True
        if len(newUser['first_name']) < 2:
            flash('First name must be at least 2 characters.', 'errorRegister')
            is_valid = False
        
        if len(newUser['last_name']) < 2:
            flash('Last name must be at least 2 characters.', 'errorRegister')
            is_valid = False
        
        if len(newUser['email']) < 1:
            flash('Email cannot be blank.', 'errorRegister')
            is_valid = False
        elif not EMAIL_REGEX.match(newUser['email']):
            flash('Invalid email address.', 'errorRegister')
            is_valid = False
        elif Login.search_by_email(newUser['email']):
            flash('Email already in use.', 'errorRegister')
            is_valid = False
        
        if not PASSWORD_REGEX.match(newUser['password']):
            flash('Password must be at least 8 characters, at least one uppercase letter and one number', 'errorRegister')
            is_valid = False
        
        if newUser['password'] != newUser['confirm_password']:
            flash('Passwords do not match.', 'errorRegister')
            is_valid = False

        return is_valid
        

