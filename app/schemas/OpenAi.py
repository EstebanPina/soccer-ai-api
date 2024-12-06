from pydantic import BaseModel
class OpenAiBase(BaseModel):
    local_team: str
    visitor_team: str
    temperature: float
    weather: str
    wind_speed: float

class OpenAiCreate(OpenAiBase):
    pass