from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import UserLogin
from ..models import User
from ..utils import verify
from ..oauth2 import create_access_token

router = APIRouter(
    prefix="/login",
    tags=["authentication"]
)

@router.post("/")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    
    access_token = create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}