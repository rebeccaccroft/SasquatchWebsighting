from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user


class Sighting:
    DB_NAME = 'sasquatch_schema'
    def __init__(self, data) -> None:
        self.id = data['id']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.date_seen = data['date_seen']
        self.num_sasquatches = data['num_sasquatches']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.reporter = None

    @classmethod
    def new_sighting(cls, data):
        query = 'INSERT INTO sightings (user_id, location, what_happened, date_seen, num_sasquatches) VALUES (%(user_id)s, %(location)s, %(what_happened)s, %(date_seen)s, %(num_sasquatches)s); '
        result = connectToMySQL(cls.DB_NAME).query_db(query, data)
        print(result)
        return result
    
    @classmethod
    def all_sightings(cls):
        query = 'SELECT * FROM sightings;'
        result = connectToMySQL(cls.DB_NAME).query_db(query)
        #print(result)
        return result
    
    @classmethod 
    def view_sighting(cls, data):
        query = 'SELECT * FROM sightings WHERE id = %(id)s;'
        result = connectToMySQL(cls.DB_NAME).query_db(query, data)
        print(result)
        return result

    @classmethod 
    def edit_sighting(cls, data):
        query = 'UPDATE sightings SET location = %(location)s, what_happened = %(what_happened)s, date_seen = %(date_seen)s, num_sasquatches = %(num_sasquatches)s WHERE id = %(id)s;'
        result = connectToMySQL(cls.DB_NAME).query_db(query, data)
        print(result)
        return result

    @classmethod
    def delete_sighting(cls, data):
        query = 'DELETE FROM sightings WHERE id = %(id)s;'
        return connectToMySQL(cls.DB_NAME).query_db(query, data)

    @classmethod
    def all_sightings_of_user(cls):
        query = 'SELECT * FROM sightings JOIN users ON users.id = sightings.user_id;'
        results = connectToMySQL(cls.DB_NAME).query_db(query)
        print(results)
        all_sightings = []

        for row in results:
            one_sighting = cls(row)
            user_data ={
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at':row ['users.created_at'],
                'updated_at':row ['users.updated_at']
            }
            user_object = user.User(user_data) 
            one_sighting.reporter = user_object
            all_sightings.append(one_sighting)
        return all_sightings