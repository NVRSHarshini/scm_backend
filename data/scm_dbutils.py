
from fastapi import  HTTPException, Depends
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import  jwt
from fastapi.security import OAuth2PasswordBearer

from data.scm_db import user_cltn






# JWT settings
SECRET_KEY = "e7230b6b51bb520d4d3075a46fe1ce78"  # Replace this with your own secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Set expiration time for the token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
def decode_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:
        # Handle expired token
        return None
    except jwt.InvalidTokenError:
        # Handle invalid token
        return None
# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to authenticate user
async def authenticate_user(email: str, password: str):
    print("entered auth user")
    user = await user_cltn.find_one({"email": email})
    if not user or not verify_password(password, user.get('hashed_password')):
        return False
    return user

# Function to get user details by username
async def get_user(username: str):
    user = await user_cltn.find_one({"username": username})
    if not user:
        return None
    return user
# Function to get user details by email from MongoDB
async def get_user_by_email(email: str):
    user = await user_cltn.find_one({"email": email})
    return user
# Dependency to get the current user based on the token.crt code
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     print("entered get_curruser")
#     if not token:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return token

async def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    try:
        # Decode the token to extract user information
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Assuming the decoded token contains user information including 'email'
        return decoded_token  
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# # Function to create access token
# def create_access_token(data: dict, expires_delta: timedelta):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + expires_delta
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# # Function to verify password
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# # Function to authenticate user
# async def authenticate_user(email: str, password: str):
#     user = await user_cltn.find_one({"email": email})
#     if not user or not verify_password(password, user.get('hashed_password')):
#         return None  # Return None if authentication fails
#     return user  # Return the user object if authentication succeeds


# # Function to get user details by username
# async def get_user(username: str):
#     user = await user_cltn.find_one({"username": username})
#     if not user:
#         return None
#     return user

# # Dependency to get the current user based on the token
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     if not token:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return token