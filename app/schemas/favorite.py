from pydantic import BaseModel
from typing import List
class FavoriteBase(BaseModel):
    match_id: str
    user_id: str
    class Config:
        from_attributes = True

class FavoriteResponse(BaseModel):
    favorites: List[str]

    class Config:
        from_attributes = True
class FavoriteCreate(FavoriteBase):
    pass

class FavoriteRead(FavoriteBase):
    id: str

    class Config:
        from_attributes = True
