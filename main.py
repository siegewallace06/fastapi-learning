from fastapi import FastAPI
import datetime

app = FastAPI()


@app.get("/")
def index():
    return {
        "data": "blog list"
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
def comments(id: int):
    # Fetch comments of Blog with id = id
    return {
        "data": {
            "comments": [
                id, id+1, id+2
            ]
        }
    }
