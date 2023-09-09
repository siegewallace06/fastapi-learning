from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from . import schemas, models
from .database import engine, LocalSession

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog")
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,
                           body=request.body, published=request.published)

    # append the created_at and updated_at fields
    new_blog.created_at = datetime.now()
    new_blog.updated_at = datetime.now()

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return {
        "Message": "Blog created successfully",
        "Data": new_blog
    }
