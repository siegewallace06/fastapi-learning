from pydantic import BaseModel
from typing import Optional
from fastapi_utils.api_model import APIModel


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str

    blogs: list[Blog] = []

    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser
