from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.hotel import Hotel

hotel_bp = Blueprint("hotel", __name__)


@hotel_bp.route("/", methods=["POST"])
@jwt_required()
def create_hotel():
    data = request.get_json()

    hotel = Hotel(
        name=data["name"],
        location=data["location"],
        description=data["description"],
        price_per_night=data["price_per_night"],
        created_by=get_jwt_identity()
    )

    db.session.add(hotel)
    db.session.commit()

    return jsonify({
        "message": "Hotel created",
        "hotel": hotel.to_dict()
    }), 201


@hotel_bp.route("/", methods=["GET"])
def get_hotels():
    hotels = Hotel.query.all()

    return jsonify([
        hotel.to_dict()
        for hotel in hotels
    ]), 200


@hotel_bp.route("/<int:id>", methods=["GET"])
def get_single_hotel(id):
    hotel = Hotel.query.get_or_404(id)

    return jsonify(hotel.to_dict()), 200