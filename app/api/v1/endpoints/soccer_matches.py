from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.soccer_matches import SoccerMatchesService
from app.schemas.soccer_matches import SoccerMatchesCreate, SoccerMatchesBase
from app.core.database import get_db
from app.guards.jwt_guard import get_current_user # Dependencia para obtener el usuario del JWT

router = APIRouter()

@router.get("/health", response_model=dict)
async def checkhealth():
    return {"status": "ok"}
  
@router.get("/{id}", response_model=SoccerMatchesBase)
async def get_user_profile(id: str, db: Session = Depends(get_db)):
    soccer_match_service = SoccerMatchesBase(db)
    user = await soccer_match_service.find_by_id(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post("/create", response_model=SoccerMatchesBase)
async def create_match(dto: SoccerMatchesCreate, db: Session = Depends(get_db)):
    soccer_match_service = SoccerMatchesService(db)
    match = await soccer_match_service.create_match(dto)
    return match
