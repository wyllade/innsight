from datetime import date
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    public_id = Column(String(20), unique=True, index=True, nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    guest_name = Column(String(120), nullable=False)
    guest_email = Column(String(120), nullable=False)
    room_type = Column(String(80), nullable=False)
    check_in = Column(String(10), nullable=False)
    check_out = Column(String(10), nullable=False)
    guests = Column(Integer, nullable=False, default=1)
    total_price = Column(Float, nullable=False)
    status = Column(String(20), nullable=False, default="confirmed")

    def _calc_nights(self):
        try:
            ci = date.fromisoformat(self.check_in)
            co = date.fromisoformat(self.check_out)
            return max(1, (co - ci).days)
        except (ValueError, TypeError):
            return 1

    def to_dict(self):
        from app.models.hotel import Hotel
        from app.database import SessionLocal
        db = SessionLocal()
        try:
            hotel = db.query(Hotel).filter(Hotel.id == self.hotel_id).first()
            hotel_name = hotel.name if hotel else "Unknown"
            hotel_location = hotel.location if hotel else ""
        finally:
            db.close()
        return {
            "id": self.public_id,
            "hotelId": str(self.hotel_id),
            "hotelName": hotel_name,
            "hotelLocation": hotel_location,
            "guestName": self.guest_name,
            "guestEmail": self.guest_email,
            "roomType": self.room_type,
            "checkIn": self.check_in,
            "checkOut": self.check_out,
            "guests": self.guests,
            "nights": self._calc_nights(),
            "total": self.total_price,
            "totalPrice": self.total_price,
            "status": self.status,
        }
