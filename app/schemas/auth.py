from pydantic import BaseModel, EmailStr
from typing import Dict, Optional,Any
from datetime import datetime

class LoginDto(BaseModel):
    email: EmailStr
    password: str
    class Config:
        from_attributes = True
        
class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: Optional[str]

    class Config:
        from_attributes = True
        
class AuthResponseDto(BaseModel):
    user: UserResponse  # Devuelve el usuario (email, nombre, etc.)
    backendTokens: Dict[str, Any]  # Contiene accessToken y refreshToken
    class Config:
        from_attributes = True
        
class RefreshTokenResponseDto(BaseModel):
    accessToken:str
    refreshToken:str
    expiresIn: int
    class Config:
        from_attributes = True
