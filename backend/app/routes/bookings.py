from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.models.hotel import Hotel
from app.models.booking import Booking

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])


def _calc_nights(check_in: str, check_out: str) -> int:
    try:
        ci = date.fromisoformat(check_in)
        co = date.fromisoformat(check_out)
        return max(1, (co - ci).days)
    except (ValueError, TypeError):
        return 1


def _calc_room_price(hotel: Hotel, room_type: str) -> float:
    for r in hotel.rooms:
        if r.get("type") == room_type:
            return r.get("pricePerNight", hotel.price_per_night)
    return hotel.price_per_night


class BookingCreate(BaseModel):
    hotelId: str
    checkIn: str
    checkOut: str
    guests: int = 1
    guestName: str
    guestEmail: str
    roomType: str = ""


@router.get("")
def get_bookings(
    email: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Booking)
    if email:
        query = query.filter(Booking.guest_email.ilike(f"%{email}%"))
    bookings = query.order_by(Booking.id.desc()).all()
    return {"bookings": [b.to_dict() for b in bookings]}


@router.get("/{booking_id}")
def get_booking(booking_id: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.public_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"booking": booking.to_dict()}


@router.post("")
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    hotel = db.query(Hotel).filter(Hotel.public_id == payload.hotelId).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    nights = _calc_nights(payload.checkIn, payload.checkOut)
    ppn = _calc_room_price(hotel, payload.roomType) if payload.roomType else hotel.price_per_night
    total_price = ppn * nights

    booking_id = f"b{datetime.utcnow().strftime('%y%m%d%H%M%S')}"
    booking = Booking(
        public_id=booking_id,
        hotel_id=hotel.id,
        guest_name=payload.guestName,
        guest_email=payload.guestEmail,
        room_type=payload.roomType or "Standard",
        check_in=payload.checkIn,
        check_out=payload.checkOut,
        guests=payload.guests,
        total_price=total_price,
        status="confirmed",
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return {"booking": booking.to_dict()}


@router.patch("/{booking_id}")
def update_booking(booking_id: str, body: dict, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.public_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if "status" in body:
        booking.status = body["status"]
    if "checkIn" in body:
        booking.check_in = body["checkIn"]
    if "checkOut" in body:
        booking.check_out = body["checkOut"]
    db.commit()
    return {"booking": booking.to_dict()}


@router.delete("/{booking_id}")
def cancel_booking(booking_id: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.public_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.status = "cancelled"
    db.commit()
    return {"message": "Booking cancelled"}
