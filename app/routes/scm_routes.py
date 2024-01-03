from datetime import timedelta
from fastapi import APIRouter, FastAPI, HTTPException, Depends,Header
from fastapi.security import OAuth2PasswordRequestForm
# from models.scm_model import User
from data.scm_dbutils import get_current_user, get_user_by_email, pwd_context,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,oauth2_scheme
from data.scm_db import Ship_collection, user_cltn
from data.db_utils import authenticate_user_by_email
from app.models.model import User
from ..models import scm_model  
router=APIRouter()


@router.get("/")
async def root():
    return {"message":"don't give up!"}


from fastapi import HTTPException

@router.post("/registration", response_model=scm_model.UserInDB)
async def create_user(user: scm_model.User):
    existing_user = await user_cltn.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already exists")
    
    hashed_password = pwd_context.hash(user.password)
    user_dict = user.dict()
    user_dict['hashed_password'] = hashed_password
    del user_dict['password']
    
    result = await user_cltn.insert_one(user_dict)
    user._id = str(result.inserted_id)
    return user


@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username'], "email": user['email'],"role": user['role']},  
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/profile", response_model=dict)
async def profile(email: str, current_user: dict = Depends(get_current_user)):
    # Check if the logged-in user's email matches the requested profile email
    if current_user["email"] != email:
        raise HTTPException(status_code=403, detail="You are not authorized to access this profile")

    user = await get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Convert ObjectId to string (if needed) before returning
    user["_id"] = str(user["_id"])
    return user


# Protected route to create a shipment
@router.post("/create_shipment/", response_model=scm_model.Shipment)
async def create_shipment(
    shipment: scm_model.Shipment,
    current_user: dict = Depends(get_current_user)
):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        # Your logic to verify user permissions and create a shipment
        # Example: Check if the current user has the necessary role or permissions
        
        # Simulate creating a shipment in the database for the example
        result = await Ship_collection.insert_one(shipment.model_dump())
        
        if result.inserted_id:
            return shipment
        else:
            raise HTTPException(status_code=500, detail="Failed to insert data into the database")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Protected route to get shipments by email
@router.get("/ship/{email}")
async def read_shipment(email: str, current_user: dict = Depends(get_current_user)):
    if current_user['role'] == 'admin':
        # Return all shipments if the user is an admin
        all_shipments = await Ship_collection.find().to_list(length=None)
        if all_shipments:
            for shipment in all_shipments:
                shipment["_id"] = str(shipment["_id"])
            return all_shipments
        raise HTTPException(status_code=404, detail="No shipments found")

    # For non-admin users, return shipments by their email
    user_shipments = await Ship_collection.find({"email": current_user['email']}).to_list(length=None)
    if user_shipments:
        for shipment in user_shipments:
            shipment["_id"] = str(shipment["_id"])
        return user_shipments
    
    raise HTTPException(status_code=404, detail="No shipments found for this email")
# @router.post("/login")
# async def login(user: User):
#     authenticated_user = await authenticate_user(user.email, user.password)
    
#     if authenticated_user:
#         access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#         access_token = create_access_token(data={"sub": authenticated_user.get('email')},expires_delta=access_token_expires)

#         return {"access_token": access_token, "token_type": "bearer"}
#     else:
#         raise HTTPException(status_code=401, detail="Invalid email or password")
    


    
# Example route to access protected data (requires authentication)
# @router.get("/protected")
# async def protected_route(current_user: dict = Depends(get_current_user)):
#     return {"message": "This is protected data!"}
#..........shipment..................
