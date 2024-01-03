from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    password: str
    phone:str
    role:str='user'
class UserInDB(User):
    _id: Optional[str] = None
    
class Shipment(BaseModel):
    email:str
    ShipmentNumber: int
    RouteDetails: str
    Device: str
    PPONumber: int
    NDCNumber: int
    SerialNumberOfGoods: str
    ContainerNumber: str
    Goods: str
    Date: str
    DeliveryNumber: str
    BatchId: str
    ShipmentDescription: str