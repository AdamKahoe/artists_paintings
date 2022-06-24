from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Painting:
    db_name = 'paintings_schema'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.description = db_data['description']
        self.price = db_data['price']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.user = ""

    @classmethod
    def save(cls,data):
        query = "INSERT INTO paintings (title, description, price, user_id) VALUES (%(name)s,%(description)s,%(price)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM paintings;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_paintings = []
        for row in results:
            print(row['id'])
            all_paintings.append( cls(row) )
        return all_paintings

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM paintings JOIN users ON paintings.user_id = users.id WHERE paintings.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)

        paint = cls(results[0])
        # print(paint.title)
        # print(paint.user)
        paint.user = results[0]['first_name']
        return paint

    @classmethod
    def update(cls, data):
        query = "UPDATE paintings SET name=%(title)s, description=%(description)s, price=%(price)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM paintings WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    # # JOIN ATTEMPT

    @classmethod
    def get_user_paintings(cls,data):
        query = "SELECT users.first_name as sender, users2.first_name as reciever, paintings.* FROM users LEFT JOIN paintings ON users.id = messages.sender_id LEFT JOIN users as users2 ON users2.id = messages.reciever_id WHERE users2.id =  %(id)s"
        print(query)
        results = connectToMySQL(cls.db_name).query_db(query,data)
        paintings = []
        for painting in results:
            paint = cls(painting)
            # print(paint.title)
            # print(paint.user)
            paint.user = painting['first_name']
            paintings.append( paint )
        return painting

    @staticmethod
    def validate_painting(painting):
        is_valid = True
        if len(painting['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters","painting")
        if len(painting['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","painting")
        if len(painting['price']) < 1:
            is_valid = False
            flash("Price must be at least 1 character","painting")
        return is_valid