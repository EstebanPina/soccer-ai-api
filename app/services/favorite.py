from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.favorite import Favorite
from typing import Dict, Any
from sqlalchemy.future import select

class FavoriteService:
  def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

  async def get_favorites(self, user_id:str="") -> Dict[str,Any]:
    # Verificar si el usuario ya existe
    statement_user_favorites = select(Favorite).where(Favorite.userId == user_id)
    user_favorites=await self.db_session.execute(statement_user_favorites)
    favorites = [fav.matchId for fav in user_favorites.scalars().all()]
    if len(favorites)==0:
        raise HTTPException(status_code=400, detail="You don't have any favorite")
    return {"favorites":favorites}