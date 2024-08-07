from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import datetime
import os

load_dotenv()

MONGODB_URI = os.environ.get('MONGODB_URI')
if not MONGODB_URI:
    raise ValueError("MONGODB_URI not found in environment variables")

# client = MongoClient(MONGODB_URI)
# db = client['MainBase']
# users = db['users']

class user_manager:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client['MainBase']
        self.users = self.db['users']

    def insert_user(self, username, email, password, user_interests: [], user_difficulties: [], currentTopicID: None):
        # user_data: username, email, password_hashed, user_interests, user_difficulties, currentTopicID
        password_hashed = password #TODO add hashing
        try:
            result = self.users.insert_one({
                "username": username,
                "email": email,
                "password_hashed": password_hashed,
                "user_interests": user_interests,
                "user_difficulties": user_difficulties,
                "currentTopicID": currentTopicID
            })
            return user_id
        except Exception as e:
            print(f"An error occured while inserting user: {e}")
            return None
        finally:
            self.db.client.close()
            user_id = result.inserted_id

    def get_user(self, user_id):
        try:
            user_data = self.users.find_one({'_id': ObjectId(user_id)})
            return user_data
        except Exception as e:
            print(f"An error occured while retrieving user data: {e}")
            return None
        finally:
            self.db.client.close()

    def delete_user(self, user_id):
        try:
            result = self.users.delete_one({'_id': ObjectId(user_id)})
            return result.deleted_counts
        except Exception as e:
            print(f"An error occured while deleting user {e}")
        finally:
            self.db.client.close()
    
    def update_user(self, user_id, update_data):
        try:
            result = self.users.find_one_and_update(
                {'_id': ObjectId(user_id)},
                {'$set': update_data},
                return_document=True
            )
            return result
        except Exception as e:
            print(f"An erroc occured while updating user data: {e}")
        finally:
            self.db.client.close()
