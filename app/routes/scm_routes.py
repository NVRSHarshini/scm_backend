from datetime import timedelta
from typing import List,Optional
from fastapi import APIRouter,  HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
# from models.scm_model import User
from ..data.scm_dbutils import get_current_user, get_user_by_email, pwd_context,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES
from ..data.scm_db import Ship_collection, user_cltn,device_collection
from ..models.scm_model import DeviceData, User,UserInDB
from ..models import scm_model  
router=APIRouter()


@router.get("/")
async def root():
    return {"message":"don't give up!"}





@router.post("/registration", response_model=scm_model.UserInDB)
async def create_user(user: scm_model.User):
    existing_user = await user_cltn.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already exists")
    
    hashed_password = pwd_context.hash(user.password)
    user_dict = user.dict()
    user_dict['hashed_password'] = hashed_password
    del user_dict['password']
    
    user_cltn.insert_one(user_dict)
   
    return user


@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user['username'], "email": user['email'],"role": user['role']},  
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/profile/{email}", response_model=dict)
async def profile(email: str, current_user: dict = Depends(get_current_user)):
    # Check if the logged-in user's email matches the requested profile email
    print(email)
    
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
        print(current_user,",",shipment.email)
        if not current_user and current_user["email"]!=shipment.email:
            raise HTTPException(status_code=401, detail="Not authenticated")
      
        existing_shipment = await Ship_collection.find_one({"ShipmentNumber": shipment.ShipmentNumber})
        if existing_shipment:
            raise HTTPException(status_code=400, detail="Conflicting shipment number. Shipment number already exists.")
        
        result = await Ship_collection.insert_one(shipment.dict())
        
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

@router.get("/deviceData", response_model=List[DeviceData])
async def get_all_devices(current_user: dict = Depends(get_current_user)):
    try:
        if current_user.get("role") != 'admin' or not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        devices = await device_collection.find({}).to_list(length=None)
        return devices

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/deviceData/{DeviceId}", response_model=List[DeviceData])
async def get_devices(DeviceId: Optional[str] = None, current_user: dict = Depends(get_current_user)):
    try:
        if current_user.get("role") != 'admin' or not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        if DeviceId:
            device = await device_collection.find_one({"Device_ID": int(DeviceId)})
            if not device:
                raise HTTPException(status_code=404, detail="Device not found")
            return [device]

        # Return all devices when DeviceId is not provided
        devices = await device_collection.find({}).to_list(length=None)
        return devices

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))