from fastapi import FastAPI
import datetime

app = FastAPI()


@app.get("/")
def index():
    return {
        "message": "Hello, world!",
        "timestamp": datetime.datetime.now(),
    }


@app.get("/about")
def about():
    return {
        "data": "This is About Page"
    }
