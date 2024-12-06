from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from cuid import cuid
class User(Base):
    __tablename__ = "User"

    id = Column(String, primary_key=True, index=True, default=cuid)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    password = Column(String, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow ,onupdate=datetime.utcnow)
    
    user_favorites = relationship("Favorite", back_populates="user")
