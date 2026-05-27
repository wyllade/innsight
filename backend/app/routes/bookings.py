from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from app.models.hotel import Hotel
from app.models.booking import Booking

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

class BookingCreate(BaseModel):
    hotel_id: int
    checkin_date: str
    checkout_date: str
    total_price: float

@router.post("")
def create_booking(payload: BookingCreate, db: Session = Depends(get_db), fallback_email: Optional[str] = Query(None)):
    email_to_link = fallback_email or "guest@innsight.com"
    hotel = db.query(Hotel).filter(Hotel.id == payload.hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    booking_obj = Booking(
        hotel_id=payload.hotel_id,
        user_email=email_to_link,
        checkin_date=payload.checkin_date,
        checkout_date=payload.checkout_date,
        total_price=payload.total_price
    )
    db.add(booking_obj)
    db.commit()
    db.refresh(booking_obj)
    return {
        "id": booking_obj.id,
        "hotel_id": booking_obj.hotel_id,
        "hotel_name": hotel.name,
        "user_email": booking_obj.user_email,
        "checkin_date": booking_obj.checkin_date,
        "checkout_date": booking_obj.checkout_date,
        "total_price": booking_obj.total_price,
        "status": booking_obj.status,
        "message": "booked"
    }

@router.get("")
def get_bookings(db: Session = Depends(get_db), fallback_email: Optional[str] = Query(None)):
    email_to_query = fallback_email or "guest@innsight.com"
    bookings = db.query(Booking).filter(Booking.user_email == email_to_query).all()
    output_data = []
    for b in bookings:
        hotel = db.query(Hotel).filter(Hotel.id == b.hotel_id).first()
        output_data.append({
            "id": b.id,
            "hotel_id": b.hotel_id,
            "hotel_name": hotel.name if hotel else "Unknown Hotel",
            "image_url": hotel.image_url if hotel else None,
            "user_email": b.user_email,
            "checkin_date": b.checkin_date,
            "checkout_date": b.checkout_date,
            "total_price": b.total_price,
            "status": b.status
        })
    return output_data
