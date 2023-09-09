from fastapi import FastAPI, Depends, status, Response, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime

from . import schemas, models, hashing
from .database import engine, LocalSession

app = FastAPI(
    title="Basic CRUD with FastAPI and SQLAlchemy",
    description="This is a very basic CRUD app using FastAPI and SQLAlchemy"
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,
                           body=request.body,
                           published=request.published,
                           user_id=1)

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


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
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


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
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
        "New blog data": blog
    }


@app.get("/blog", tags=["blogs"])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()

    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No blogs found, please create one")

    # Show who is the creator of the blog from the User table but get only the name and email from the list of blogs
    for blog in blogs:
        blog.creator = db.query(models.User).filter(
            models.User.id == blog.user_id).first()
        del blog.user_id
        del blog.creator.password
        del blog.creator.updated_at
        del blog.creator.created_at

    return {
        "Message": "Blogs retrieved successfully",
        "Data": blogs
    }


@app.get("/blog/{id}", tags=["blogs"])  # , response_model=schemas.ShowBlog
def get_blog_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # If the blog is not found
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    # Show who is the creator of the blog from the User table but get only the name and email
    blog.creator = db.query(models.User).filter(
        models.User.id == blog.user_id).first()
    del blog.user_id
    del blog.creator.password
    del blog.creator.updated_at
    del blog.creator.created_at

    return {
        "Message": "Blog retrieved successfully",
        "Data": blog
    }


# , response_model=schemas.ShowUser
@app.post("/user", status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))

    # Handle unique email constraint
    user = db.query(models.User).filter(
        models.User.email == request.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with email {request.email} already exists")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Remove the entire password field from the response so the response doesnt contain the password key
    del new_user.password

    return {
        "Message": "User created successfully",
        "Data": new_user
    }


@app.get("/user/{id}", tags=["users"])
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    # If the user is not found
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    # Delete the password field from the response
    del user.password
    del user.id

    return {
        "Message": "User retrieved successfully",
        "Data": user
    }
