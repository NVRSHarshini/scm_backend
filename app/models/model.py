
#from bson import ObjectId
from bson import ObjectId
from pydantic import BaseModel
class LoginResponse(BaseModel):
    name: str
    email: str
    password:str
    phone: str

class Shipment(BaseModel):
    ShipmentNumber: str
    RouteDetails: str
    Device: str
    PPONumber: str
    NDCNumber: str
    SerialNumberOfGoods: str
    ContainerNumber: str
    Goods: str
    Date: str
    DeliveryNumber: str
    BatchId: str
    ShipmentDescription: str
# Pydantic model for JWT token payload
class TokenData(BaseModel):
    email: str | None = None
# Pydantic model for user registration

#.....................auth.................................
class User(BaseModel):
    email:str
    password:str
# Token model
class Token(BaseModel):
    access_token: str
    token_type: str