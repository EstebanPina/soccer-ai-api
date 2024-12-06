from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class UserBase(BaseModel):
    email: EmailStr
    name: str 
    class Config:
        from_attributes = True

class CreateUserDto(BaseModel):
    email: EmailStr
    name: str
    password: str
    class Config:
        from_attributes = True

class FavoriteDto(BaseModel):
    match_id: str
    username: str
    class Config:
        from_attributes = True
    
class UserResponse(UserBase):
    id: str
    email: EmailStr
    createdAt: datetime  
    
    class Config:
        from_attributes = True

class FavoriteResponse(UserBase):
    id: str
    email: EmailStr
    favorites: List[str]  
    name: str
    class Config:
        from_attributes = True
class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
class AddFavoriteDto(BaseModel):
    username: str
    match_id: str
    class Config:
        from_attributes = True