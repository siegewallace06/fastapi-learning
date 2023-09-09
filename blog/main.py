from fastapi import FastAPI

from . import models
from .database import engine, get_db
from .routers import blog, user, auth_router

app = FastAPI(
    title="Basic CRUD with FastAPI and SQLAlchemy",
    description="This is a very basic CRUD app using FastAPI and SQLAlchemy"
)
app.include_router(auth_router.router)
app.include_router(user.router)
app.include_router(blog.router)


models.Base.metadata.create_all(bind=engine)
