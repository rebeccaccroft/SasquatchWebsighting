
from cgitb import reset
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import sighting
import re
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')   


class User:
    DB_NAME = 'sasquatch_schema'


    def __init__(self, data) :
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sightings = []

    @classmethod
    def create_user(cls, data):
            query_action = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
            insert_user = connectToMySQL(cls.DB_NAME).query_db(query_action, data)
            print(insert_user)
            return insert_user

    @classmethod
    def get_single_id(cls,data):
        query_action = 'SELECT * FROM users WHERE id = %(id)s;'
        find_user_by_id =  connectToMySQL(cls.DB_NAME).query_db(query_action, data)
        return cls(find_user_by_id[0])

    @classmethod
    def get_single_email(cls,data):
        query_action = 'SELECT * FROM users WHERE email = %(email)s;'
        results =  connectToMySQL(cls.DB_NAME).query_db(query_action, data)
        if len(results) == 0:
            return False
        return cls(results[0])


    @staticmethod
    def validate_register(request_form):
        is_valid = True
        if len(request_form['first_name']) <= 2:
            flash("Now Biff, first name must be at least 2 characters.", 'register')
            is_valid = False
        if len(request_form['last_name']) <= 2:
            flash("Now Biff, last name must be at least 2 characters.", 'register')
            is_valid = False
        if len(request_form['password_register']) <= 8:
            flash("Now Biff, this password must be at least 8 characters.", 'register')
            is_valid = False
        if len(request_form['password_confirm']) <= 8:
            flash("Now Biff, this password must be at least 8 characters.", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(request_form['email_register']): 
            flash("Now Biff, this is an invalid email address!", 'register')
            is_valid = False
        if request_form['password_register'] != request_form['password_confirm']:
            flash("Now Biff, these passwords do not match.", 'register')
            is_valid = False   
        flash("Great Scott!!! You've registered. Please login.", 'register')        
        return is_valid


    @staticmethod
    def validate_login(form_data):
        is_valid = True
        data = {
            'email': form_data['email']
        }
        user = User.get_single_email(data)
        if not user:
            flash('Now Biff, that login is invalid', 'login')
            is_valid = False
        elif not bcrypt.check_password_hash(user.password, form_data['password']):
            flash('Now Biff, that login is invalid', 'login')
            is_valid = False
        return is_valid
