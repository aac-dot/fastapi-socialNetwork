from datetime import datetime
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
    id: int
    email: EmailStr

class UserCreate(UserBase):
    password: str
    
class UserResponse(UserBase):
    created_at: datetime