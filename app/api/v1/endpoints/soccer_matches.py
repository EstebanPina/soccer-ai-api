from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.soccer_matches import SoccerMatchesService
from app.schemas.soccer_matches import SoccerMatchesCreate, SoccerMatchesRead
from app.core.database import get_db
from app.guards.jwt_guard import get_current_user # Dependencia para obtener el usuario del JWT

router = APIRouter()

@router.get("/health", response_model=dict)
async def checkhealth():
    return {"status": "ok"}
  
@router.post("/", response_model=SoccerMatchesRead)
async def get_match(dto:SoccerMatchesCreate, db: Session = Depends(get_db)):
    soccer_match_service = SoccerMatchesService(db)
    user = await soccer_match_service.find_by_id(dto)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
