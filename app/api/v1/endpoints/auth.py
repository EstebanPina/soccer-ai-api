from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import LoginDto, AuthResponseDto, RefreshTokenResponseDto
from app.schemas.user import CreateUserDto, UserResponse
from app.services.user import UserService
from app.services.auth import AuthService
from app.core.database import get_db
from app.guards.jwt_guard import get_current_user
from app.guards.refresh_jwt_guard import get_refresh_token

router = APIRouter()

@router.get("/health", response_model=dict)
async def checkhealth():
    return {"status": "ok"}

@router.post("/register", response_model=UserResponse)
async def register_user(dto: CreateUserDto, db: AsyncSession = Depends(get_db)):
    """
    Register a new user.
    """
    user_service = UserService(db)
    return await user_service.create_user(dto)


@router.post("/login", response_model=AuthResponseDto)
async def login_user(dto: LoginDto, db: AsyncSession = Depends(get_db)):
    """
    Authenticate a user and return access and refresh tokens.
    """
    auth_service = AuthService(UserService(db), db)
    return await auth_service.login(dto)


@router.post("/refresh", response_model=RefreshTokenResponseDto)
async def refresh_token(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_refresh_token)):
    """
    Refresh the user's tokens.
    """
    auth_service = AuthService(UserService(db), db)
    return await auth_service.refresh_token(current_user)
