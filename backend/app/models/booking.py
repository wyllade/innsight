from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    user_email = Column(String, index=True, nullable=False)
    checkin_date = Column(String, nullable=False)
    checkout_date = Column(String, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, default="confirmed")
