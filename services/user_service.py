from models.user import User
from utils.database import get_db
from bson import ObjectId
from utils.security import verify_password

db = get_db()
users_collection = db['users']

def create_user(username: str, email: str, password: str, user_interests: None, user_difficulties: None, currentTopicID: None):
    user = User(username, email, password, user_interests, user_difficulties, currentTopicID)
    users_collection.insert_one(user.to_dict())
    return user

def get_user_by_id(user_id):
    user_data = users_collection.find_one({'_id': ObjectId(user_id)})
    if user_data:
        user_data['_id'] = str(user_data['_id'])
    return user_data

def authenticate_user(email: str, password: str):
    user_data = users_collection.find_one({'email': email})
    if not user_data:
        return None
    if not verify_password(password, user_data['password']):
        return None
    return User.from_dict(user_data)