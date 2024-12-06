from sqlalchemy import Column, String, DateTime,Double
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from cuid import cuid
class Venue(Base):
    __tablename__ = "Venue"

    id = Column(String, primary_key=True, index=True)
    stadium = Column(String, unique=True, index=True, nullable=False)
    location = Column(String, nullable=True)
    lat = Column(String, nullable=False)
    lon = Column(String, default=datetime.utcnow)
    weather = Column(String, nullable=True)
    temperature = Column(Double, nullable=True)
    wind_speed = Column(Double, nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow ,onupdate=datetime.utcnow)

    soccer_matches = relationship("SoccerMatches", back_populates="venue")