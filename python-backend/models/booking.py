from pydantic import BaseModel
from typing import Optional


class BookingCreate(BaseModel):
    hotelId: str
    checkIn: str
    checkOut: str
    guests: int = 1
    guestName: str
    guestEmail: str


class Booking(BaseModel):
    id: str
    hotelId: str
    hotelName: str
    hotelLocation: str
    checkIn: str
    checkOut: str
    nights: int
    guests: int
    guestName: str
    guestEmail: str
    pricePerNight: int
    subtotal: int
    taxes: int
    total: int
    status: str
    createdAt: str


class BookingResponse(BaseModel):
    message: str
    booking: Booking
