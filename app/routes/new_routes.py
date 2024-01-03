from datetime import datetime, timedelta
from typing import Annotated
from bson import ObjectId
from fastapi import Depends, FastAPI,APIRouter,HTTPException,Body,status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from data.db_utils import  ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM,  create_access_token, create_refresh_token, get_hashed_password, verify_password 
from data.db import login_collection,ship_collection,user_cltn


from app.models.model import  LoginResponse, TokenData, Shipment, User, Token
from fastapi.responses import JSONResponse
router=APIRouter()


@router.get("/")
def dashboard():
    return{"output":"from api"}

# @router.get("/users",response_description="Show all Users")
# async def list_all_users():
#        return await read_users()



# @router.post("/user/auth")
# async def login(email: str, password: str):
    
#     user_data = await authenticate_user(email, password)
    
    
#     if user_data:
#         user_data["_id"] = str(user_data["_id"])

#     return user_data

# @router.get("/user/{user_id}")
# async def read_user(user_id: str):
#     user = await login_collection.find_one({"_id": ObjectId(user_id)})
#     if user:
#         # Convert ObjectId to string before returning
#         user["_id"] = str(user["_id"])
#         return user
#     raise HTTPException(status_code=404, detail="User not found")


# @router.post("/register", response_description="User data added into the database")
# async def add_user_data(user: LoginResponse = Body(...)):
#     user_dict = jsonable_encoder(user)
    
#     # Make sure to use the correct function from your CRUD operations
#     new_user = await add_user(user_dict)
    
#     # Check if new_user is not None or handle accordingly based on your logic
#     if new_user:
#         return JSONResponse(content={"message": "User added successfully.", "data": new_user})
#     else:
#         return JSONResponse(content={"message": "Failed to add user."}, status_code=500)
# @router.post("/login")
# async def login(user: User):
#     # Use the login_user function to check authentication
#     authenticated_user = await login_user(user.Email, user.Password)
#     print(f"Received request: {user.Email}, {user.Password}")
    
#     if authenticated_user:
#         return{"message":"Login success"}
#         # return {"token": "your_token_here"}  # Replace with your token generation logic
#     else:
#         raise HTTPException(status_code=401, detail="Login failed")


# @router.post("/create_shipment/", response_model=Shipment)
# async def create_shipment(shipment: Shipment):
#     try:
#         result = await ship_collection.insert_one(shipment.model_dump())
#         if result.inserted_id:
#             return shipment
#         else:
#             raise HTTPException(status_code=500, detail="Failed to insert data into the database")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/ship/{shipment_number}")
# async def read_shipment(shipment_number: str):
#     # Find a document where the `ShipmentNumber` matches the provided string
#     Shipment = await ship_collection.find_one({"ShipmentNumber": shipment_number})
#     if Shipment:
#         # Convert ObjectId to string before returning (if needed)
#         Shipment["_id"] = str(Shipment["_id"])
#         return Shipment
#     raise HTTPException(status_code=404, detail="Shipment not found")




#............................auths.......................

from fastapi import FastAPI, status, HTTPException
from fastapi.responses import RedirectResponse
# from app.schemas import UserOut, UserAuth
# from replit import db

from uuid import uuid4

@router.post('/signup', summary="Create new user", response_model=User)
async def create_user(data: User):
    # querying database to check if user already exist
    user = user_cltn.get(data.email, None)
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = {
        'email': data.email,
        'password': get_hashed_password(data.password),
        'id': str(uuid4())
    }
    user_cltn[data.email] = user    # saving user to database
    return user
@router.post('/login', summary="Create access and refresh tokens for user", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_cltn.get(form_data.username, None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }