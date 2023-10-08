from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import user

from flask_app.models import house

from flask import flash

import pprint

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

DB = "smarthomes"

class Houses:
    def __init__(self, data):
        self.id = data['id']
        self.house_type = data['house_type']
        self.price = data['price']
        self.address = data['address']
        self.square_foot = data['square_foot']
        self.bed = data['bed']
        self.bath = data['bath']
        self.year_built = data['year_built']
        self.listing_date = data['listing_date']
        self.smartdevice = data['smartdevice']
        self.created_at = data["created_at"]
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None

    @classmethod
    def create_homes(cls,data):
        query = """INSERT INTO house (house_type,price,address,square_foot,bed,bath,year_built,listing_date,smartdevice,user_id) VALUES (%(house_type)s,%(price)s,%(address)s,%(square_foot)s,%(bed)s,%(bath)s,%(year_built)s,%(listing_date)s,%(smartdevice)s,%(user_id)s);"""
        results = connectToMySQL(DB).query_db(query, data)
        pprint.pprint(results,sort_dicts=False)
        return results
    
    @staticmethod
    def houses_validator(houses):
        print(houses)
        is_valid = True
        if not houses:
            flash("All Fields Required")
            is_valid =False
        if len(houses['house_type']) == 0:
                flash("Model must be not blank")
                is_valid = False
        if  len(houses['address']) == 0:
                flash("Address must not be blank")
                is_valid = False
        if len(houses['bed']) == 0:
                flash("Bed must not be blank")
                is_valid = False
        if len(houses['bath']) == 0:
                flash("Bath must not be blank")
                is_valid = False
        if len(houses['smartdevice']) == 0:
                flash("Smartdevice must not be blank")
                is_valid = False
        if  not houses['price']:
                flash("Your Price must be greater than 0")
                is_valid = False
        elif int(houses['price']) == 0:
                flash("Your Price must be greater than 0")
                is_valid = False
        if len(houses['year_built']) == 0:
                flash("Year built must not be blank")
                return False
      
        return is_valid
    
    @classmethod
    def get_all_houses(cls):
        query = """SELECT * FROM house LEFT JOIN user on user.id = house.user_id;"""
        results = connectToMySQL(DB).query_db(query)
        pprint.pprint(results,sort_dicts=False)
        all_houses = []
        for row_in_db in results:
            houses = cls(row_in_db)
            users_dictionary = {
                'id' :row_in_db['user_id'],
                'first_name' : row_in_db['first_name'],
                'last_name' : row_in_db['last_name'],
                'email' : row_in_db['email'],
                'password' : None,
                'created_at' : row_in_db['created_at'],
                'updated_at' : row_in_db['updated_at'],
            }
            houses.user = user.Users(users_dictionary)
            all_houses.append(houses)
        return all_houses
    
    @classmethod
    def get_one_house(cls, user_id):
        query  = "SELECT * FROM house LEFT JOIN user on user.id = house.user_id WHERE house.id = %(id)s;"
        data = {'id':user_id}
        results = connectToMySQL(DB).query_db(query, data)
        if not results:
            return None
        row = results[0]
        user_data = {
            'id': row['user_id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'password': None,
            'created_at': row['created_at'],
            'updated_at': row['updated_at'],
        }
        house = cls(row)
        house.user = user.Users(user_data)
        return house
    
    @classmethod
    def update_house(cls,data):
        query = """UPDATE house SET house_type = %(house_type)s, price = %(price)s, address = %(address)s, square_foot = %(square_foot)s, bed = %(bed)s, bath = %(bath)s, year_built = %(year_built)s, listing_date = %(listing_date)s, smartdevice = %(smartdevice)s  WHERE id = %(id)s;"""
        return connectToMySQL(DB).query_db(query, data)
        
    @classmethod
    def delete_house(cls, id):
        query  = "DELETE FROM house WHERE id = %(id)s;"
        data = {"id": id}
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def purchase_house(cls,data):
        query = """UPDATE house SET user_id = %(id)s WHERE (id = %(id)s);"""
        return connectToMySQL(DB).query_db(query, data)
        

