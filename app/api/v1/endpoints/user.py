from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.user import UserService
from app.schemas.user import UserResponse,FavoriteResponse, AddFavoriteDto
from app.core.database import get_db
from app.guards.jwt_guard import get_current_user # Dependencia para obtener el usuario del JWT

router = APIRouter()

@router.get("/health", response_model=dict)
async def checkhealth():
    return {"status": "ok"}
  
@router.get("/{id}", response_model=UserResponse)
async def get_user_profile(id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_service = UserService(db)
    print(user_service)
    user = await user_service.find_by_id(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/add_favorite/{matchId}", response_model=FavoriteResponse)
async def add_favorite_endpoint(matchId: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    print(current_user)
    user_service = UserService(db)
    user = await user_service.add_favorite(current_user,matchId)
    return user

@router.get("/remove_favorite/{matchId}", response_model=FavoriteResponse)
async def remove_favorite_endpoint(matchId: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_service = UserService(db)
    user = await user_service.remove_favorite(current_user,matchId)
    return user
