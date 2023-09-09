from fastapi import FastAPI

from . import models
from .database import engine, get_db
from .routers import blog, user

app = FastAPI(
    title="Basic CRUD with FastAPI and SQLAlchemy",
    description="This is a very basic CRUD app using FastAPI and SQLAlchemy"
)

app.include_router(blog.router)
app.include_router(user.router)

models.Base.metadata.create_all(bind=engine)
