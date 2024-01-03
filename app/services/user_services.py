from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional
app = FastAPI()
# Define a secret key to sign and verify JWT tokens
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
# MongoDB settings
MONGO_USERNAME = "your-username"
MONGO_PASSWORD = "your-password"
MONGO_DB = "your-database"
MONGO_COLLECTION = "users"
# MongoDB connection URL
MONGO_URL = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@your-cluster.mongodb.net/{MONGO_DB}?retryWrites=true&w=majority"
# Pydantic model for JWT token payload
class TokenData(BaseModel):
    email: str | None = None
# Pydantic model for user registration
class UserRegistration(BaseModel):
    username: str
    email: str
    password: str
# Pydantic model for user login
class UserLogin(BaseModel):
    email: str
    password: str
# Create an OAuth2 password bearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Function to create a JWT token
def create_jwt_token(data: dict) -> str:
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
# Function to decode a JWT token
def decode_jwt_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(**payload)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
# MongoDB connection
client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]
# Public endpoint for user registration
@app.post("/register")
async def register_user(user: UserRegistration):
    existing_user = await collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Hash the password before storing it in the database
    hashed_password = "hash_the_password_here"
    # Create a new user document
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
    }
    # Insert the new user into the database
    await collection.insert_one(new_user)
    return {"message": "User registered successfully"}
# Public endpoint for user login and token creation
@app.post("/token")
async def login_for_access_token(user: UserLogin):
    stored_user = await collection.find_one({"email": user.email})
    if not stored_user or stored_user["password"] != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_data = {"email": user.email}
    access_token = create_jwt_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}
# Private endpoint protected with token authentication
@app.get("/private-data")
async def get_private_data(token_data: TokenData = Depends(decode_jwt_token)):
    return {"message": "You have access to private data", "user_email": token_data.email}