from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

import pprint

from flask_app.models import house

from flask_app.models import user

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

DB = "smarthomes"

class Users:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data["created_at"]
        self.updated_at = data['updated_at']
        self.house = []

    @classmethod
    def create_users(cls,data):
        query = "INSERT INTO user (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        results = connectToMySQL(DB).query_db(query, data)
        return results

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM user LEFT JOIN house on user.id = house.user_id;"
        results = connectToMySQL(DB).query_db(query)
        pprint.pprint
        all_users = []
        for row_in_db in results:
            users = cls(row_in_db)
            houses_data = {
                'id': row_in_db['id'],
                'house_type' : row_in_db['house_type'],
                'price' : row_in_db['price'],
                'address' : row_in_db['address'],
                'square_foot' : row_in_db['square_foot'],
                'bed' : row_in_db['bed'],
                'bath' : row_in_db['bath'],
                'year_built' : row_in_db['year_built'],
                'listing_date' : row_in_db['listing_date'],
                'smartdevice' : row_in_db['smartdevice'],
                'created_at': row_in_db["created_at"],
                'updated_at' : row_in_db['updated_at'],
                'user_id' : row_in_db['user_id'],
            }
        users.house = house.Houses(houses_data)
        all_users.append(users)
        return all_users

    @classmethod
    def get_user_by_email(cls, data):
        query  = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(DB).query_db(query, {'email': data})
        pprint.pprint(results,sort_dicts=False)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_one(cls, user_id):
        query  = "SELECT * FROM user WHERE id = %(id)s;"
        data = {'id':user_id}
        results = connectToMySQL(DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def user_validator(users):
        print(users)
        user_data = Users.get_user_by_email(users['email'])
        is_valid = True
        if user_data:
            flash("Invalid email/password", "register")
            is_valid = False
        else:
            if len(users['first_name']) < 3:
                flash("First name must be at least 3 characters", "register")
                is_valid = False
            if len(users['last_name']) < 3:
                flash("Last name must be at least 3 characters", "register")
                is_valid = False
            if not EMAIL_REGEX.match(users['email']):
                flash("Invalid email address!", "register")
                is_valid = False
            if len(users['password']) == 0:
                flash("Your password can not be blank", "register")
                is_valid = False
            elif len(users['password']) < 8:
                flash("Your password has to be greater than 8 characters", "register")
                is_valid = False
            if  users['password'] != users['confirm_password']:
                flash("Your password and confirm password do not match","register")
                is_valid = False

        return is_valid





