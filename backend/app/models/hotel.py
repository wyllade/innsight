import json
from sqlalchemy import Column, Integer, String, Text, Float, Boolean
from app.database import Base


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    public_id = Column(String(10), unique=True, index=True, nullable=False)
    name = Column(String(120), nullable=False)
    location = Column(String(120), nullable=False)
    country = Column(String(80), nullable=False, default="")
    city = Column(String(80), nullable=False)
    emoji = Column(String(10), nullable=False, default="hotel")
    badge = Column(String(40), nullable=True)
    _images = Column("images", Text, nullable=False, default="[]")
    _rooms = Column("rooms", Text, nullable=False, default="[]")
    price_per_night = Column(Float, nullable=False)
    rating = Column(Float, nullable=False, default=0)
    reviews_count = Column(Integer, nullable=False, default=0)
    stars = Column(Integer, nullable=False, default=3)
    hotel_type = Column(String(20), nullable=False, default="Hotel")
    _amenities = Column("amenities", Text, nullable=False, default="[]")
    description = Column(Text, nullable=False, default="")
    check_in = Column(String(5), nullable=False, default="14:00")
    check_out = Column(String(5), nullable=False, default="12:00")
    pets_allowed = Column(Boolean, nullable=False, default=False)
    smoking = Column(Boolean, nullable=False, default=False)
    _payments = Column("payments", Text, nullable=False, default="[]")
    cancellation_policy = Column(String(30), nullable=False, default="free_cancellation")
    lat = Column(Float, nullable=False, default=0)
    lng = Column(Float, nullable=False, default=0)

    @property
    def images(self):
        return json.loads(self._images)

    @images.setter
    def images(self, value):
        self._images = json.dumps(value)

    @property
    def rooms(self):
        return json.loads(self._rooms)

    @rooms.setter
    def rooms(self, value):
        self._rooms = json.dumps(value)

    @property
    def amenities(self):
        return json.loads(self._amenities)

    @amenities.setter
    def amenities(self, value):
        self._amenities = json.dumps(value)

    @property
    def payments(self):
        return json.loads(self._payments)

    @payments.setter
    def payments(self, value):
        self._payments = json.dumps(value)

    def to_dict(self):
        return {
            "id": self.public_id,
            "name": self.name,
            "location": self.location,
            "country": self.country,
            "city": self.city,
            "emoji": self.emoji,
            "badge": self.badge,
            "images": self.images,
            "rooms": self.rooms,
            "pricePerNight": self.price_per_night,
            "rating": self.rating,
            "reviews": self.reviews_count,
            "stars": self.stars,
            "type": self.hotel_type,
            "amenities": self.amenities,
            "description": self.description,
            "checkIn": self.check_in,
            "checkOut": self.check_out,
            "petsAllowed": self.pets_allowed,
            "smoking": self.smoking,
            "payments": self.payments,
            "cancellationPolicy": self.cancellation_policy,
            "lat": self.lat,
            "lng": self.lng,
        }
