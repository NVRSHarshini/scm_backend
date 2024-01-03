from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional

# Define some constants
SECRET_KEY = "your-secret-key"  # Replace with a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes

# Mock database model for a user
class User(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    hashed_password: str

# Mock function to get user from a database (replace this with actual user retrieval logic)
async def get_user(username: str):
    # Fetch user details based on the username from the database
    # Replace this with your actual logic to retrieve user details
    # For demonstration, returning hardcoded user data
    if username == "user":
        return User(id=1, username="user", email="user@example.com", hashed_password="$2b$12$T6hQ29x/saMJT8s4ZGezPuDW0aHh6k.7UfdzKQ.IgL4O")

# Create FastAPI instance
app = FastAPI()

# Hashing library for password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Token creation function
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Authenticate user function
async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

# Token endpoint to generate access token
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Example protected route
@app.get("/users/me")
async def read_user_me(current_user: User = Depends(oauth2_scheme)):
    return current_user
