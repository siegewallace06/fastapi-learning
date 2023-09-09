from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..hashing import Hash

from .. import models, schemas


def create(request: schemas.User, db: Session):
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


def get_by_id(id: int, db: Session):
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
