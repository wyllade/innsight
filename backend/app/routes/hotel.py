from flask import Blueprint, jsonify
from app.models.hotel import Hotel

hotel_bp = Blueprint("hotel", __name__)


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