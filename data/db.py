# db.py

import motor.motor_asyncio
from fastapi import HTTPException

MONGO_DETAILS = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.students
user_collection = database.get_collection("user")
login_collection=database.get_collection("Login")
ship_collection = database.get_collection("crtShip")
#...............auth...............
db=client.scm
user_cltn=db.get_collection("user")

print("I'm database db.py, and next is...")
