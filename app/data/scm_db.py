import motor.motor_asyncio
import os


from dotenv import load_dotenv

load_dotenv()


MONGO_DETAILS = os.getenv("MONGO_DETAILS")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
db = client.scm
user_cltn = db.get_collection("user")
Ship_collection=db.get_collection("shipment")
device_collection=db.get_collection("DeviceData")