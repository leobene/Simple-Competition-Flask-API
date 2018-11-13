import sqlite3
from db import db

class UserModel(object):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    #retrieve a user by username
    @classmethod
    def find_by_username(cls, username):
    	connection = sqlite3.connect('data.db')
    	cursor = connection.cursor()

    	query = "SELECT * FROM users WHERE username=?"
    	result = cursor.execute(query, (username,))
    	row = result.fetchone()
    	if row:
    		user = cls(*row)
    	else:
    		user = None

    	connection.close()
    	return user

    #retrieve a user by id
    @classmethod
    def find_by_id(cls, _id):
    	connection = sqlite3.connect('data.db')
    	cursor = connection.cursor()

    	query = "SELECT * FROM users WHERE id=?"
    	result = cursor.execute(query, (_id,))
    	row = result.fetchone()
    	if row:
    		user = cls(*row)
    	else:
    		user = None

    	connection.close()
    	return user
