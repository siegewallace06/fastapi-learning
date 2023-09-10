from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from blog import models, schemas


def get_all(db: Session):
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


def get_by_id(id: int, db: Session):
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


def create(request: schemas.Blog, db: Session):
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


def update(id: int, request: schemas.Blog, db: Session):
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


def delete(id: int, db: Session):
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
