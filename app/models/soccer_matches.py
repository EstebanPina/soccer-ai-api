from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from app.core.database import Base
from cuid import cuid
from sqlalchemy.orm import relationship
class SoccerMatches(Base):
    __tablename__ = "SoccerMatches"

    id = Column(String, primary_key=True, index=True, default=cuid)
    id_sports_api = Column(String, nullable=False)
    view_count = Column(Integer, nullable=False, default=0)
    prediction_ai = Column(String, nullable=True)
    local_team = Column(String, nullable=False)
    visitor_team = Column(String, nullable=False)
    finished = Column(Boolean, default=False)
    venueId = Column(String, ForeignKey("Venue.id"), nullable=False)
    
    venue = relationship("Venue", back_populates="soccer_matches")
    
