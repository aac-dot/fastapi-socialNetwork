from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException, Response, APIRouter
from typing import List

from ..schemas import UserCreate, UserResponse
from ..database import get_db
from .. import models
from ..utils import hash

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    user.password = hash(user.password)
    
    new_user = models.Users(**user.model_dump())
    
    db.add(new_user) 
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/users", response_model=List[UserResponse])
def get_user(db: Session = Depends(get_db)):
    
    users = db.query(models.Users).all()
    
    return users

@router.get("/users/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.Users).filter(models.Users.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with the id: {id} was not found")
    
    return user