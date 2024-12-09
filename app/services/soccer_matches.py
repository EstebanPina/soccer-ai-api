from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.soccer_matches import SoccerMatches
from app.models.venue import Venue
from app.schemas.soccer_matches import SoccerMatchesCreate, SoccerMatchesRead,SoccerMatchesFavorites
from app.schemas.OpenAi import OpenAiCreate
from app.services.open_ai import OpenAIService
from typing import Dict, Any
from sqlalchemy.future import select

class SoccerMatchesService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_match(self, dto: SoccerMatchesCreate) -> Dict[str, Any]:
        statement = select(SoccerMatches).where(SoccerMatches.id_sports_api == dto.id_sports_api)
        result=await self.db_session.execute(statement)
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Match is already registered")
        statement = select(Venue).where(Venue.id == dto.venueId)
        result=await self.db_session.execute(statement)
        venue_conditions=result.scalar_one_or_none()
        if not venue_conditions:
            raise HTTPException(status_code=400, detail="Venue is not registered")
        prediction_dto= OpenAiCreate(local_team=dto.local_team,visitor_team=dto.visitor_team,temperature=venue_conditions.temperature,weather=venue_conditions.weather,wind_speed=venue_conditions.wind_speed)
        openai_service = OpenAIService()
        prediction_ai = await openai_service.create_prediction(prediction_dto)
        new_match = SoccerMatches(**dto.dict(), view_count=1, prediction_ai=prediction_ai )
        self.db_session.add(new_match)
        await self.db_session.commit()
        await self.db_session.refresh(new_match)
        return new_match
      
    async def find_by_id(self, dto:SoccerMatchesCreate) -> Dict[str, Any]:
        statement = select(SoccerMatches).where(SoccerMatches.id_sports_api == dto.id_sports_api)
        result=await self.db_session.execute(statement)
        match=result.scalar_one_or_none()
        print(match)
        if match:
            match.view_count+=1
            await self.db_session.commit()
            return match
        return await self.create_match(dto)
    
    async def find_many(self, dto:SoccerMatchesFavorites) -> Dict[str, Any]:
        print(dto.favorites)
        statement = select(SoccerMatches).where(SoccerMatches.id_sports_api.in_(dto.favorites))
        result=await self.db_session.execute(statement)
        matches=result.scalars().all()
        matches_read=[SoccerMatchesRead.from_orm(match) for match in matches]
        if not matches:
            raise HTTPException(status_code=400, detail="Matches not found")
        return matches_read
