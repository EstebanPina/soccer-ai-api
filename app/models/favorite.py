from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from cuid import cuid
class Favorite(Base):
    __tablename__ = "Favorite"

    id = Column(String, primary_key=True, index=True, default=cuid)
    matchId = Column(String, nullable=False)
    userId = Column(String, ForeignKey("User.id"), nullable=False)
    
    user = relationship("User", back_populates="user_favorites")
