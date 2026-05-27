from datetime import datetime, date
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.booking import Booking

bookings_bp = Blueprint("bookings", __name__)


def _calc_nights(check_in, check_out):
    try:
        ci = date.fromisoformat(check_in)
        co = date.fromisoformat(check_out)
        return max(1, (co - ci).days)
    except (ValueError, TypeError):
        return 1


def _calc_room_price(hotel, room_type):
    rooms = hotel.to_dict().get("rooms", [])
    for r in rooms:
        if r["type"] == room_type:
            return r["pricePerNight"]
    return hotel.price_per_night


@bookings_bp.route("/", methods=["GET"])
def get_bookings():
    query = Booking.query
    email = request.args.get("email")
    if email:
        query = query.filter(Booking.guest_email.ilike(f"%{email}%"))
    bookings = query.order_by(Booking.created_at.desc()).all()
    return jsonify({"bookings": [b.to_dict() for b in bookings]}), 200


@bookings_bp.route("/<id>", methods=["GET"])
def get_booking(id):
    booking = Booking.query.get_or_404(id)
    return jsonify({"booking": booking.to_dict()}), 200


@bookings_bp.route("/", methods=["POST"])
def create_booking():
    data = request.get_json()
    from app.models.hotel import Hotel
    hotel = Hotel.query.get(data["hotelId"])
    if not hotel:
        return jsonify({"error": "Hotel not found"}), 404

    nights = _calc_nights(data.get("checkIn", ""), data.get("checkOut", ""))
    room_type = data.get("roomType", "")
    ppn = _calc_room_price(hotel, room_type) if room_type else hotel.price_per_night

    total_price = data.get("totalPrice") or (ppn * nights)

    booking_id = f"b{datetime.utcnow().strftime('%y%m%d%H%M%S')}"
    booking = Booking(
        id=booking_id,
        hotel_id=data["hotelId"],
        guest_name=data["guestName"],
        guest_email=data["guestEmail"],
        room_type=room_type or "Standard",
        check_in=data["checkIn"],
        check_out=data["checkOut"],
        guests=data.get("guests", 1),
        total_price=total_price,
        status="confirmed",
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({"booking": booking.to_dict()}), 201


@bookings_bp.route("/<id>", methods=["PATCH"])
def update_booking(id):
    booking = Booking.query.get_or_404(id)
    data = request.get_json()
    if "status" in data:
        booking.status = data["status"]
    if "checkIn" in data:
        booking.check_in = data["checkIn"]
    if "checkOut" in data:
        booking.check_out = data["checkOut"]
    db.session.commit()
    return jsonify({"booking": booking.to_dict()}), 200


@bookings_bp.route("/<id>", methods=["DELETE"])
def cancel_booking(id):
    booking = Booking.query.get_or_404(id)
    booking.status = "cancelled"
    db.session.commit()
    return jsonify({"message": "Booking cancelled"}), 200
