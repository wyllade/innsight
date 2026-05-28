from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    author = Column(String, default="Guest Traveler")
    text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
