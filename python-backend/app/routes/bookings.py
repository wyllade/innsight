import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from app.data.hotels import hotels, bookings, reviews
from app.middleware.error_handler import create_booking_record

router = APIRouter()


@router.post("")
def create_booking(payload: dict):
    hotel_id = payload.get("hotelId")
    check_in = payload.get("checkIn")
    check_out = payload.get("checkOut")
    guest_name = payload.get("guestName", "").strip()
    guest_email = payload.get("guestEmail", "").strip()
    guests = payload.get("guests", 1)
    room_type = payload.get("roomType")

    if not hotel_id or not check_in or not check_out or not guest_name or not guest_email:
        raise HTTPException(status_code=400, detail="Missing required fields: hotelId, checkIn, checkOut, guestName, guestEmail")

    hotel = next((h for h in hotels if h["id"] == hotel_id), None)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    try:
        in_date = datetime.strptime(check_in, "%Y-%m-%d")
        out_date = datetime.strptime(check_out, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    if out_date <= in_date:
        raise HTTPException(status_code=400, detail="checkOut must be after checkIn")

    # Check availability
    overlapping = [
        b for b in bookings
        if b["hotelId"] == hotel_id
        and b["status"] != "cancelled"
        and datetime.strptime(b["checkIn"], "%Y-%m-%d") < out_date
        and datetime.strptime(b["checkOut"], "%Y-%m-%d") > in_date
    ]
    if overlapping:
        raise HTTPException(status_code=409, detail="Hotel is not available for the selected dates")

    # Room type selection
    price_per_night = hotel["pricePerNight"]
    selected_room = None
    if room_type and hotel.get("rooms"):
        rooms = hotel["rooms"]
        selected_room = next(
            (r for r in rooms if r["type"].lower() == room_type.lower()), None
        )
        if selected_room:
            price_per_night = selected_room["pricePerNight"]
            if selected_room["available"] <= 0:
                raise HTTPException(status_code=409, detail="Selected room type is sold out")

    # Guest count check
    if selected_room and guests > selected_room["maxGuests"]:
        raise HTTPException(
            status_code=400,
            detail=f"Selected room type ({selected_room['type']}) max {selected_room['maxGuests']} guests",
        )

    booking_id = str(uuid.uuid4())
    booking = create_booking_record(
        booking_id,
        hotel,
        check_in,
        check_out,
        guests,
        guest_name,
        guest_email,
        room_type=(selected_room["type"] if selected_room else None),
        price_per_night=price_per_night,
    )
    bookings.append(booking)

    # Decrement room availability
    if selected_room:
        selected_room["available"] = max(0, selected_room["available"] - 1)

    return {"message": "Booking confirmed!", "booking": booking}


@router.get("")
def list_bookings(email: str = Query("")):
    result = bookings
    if email:
        result = [b for b in bookings if b["guestEmail"].lower() == email.lower()]
    return {"total": len(result), "bookings": result}


@router.get("/{booking_id}")
def get_booking(booking_id: str):
    for b in bookings:
        if b["id"] == booking_id:
            return b
    raise HTTPException(status_code=404, detail="Booking not found")


@router.patch("/{booking_id}")
def modify_booking(booking_id: str, body: dict):
    booking = next((b for b in bookings if b["id"] == booking_id), None)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking["status"] == "cancelled":
        raise HTTPException(status_code=400, detail="Cannot modify a cancelled booking")

    if "checkIn" in body:
        booking["checkIn"] = body["checkIn"]
    if "checkOut" in body:
        booking["checkOut"] = body["checkOut"]
    if "guests" in body:
        booking["guests"] = body["guests"]

    try:
        in_date = datetime.strptime(booking["checkIn"], "%Y-%m-%d")
        out_date = datetime.strptime(booking["checkOut"], "%Y-%m-%d")
        if out_date > in_date:
            nights = max(1, (out_date - in_date).days)
            booking["nights"] = nights
            booking["subtotal"] = nights * booking["pricePerNight"]
            booking["taxes"] = round(booking["subtotal"] * 0.16)
            booking["total"] = booking["subtotal"] + booking["taxes"]
    except ValueError:
        pass

    return {"message": "Booking updated", "booking": booking}


@router.delete("/{booking_id}")
def cancel_booking(booking_id: str):
    for b in bookings:
        if b["id"] == booking_id:
            b["status"] = "cancelled"
            return {"message": "Booking cancelled", "booking": b}
    raise HTTPException(status_code=404, detail="Booking not found")
