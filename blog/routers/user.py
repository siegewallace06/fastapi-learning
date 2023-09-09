from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from ..hashing import Hash

from .. import schemas, models, database

router = APIRouter(prefix="/user", tags=["users"])
get_db = database.get_db

# , response_model=schemas.ShowUser


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name, email=request.email, password=Hash.bcrypt(request.password))

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


@router.get("/{id}")
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
