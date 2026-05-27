from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.booking import Booking

booking_bp = Blueprint("booking", __name__)


@booking_bp.route("/", methods=["POST"])
@jwt_required()
def create_booking():
    user_id = get_jwt_identity()
    data = request.get_json()

    booking = Booking(
        user_id=user_id,
        hotel_name=data["hotel_name"],
        city=data["city"],
        external_hotel_id=data.get("external_hotel_id")
    )

    db.session.add(booking)
    db.session.commit()

    return jsonify(booking.to_dict()), 201


@booking_bp.route("/", methods=["GET"])
@jwt_required()
def get_bookings():
    user_id = get_jwt_identity()

    bookings = Booking.query.filter_by(user_id=user_id).all()

    return jsonify([b.to_dict() for b in bookings])