from pydantic import BaseModel
from typing import List,Any

class SoccerMatchesFavorites(BaseModel):
    favorites: List
    class Config:
        from_attributes = True
class SoccerMatchesBase(BaseModel):
    id_sports_api: str
    local_team: str
    visitor_team: str
    local_team_img: str
    visitor_team_img: str
    finished: bool
    venueId: str
    class Config:
        from_attributes = True

class SoccerMatchesCreate(SoccerMatchesBase):
    pass

class SoccerMatchesRead(SoccerMatchesBase):
    id: str
    prediction_ai: str
    view_count: int
    class Config:
        from_attributes = True
class SoccerMatchesReadMany(BaseModel):
    data: List[Any]
    class Config:
        from_attributes = True
