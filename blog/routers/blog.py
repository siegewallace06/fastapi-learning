from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from sqlalchemy.orm import Session

from .. import oauth2
from .. import schemas, models, database
from ..repository import blog_repository

router = APIRouter(
    prefix="/blog",
    tags=["blogs"]
)
get_db = database.get_db


@router.get("/")
def get_all_blogs(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog_repository.get_all(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog_repository.create(request, db)


@router.get("/{id}")  # , response_model=schemas.ShowBlog
def get_blog_by_id(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog_repository.get_by_id(id, db)


@router.delete("/{id}")
def delete_blog(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog_repository.delete(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog_repository.update(id, request, db)
