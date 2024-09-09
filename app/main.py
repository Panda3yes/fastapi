from fastapi import FastAPI  # import the fastapi
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import Settings

# models.Base.metadata.create_all(bind=engine)  # commented out because using Alembic

origins = ["*"] # set domain that can access the API, "*" wildcard allows all domain to access the API

app = FastAPI()                 # create an instance of FastAPI assign to variable app

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")                   # @ is decorator and refers to app instance, get refers to the HTTP GET method and "/" refers to root
async def root():               # function root
    return {"message": "Welcome to Learn API with FastAPI!"}