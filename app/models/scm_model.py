from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    password: str
    phone: str
    role: str = 'user'
    _id: Optional[str] = None 


class UserInDB(BaseModel):
    username: str
    email: str
    password: str
    phone: str
    role: str = 'user'
    _id: Optional[str] = None


class Shipment(BaseModel):
    email: str
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
class DeviceData(BaseModel):
    Device_ID: int
    Battery_Level: float
    First_Sensor_temperature: float
    Route_From: str
    Route_To: str
  