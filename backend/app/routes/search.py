from flask import Blueprint, request, jsonify
from app.services.amadeus import search_hotels_by_city

search_bp = Blueprint("search", __name__)


@search_bp.route("/hotels", methods=["GET"])
def search_hotels():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "city is required"}), 400

    hotels = search_hotels_by_city(city)

    result = [
        {
            "name": h.get("name"),
            "chainCode": h.get("chainCode"),
            "iataCode": h.get("iataCode")
        }
        for h in hotels
    ]

    return jsonify({
        "city": city,
        "results": result
    })