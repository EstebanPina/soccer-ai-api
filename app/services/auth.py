# app/services/auth.py
from datetime import timedelta
from fastapi import Depends, HTTPException
from app.services.user import UserService
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.schemas.auth import LoginDto
from sqlalchemy.ext.asyncio import AsyncSession
import time
class AuthService:
    def __init__(self, user_service: UserService, db_session: AsyncSession):
        self.user_service = user_service
        self.db_session = db_session
        self.EXPIRE_TIME = 15*60

    async def login(self, dto: LoginDto):
        user = await self.validate_user(dto)
        payload = {
            "id": user["id"],
            "username": user["email"],
            "sub": {
                "name": user["name"],
            },
        }
        return {
            "user": user,
            "backendTokens": {
                "accessToken": create_access_token(payload, expires_delta=timedelta(minutes=15)),
                "refreshToken": create_refresh_token(payload, expires_delta=timedelta(days=7)),
                "expiresIn": int(time.time()) + self.EXPIRE_TIME,
            },
        }

    async def validate_user(self, dto: LoginDto):
        user = await self.user_service.find_by_email(dto.email)
        print('user',user)
        if user and verify_password(dto.password, user.password):
            return {k: v for k, v in vars(user).items() if k != "password"}  # Excluir la contraseña
        raise HTTPException(status_code=401, detail="Invalid credentials or user not found")

    async def refresh_token(self, user: dict):
        payload = {
            "username": user["username"],
            "sub": user["sub"],
        }
        return {
            "accessToken": create_access_token(payload, expires_delta=timedelta(minutes=15)),
            "refreshToken": create_refresh_token(payload, expires_delta=timedelta(days=7)),
            "expiresIn":  int(time.time()) + self.EXPIRE_TIME,
        }
