from bson import ObjectId
from utils.security import hash_password

class User:
    def __init__(self, username, email, password, user_interests=None, user_difficulties=None, currentTopicID=None, _id=None):
        self._id = _id or ObjectId()
        self.username = username
        self.email = email
        self.password = hash_password(password)
        self.user_interests = user_interests if user_interests is not None else []
        self.user_difficulties = user_difficulties if user_difficulties is not None else []
        self.currentTopicID = currentTopicID

    def to_dict(self):
        return {
            '_id': self._id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'user_interests': self.user_interests,
            'user_difficulties': self.user_difficulties,
            'currentTopicID': self.currentTopicID
        }
    
    @staticmethod
    def from_dict(data):
        return User(
            username=data.get("username"),
            email=data.get('email'),
            password=data.get('password'),
            user_interests=data.get('user_interests', []),
            user_difficulties=data.get('user_difficulties', []),
            currentTopicID=data.get('currentTopicID'),
            _id=data.get('_id')
        )
