from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.favorite import FavoriteService
from app.schemas.favorite import FavoriteResponse
from app.core.database import get_db
from app.guards.jwt_guard import get_current_user # Dependencia para obtener el usuario del JWT

router = APIRouter()
@router.get("/health", response_model=dict)
async def checkhealth():
    return {"status": "ok"}
  
@router.get("/", response_model=FavoriteResponse)
async def get_my_favorites(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    print(current_user)
    favorite_service = FavoriteService(db)
    favorites = await favorite_service.get_favorites(current_user["id"])
    if not favorites:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return favorites

@router.get("/{id}", response_model=FavoriteResponse)
async def get_user_favorites(id: str, db: Session = Depends(get_db)):
    favorite_service = FavoriteService(db)
    favorites = await favorite_service.get_favorites(id)
    if not favorites:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return favorites