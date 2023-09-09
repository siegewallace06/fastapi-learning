from fastapi import FastAPI, Depends, status, Response, HTTPException
from pydantic import BaseModel
from typing import Optional, List
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


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,
                           body=request.body, published=request.published)

    # append the created_at and updated_at fields
    # new_blog.created_at = datetime.now()
    # new_blog.updated_at = datetime.now()

    try:
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Could not save the blog")

    return {
        "Message": "Blog created successfully",
        "Data": new_blog
    }


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {
        "Message": "Blog deleted successfully",
        "Deleted blog id": id
    }


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int,
                request: schemas.Blog,
                db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Unable to Update. Blog with id {id} not found")

    # Update the updated_at field
    blog.title = request.title
    blog.body = request.body
    blog.published = request.published
    blog.updated_at = datetime.now()

    # blog.update(request)

    db.commit()
    return {
        "Message": "Blog updated successfully",
        "New blog data": request
    }


@app.get("/blog")
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()

    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No blogs found, please create one")

    return {
        "Message": "Blogs retrieved successfully",
        "Data": blogs
    }


@app.get("/blog/{id}")
def get_blog_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # If the blog is not found
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {
        #     "Message": "Blog not found",
        #     "Data": None
        # }
    return {
        "Message": "Blog retrieved successfully",
        "Data": blog
    }


# , response_model=schemas.User)
@app.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name, email=request.email, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "Message": "User created successfully",
        "Data": new_user
    }
