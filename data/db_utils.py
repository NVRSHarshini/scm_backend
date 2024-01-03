
#db_util.py containing all the helper fuctions 
from datetime import datetime, timedelta
from typing import Annotated, Optional, Union
from bson import ObjectId
from fastapi import HTTPException
from jose import JWTError, jwt
from data.db import user_collection,login_collection,ship_collection,user_cltn,db

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.models.model import TokenData, User



# def convert_to_json(obj):
#     if isinstance(obj, ObjectId):
#         return str(obj)
#     if isinstance(obj, list):
#         return [convert_to_json(item) for item in obj]
#     if isinstance(obj, dict):
#         return {key: convert_to_json(value) for key, value in obj.items()}
#     return obj

# async def read_users():
#     users = []
#     async for user in user_collection.find({}):
#         users.append(convert_to_json(user))
#     return users
# async def read_shipment():
#     users = []
#     async for user in ship_collection.find({}):
#         users.append(convert_to_json(user))
#     return users
# async def authenticate_user(email: str, password: str):
#     user = await login_collection.find_one({"email": email, "password": password})
#     return user

# async def read_user(user_id):
#     user = await user_collection.find_one({"_id": ObjectId(user_id)})
#     if user:
#         return convert_to_json(user)
#     raise HTTPException(status_code=404, detail="User not found")

# async def login_user(email, password):
#     user = await login_collection.find_one({"email": email, "password": password})
#     if user:
#         return True
#         # return convert_to_json(user)
#     # return None
#     return await read_users()

# def ResponseModel(data, message):
#     return {
#         "data": [data],
#         "code": 200,
#         "message": message,
#     }
# def login_helper(user) -> dict:
#     return {
#         "name": user.get("name", ""),
#         "email": user.get("email", ""),
#         "password": user.get("password", ""),
#         "phone": user.get("phone", "")
#     }

# async def add_user(user_data: dict) -> dict:
#     user = await login_collection.insert_one(user_data)
#     new_user = await login_collection.find_one({"_id": user.inserted_id})
#     return login_helper(new_user)
# print("I'm database util.py, and next is...")


#..................auth...................

from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = '4f1feeca525de4cdb064656007da3edac7895a87ff0ea865693300fb8b6e8f9c'  # should be kept secret
JWT_REFRESH_SECRET_KEY = '4f1feeca525de4cdb064656007da3edac7895a87ff0ea865693300fb8b6e8f9c'   # should be kept secret


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)
def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt
# Existing imports and code...

async def authenticate_user_by_email(email: str, password: str):
    user = await user_cltn.find_one({"email": email})
    if not user or not verify_password(password, user.get('hashed_password')):
        return None
    return user
