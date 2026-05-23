from pydantic import BaseModel
from typing import Optional


class Hotel(BaseModel):
    id: str
    name: str
    location: str
    country: str
    city: str
    emoji: str
    badge: Optional[str] = None
    pricePerNight: int
    rating: float
    reviews: int
    stars: int
    type: str
    amenities: list[str]
    description: str
    checkIn: str
    checkOut: str
    petsAllowed: bool
    smoking: bool
    payments: list[str]
    lat: float
    lng: float
