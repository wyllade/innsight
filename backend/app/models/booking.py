from datetime import datetime
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

    def to_dict(self):
        return {
            "id": self.id,
            "hotelId": self.hotel_id,
            "guestName": self.guest_name,
            "guestEmail": self.guest_email,
            "roomType": self.room_type,
            "checkIn": self.check_in,
            "checkOut": self.check_out,
            "guests": self.guests,
            "totalPrice": self.total_price,
            "status": self.status,
            "createdAt": self.created_at,
        }
