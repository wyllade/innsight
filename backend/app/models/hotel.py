import json
from app.extensions import db


class Hotel(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(80), nullable=False, default="")
    city = db.Column(db.String(80), nullable=False, default="")
    emoji = db.Column(db.String(10), nullable=False, default="🏨")
    badge = db.Column(db.String(40), nullable=True)
    images = db.Column(db.Text, nullable=False, default="[]")
    rooms = db.Column(db.Text, nullable=False, default="[]")
    price_per_night = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False, default=0)
    reviews_count = db.Column(db.Integer, nullable=False, default=0)
    stars = db.Column(db.Integer, nullable=False, default=3)
    hotel_type = db.Column(db.String(20), nullable=False, default="Hotel")
    amenities = db.Column(db.Text, nullable=False, default="[]")
    description = db.Column(db.Text, nullable=False, default="")
    check_in = db.Column(db.String(5), nullable=False, default="14:00")
    check_out = db.Column(db.String(5), nullable=False, default="12:00")
    pets_allowed = db.Column(db.Boolean, nullable=False, default=False)
    smoking = db.Column(db.Boolean, nullable=False, default=False)
    payments = db.Column(db.Text, nullable=False, default="[]")
    cancellation_policy = db.Column(db.String(30), nullable=False, default="free_cancellation")
    lat = db.Column(db.Float, nullable=False, default=0)
    lng = db.Column(db.Float, nullable=False, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "country": self.country,
            "city": self.city,
            "emoji": self.emoji,
            "badge": self.badge,
            "images": json.loads(self.images),
            "rooms": json.loads(self.rooms),
            "pricePerNight": self.price_per_night,
            "rating": self.rating,
            "reviews": self.reviews_count,
            "stars": self.stars,
            "type": self.hotel_type,
            "amenities": json.loads(self.amenities),
            "description": self.description,
            "checkIn": self.check_in,
            "checkOut": self.check_out,
            "petsAllowed": self.pets_allowed,
            "smoking": self.smoking,
            "payments": json.loads(self.payments),
            "cancellationPolicy": self.cancellation_policy,
            "lat": self.lat,
            "lng": self.lng,
        }