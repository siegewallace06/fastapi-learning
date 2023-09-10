from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from blog import schemas, models, database
from blog.repository import user_repository

router = APIRouter(prefix="/user", tags=["users"])
get_db = database.get_db


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user_repository.create(request, db)


@router.get("/{id}")
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return user_repository.get_by_id(id, db)
