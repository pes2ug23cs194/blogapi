from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    class Config:
        from_attributes = True



class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True
class PostUpdate(BaseModel):
    title: str
    content: str
    published: bool