import uvicorn

from fastapi import FastAPI,Request,HTTPException,Response
from app.routes import routes,new_routes
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
@app.get('/from main(app.get)')
def fastApi_object():
    return {'output':'message from fastapi-main'}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(new_routes.router)
#app.include_router(Login.html)


if __name__ == "__main__":
     uvicorn.run(app, host="127.0.0.1", port=8000)

# # main.py
# from pydantic import BaseModel
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# #from fastapi.middleware.cors import CORSMiddleware
# from bson import ObjectId

# from data.db_utils import read_users, read_user,login_user
# from app.models.model import LoginResponse,User

# app = FastAPI()


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
# from app.models import model

# origins = ["http://localhost:3000/","http:/localhost:3000/sign_in","http:/localhost:3000/LoginPage","http://127.0.0.1:8000/login"]
# origin = [
#     "*"
# ]

# # Configure CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins+origin,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

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

# @app.post("/login/")
# async def login(user: model.User):
#     # Use the login_user function to check authentication
#     authenticated_user = await db_utils.login_user(user.Email, user.Password)
#     #print(f"Received request: {user.Email}, {user.Password}")
    
#     if authenticated_user:
#         return {"message": "Login success"}
#     else:
#         raise HTTPException(status_code=401, detail="Login failed")

# #print("I'm routes.py, and next is...")
# # def get_route_url(request:Request,route_name: str):
# #     return request.url_for(route_name)


# # route_name = "login"
# # route_url = get_route_url(request=None,route_name=route_name)
# # print(f"URL for '{route_name}': {route_url}")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
# # Define the origins allowed to access the API (replace with your React app's URL)



# print("I'm main.py, and next is...")
