from flask_app.config.mysqlconnection import connectToMySQL , DB
from flask_app.models.User import User
from flask import flash
from flask import request , session , redirect



class Thought:

    def __init__(self , data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def get_by_id(cls , data):
        query = "SELECT * FROM thoughts JOIN users ON thoughts.user_id = users.id WHERE thoughts.id = %(id)s;" 
        results = connectToMySQL(DB).query_db(query , data)

        thought = None
        if results:
            thought = cls(results[0])
            user_data = {
                'id': results[0]['users.id'],
                'first_name': results[0]['first_name'],
                'last_name': results[0]['last_name'],
                'email': results[0]['email'],
                'password': results[0]['password'],
                'created_at': results[0]['users.created_at'],
                'updated_at': results[0]['users.updated_at'],
            }
            thought.user = User(user_data)
        return thought
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM thoughts JOIN users ON thoughts.user_id = users.id;"
        results = connectToMySQL(DB).query_db(query)
        thoughts = []

        if results:
            for row in results:
                thought = cls(row)
                user_data = {
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                }
                thought.user = User(user_data)
                thoughts.append(thought)

        return thoughts
    @classmethod
    def like_thought(cls):
        if "count" not in session:
            session['count']=1
        else:
            session['count']+=1
        return session['count']
    @classmethod
    def unlike_thought(cls):
        if "count" not in session:
            session['count']=0
        else:
            if session['count']>0 :

                session['count']-=1
        return session['count']



    @classmethod 
    def create(cls , data):
        query = "INSERT INTO thoughts (content, user_id) VALUES(%(content)s,%(user_id)s);"
        result = connectToMySQL(DB).query_db(query , data)
        return result 

    
    @classmethod
    def update(cls, data):
        query = "UPDATE thoughts SET content=%(content)s WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)
        return result
    
    @classmethod 
    def delete(cls, data):
        query = "DELETE FROM thoughts WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query , data)
        return result
    
    @staticmethod
    def validate_thought(thought):
        is_valid = True
        if len(thought['content']) < 5:
            is_valid = False
            flash("Thought must be at least 5 characters!!!!!!!!","thought")
        return is_valid