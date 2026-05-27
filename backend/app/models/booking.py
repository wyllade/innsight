from datetime import datetime, date
from app.extensions import db


class Booking(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    hotel_id = db.Column(db.String(10), db.ForeignKey("hotel.id"), nullable=False)
    guest_name = db.Column(db.String(120), nullable=False)
    guest_email = db.Column(db.String(120), nullable=False)
    room_type = db.Column(db.String(80), nullable=False)
    check_in = db.Column(db.String(10), nullable=False)
    check_out = db.Column(db.String(10), nullable=False)
    guests = db.Column(db.Integer, nullable=False, default=1)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="confirmed")
    created_at = db.Column(db.String(20), nullable=False, default=lambda: datetime.utcnow().isoformat())

    def _calc_nights(self):
        try:
            ci = date.fromisoformat(self.check_in)
            co = date.fromisoformat(self.check_out)
            return max(1, (co - ci).days)
        except (ValueError, TypeError):
            return 1

    def to_dict(self):
        from app.models.hotel import Hotel
        hotel = Hotel.query.get(self.hotel_id)
        hotel_name = hotel.name if hotel else "Unknown"
        hotel_location = hotel.location if hotel else ""
        return {
            "id": self.id,
            "hotelId": self.hotel_id,
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
            "createdAt": self.created_at,
        }
