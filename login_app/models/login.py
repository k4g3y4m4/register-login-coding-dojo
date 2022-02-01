from login_app.configDB.mysqlconnection import connectToMySQL
from flask import flash
import re

class Login:
    def __init__(self,email,password):
        self.email = email
        self.password = password
    
    @classmethod
    def verify_login(cls,login):
        is_valid = True
        if len(login['email']) < 1:
            flash('Email cannot be blank', 'errorLogin')
            is_valid = False
    
        return is_valid

    @classmethod
    def search_by_email(cls,email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {
            'email': email
        }
        db = connectToMySQL('db_users')
        user = db.query_db(query, data)
        if len(user) > 0:
            return user[0]
        else:
            return False
    