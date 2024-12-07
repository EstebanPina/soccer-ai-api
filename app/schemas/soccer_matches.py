from pydantic import BaseModel

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
