from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from bson import ObjectId
from services.user_service import create_user, get_user_by_id, authenticate_user

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    user_interests: List[str] = []
    user_difficulties: List[str] = []
    currentTopicID: Optional[str] = None

@app.post('/users', response_model=UserCreate)
def add_user(user: UserCreate):
    created_user = create_user(
        username=user.username,
        email=user.email,
        password=user.password,
        user_interests=user.user_interests,
        user_difficulties=user.user_difficulties,
        currentTopicID=user.currentTopicID
    )
    return created_user.to_dict()

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    user_interests: List[str] = []
    user_difficulties: List[str] = []
    currentTopicID: Optional[str] = None

@app.get('/users/{user_id}', response_model=UserResponse)
def get_user(user_id: str):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=str(user['_id']),
        username=user['username'],
        email=user['email'],
        user_interests=user.get('user_interests', []),
        user_difficulties=user.get('user_difficulties', []),
        currentTopicID=user.get('currentTopicID')
    )

class UserLogin(BaseModel):
    email: str
    password: str

@app.post('/login')
def login(user_credentials: UserLogin):
    user = authenticate_user(user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #TODO creatin and returning a token
    return {"message": "Login succesful", "user_id": str(user._id)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
