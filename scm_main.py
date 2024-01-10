from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.routes import  scm_routes
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(scm_routes.router)
if __name__ == "__main__":
     uvicorn.run(app, host="127.0.0.1", port=8000)