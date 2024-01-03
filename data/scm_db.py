import motor.motor_asyncio

# MongoDB connection setup
MONGO_DETAILS = "mongodb+srv://hannytpt:DrZRsaq6jV76dCm@cluster0.meovrp4.mongodb.net/"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
db = client.scm
user_cltn = db.get_collection("user")
Ship_collection=db.get_collection("shipment")