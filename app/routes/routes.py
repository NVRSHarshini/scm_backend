from fastapi import FastAPI
from fastapi import APIRouter,HTTPException
from data.db import login_collection
from app.models import model
# app= FastAPI()
from fastapi.templating import Jinja2Templates
TEMPLATES = Jinja2Templates(directory="templates")
router = APIRouter()

# @router.get("/")
# def home_page():
#     """Home Page"""

#     return TEMPLATES.TemplateResponse("home.html")

# @router.get("/signup")
# def home_page():
#     """Home Page"""

#     return TEMPLATES.TemplateResponse("homepage.html")
# @router.post("/login")
# async def login(user: model.User):
#     # Check if email and password match in the database
#     result = login_collection.find_one({"email": user.email, "password": user.password})
#     if result:
#         return {"success": True, "message": "Login successful"}
#     else:
#         raise HTTPException(status_code=401, detail="Invalid email or password")
# import sys
# import os
# from fastapi import FastAPI
# from fastapi.routing import APIRoute
# from fastapi import Request
# from starlette.datastructures import URL


# # Rest of your code

# # Get the directory of the current script (routes.py)
# current_directory = os.path.dirname(os.path.abspath(__file__))

# # Get the directory containing the "app" directory
# project_directory = os.path.dirname(current_directory)

# # Append the project directory to the Python path
# sys.path.append(project_directory)



# from fastapi import FastAPI, HTTPException
# from data import db_utils
# from models import model

# # from data.db_utils import User, login_user
# # from data.db_utils import read_user, read_users

# app = FastAPI()

# @app.get("/")
# def home():
#     return {"output": "Welcome home from FastAPI"}

# @app.get("/users")
# async def list_users():
#     return await db_utils.read_users()

# @app.get("/users/{user_id}")
# async def get_user(user_id: str):
#     return await db_utils.read_user(user_id)

# @app.post("/login")
# async def login(user: model.User):
#     # Use the login_user function to check authentication
#     authenticated_user = await db_utils.login_user(user.Email, user.Password)
#     #print(f"Received request: {user.Email}, {user.Password}")
    
#     if authenticated_user:
#         return {"message": "Login success"}
#     else:
#         raise HTTPException(status_code=401, detail="Login failed")

# print("I'm routes.py, and next is...")
# # def get_route_url(request:Request,route_name: str):
# #     return request.url_for(route_name)


# # route_name = "login"
# # route_url = get_route_url(request=None,route_name=route_name)
# # print(f"URL for '{route_name}': {route_url}")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)


#....before with route error: app not found.........
# from fastapi import FastAPI, HTTPException


# from app.data.db_utils import User,login_user
# from app.data.db_utils import login_user, read_user, read_users

# app = FastAPI()

# @app.get("/")
# def home():
#     return {"output": "Welcome home from fastapi"}

# @app.get("/users")
# async def list_users():
#     return await read_users()

# @app.get("/users/{user_id}")
# async def get_user(user_id: str):
#     return await read_user(user_id)



# @app.post("/login")
# async def login(user: User):
#     # Use the login_user function to check authentication
#     authenticated_user = await login_user(user.Email, user.Password)
#     print(f"Received request: {user.Email}, {user.Password}")
    
#     if authenticated_user:
#         return{"message":"Login success"}
#         # return {"token": "your_token_here"}  # Replace with your token generation logic
#     else:
#         raise HTTPException(status_code=401, detail="Login failed")
    
# print("I'm routes.py, and next is...")