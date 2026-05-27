from datetime import datetime
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.booking import Booking

bookings_bp = Blueprint("bookings", __name__)


@bookings_bp.route("/", methods=["GET"])
def get_bookings():
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return jsonify([b.to_dict() for b in bookings]), 200


@bookings_bp.route("/<id>", methods=["GET"])
def get_booking(id):
    booking = Booking.query.get_or_404(id)
    return jsonify(booking.to_dict()), 200


@bookings_bp.route("/", methods=["POST"])
def create_booking():
    data = request.get_json()
    from app.models.hotel import Hotel
    hotel = Hotel.query.get(data["hotelId"])
    if not hotel:
        return jsonify({"error": "Hotel not found"}), 404

    booking_id = f"b{datetime.utcnow().strftime('%y%m%d%H%M%S')}"
    booking = Booking(
        id=booking_id,
        hotel_id=data["hotelId"],
        guest_name=data["guestName"],
        guest_email=data["guestEmail"],
        room_type=data["roomType"],
        check_in=data["checkIn"],
        check_out=data["checkOut"],
        guests=data.get("guests", 1),
        total_price=data["totalPrice"],
        status="confirmed",
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify(booking.to_dict()), 201


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
    return jsonify(booking.to_dict()), 200


@bookings_bp.route("/<id>", methods=["DELETE"])
def cancel_booking(id):
    booking = Booking.query.get_or_404(id)
    booking.status = "cancelled"
    db.session.commit()
    return jsonify({"message": "Booking cancelled"}), 200
