from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

import datetime

app = FastAPI()


@app.get("/blog")
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {
            "data": f"{limit} published blogs from the db"
        }
    else:
        return {
            "data": f"{limit} blogs from the db"
        }


@app.get("/blog/unpublished")
def unpublished():
    # Fetch unpublished blogs
    return {
        "data": "all unpublished blogs"
    }


@app.get("/blog/{id}")
def show(id: int):
    # Fetch Blog Data with id = id
    return {
        "data": id
    }


@app.get("/blog/{id}/comments")
def comments(id: int, limit: int = 10):
    # Fetch comments of Blog with id = id
    return {
        "data": {
            "id": id,
            "limit_by": limit
        }
    }


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = False


@app.post("/blog")
def create_blog(request: Blog):
    # Create a new blog with 201 status code
    return {
        "message": "Blog created successfully",
        "data": request
    }


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=3000)
