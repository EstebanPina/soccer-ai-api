import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from app.services.sportsdb import SportsDbService
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/health", response_model=dict)
async def checkhealth():
  return {"status": "ok"}

@router.get("/league/{country}", response_model=dict)
async def get_league_matches(db: Session = Depends(get_db),country:str=""):
  sportsdb_service = SportsDbService(db)
  matches = await sportsdb_service.get_league_matches(country)
  if not matches:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matches not found")
  return matches

@router.get("/venues/{country}", response_model=dict)
async def get_all_cities(db: Session = Depends(get_db),country:str=""):
  sportsdb_service = SportsDbService(db)
  venues = await sportsdb_service.get_all_cities(country)
  if not venues:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venues not found")
  return venues