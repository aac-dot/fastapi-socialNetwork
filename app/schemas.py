from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    
class UserResponse(UserBase):
    created_at: datetime
    
class UserLogin(UserBase):
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None