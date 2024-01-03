from typing import Optional
import motor.motor_asyncio
from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from bson import ObjectId
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# MongoDB connection setup
MONGO_DETAILS = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
db = client.scm
user_cltn = db.get_collection("user")

# FastAPI app instance
app = FastAPI()

# JWT settings
SECRET_KEY = "your-secret-key"  # Replace this with your own secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Set expiration time for the token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: str
    password: str

class UserInDB(User):
    _id: Optional[str] = None

@app.post("/users/", response_model=UserInDB)
async def create_user(user: User):
    hashed_password = pwd_context.hash(user.password)
    user_dict = user.dict()
    user_dict['hashed_password'] = hashed_password
    del user_dict['password']
    result = await user_cltn.insert_one(user_dict)
    user._id = str(result.inserted_id)
    return user

# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to authenticate user
async def authenticate_user(username: str, password: str):
    user = await user_cltn.find_one({"username": username})
    if not user or not verify_password(password, user.get('hashed_password')):
        return False
    return user

# Function to get user details by username
async def get_user(username: str):
    user = await user_cltn.find_one({"username": username})
    if not user:
        return None
    return user

# Dependency to get the current user based on the token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token

# Example route for token generation using authentication
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Example route to access protected data (requires authentication)
@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "This is protected data!"}
