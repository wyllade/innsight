import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException
from data.hotels import hotels, bookings
from middleware.error_handler import create_booking_record
from models.booking import BookingCreate

router = APIRouter()


@router.post("")
def create_booking(payload: BookingCreate):
    hotel = next((h for h in hotels if h["id"] == payload.hotelId), None)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    try:
        in_date = datetime.strptime(payload.checkIn, "%Y-%m-%d")
        out_date = datetime.strptime(payload.checkOut, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    if out_date <= in_date:
        raise HTTPException(status_code=400, detail="checkOut must be after checkIn")

    booking_id = str(uuid.uuid4())
    booking = create_booking_record(
        booking_id,
        hotel,
        payload.checkIn,
        payload.checkOut,
        payload.guests,
        payload.guestName,
        payload.guestEmail,
    )
    bookings.append(booking)

    return {"message": "Booking confirmed!", "booking": booking}


@router.get("")
def list_bookings():
    return {"total": len(bookings), "bookings": bookings}


@router.get("/{booking_id}")
def get_booking(booking_id: str):
    for b in bookings:
        if b["id"] == booking_id:
            return b
    raise HTTPException(status_code=404, detail="Booking not found")


@router.delete("/{booking_id}")
def cancel_booking(booking_id: str):
    for b in bookings:
        if b["id"] == booking_id:
            b["status"] = "cancelled"
            return {"message": "Booking cancelled", "booking": b}
    raise HTTPException(status_code=404, detail="Booking not found")
