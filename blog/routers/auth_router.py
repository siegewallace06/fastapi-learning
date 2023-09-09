from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from .. import schemas, database, models, token
from ..hashing import Hash


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect password")

    access_token_expires = timedelta(minutes=15)
    access_token = token.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
