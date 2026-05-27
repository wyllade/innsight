from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.hotel import Hotel

hotel_bp = Blueprint("hotel", __name__)


@hotel_bp.route("/", methods=["GET"])
def get_hotels():
    query = Hotel.query

    city = request.args.get("city")
    if city:
        query = query.filter(Hotel.city.ilike(f"%{city}%"))

    q = request.args.get("q")
    if q:
        query = query.filter(
            Hotel.name.ilike(f"%{q}%") | Hotel.description.ilike(f"%{q}%")
        )

    amenities = request.args.get("amenities")
    if amenities:
        wanted = [a.strip().lower() for a in amenities.split(",")]
        all_hotels = query.all()
        filtered = []
        for h in all_hotels:
            h_amenities = [a.lower() for a in h.to_dict()["amenities"]]
            if any(a in h_amenities for a in wanted):
                filtered.append(h)
        # Re-query with IDs
        ids = [h.id for h in filtered]
        query = Hotel.query.filter(Hotel.id.in_(ids))

    min_price = request.args.get("minPrice")
    if min_price:
        query = query.filter(Hotel.price_per_night >= float(min_price))

    max_price = request.args.get("maxPrice")
    if max_price:
        query = query.filter(Hotel.price_per_night <= float(max_price))

    stars = request.args.get("stars")
    if stars:
        query = query.filter(Hotel.stars >= int(stars))

    type_param = request.args.get("type")
    if type_param:
        types = [t.strip() for t in type_param.split(",")]
        query = query.filter(Hotel.hotel_type.in_(types))

    sort = request.args.get("sort")
    if sort == "price_asc":
        query = query.order_by(Hotel.price_per_night.asc())
    elif sort == "price_desc":
        query = query.order_by(Hotel.price_per_night.desc())
    elif sort == "rating":
        query = query.order_by(Hotel.rating.desc())
    elif sort == "reviews":
        query = query.order_by(Hotel.reviews_count.desc())

    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 20, type=int)

    total = query.count()
    total_pages = (total + limit - 1) // limit
    hotels = query.offset((page - 1) * limit).limit(limit).all()

    return jsonify({
        "total": total,
        "page": page,
        "limit": limit,
        "totalPages": total_pages,
        "results": [h.to_dict() for h in hotels],
    }), 200


@hotel_bp.route("/featured", methods=["GET"])
def get_featured():
    hotels = Hotel.query.order_by(Hotel.rating.desc()).limit(6).all()
    return jsonify([h.to_dict() for h in hotels]), 200


@hotel_bp.route("/<id>", methods=["GET"])
def get_single_hotel(id):
    hotel = Hotel.query.get_or_404(id)
    return jsonify(hotel.to_dict()), 200


@hotel_bp.route("/<id>/rooms", methods=["GET"])
def get_hotel_rooms(id):
    hotel = Hotel.query.get_or_404(id)
    return jsonify(hotel.to_dict()["rooms"]), 200


@hotel_bp.route("/<id>/reviews", methods=["GET"])
def get_hotel_reviews(id):
    return jsonify([]), 200


@hotel_bp.route("/<id>/reviews", methods=["POST"])
def add_hotel_review(id):
    return jsonify({"message": "Review added"}), 201


@hotel_bp.route("/<id>/availability", methods=["GET"])
def check_availability(id):
    hotel = Hotel.query.get_or_404(id)
    rooms = hotel.to_dict()["rooms"]
    return jsonify({"available": True, "rooms": rooms}), 200


@hotel_bp.route("/amenities/all", methods=["GET"])
def get_all_amenities():
    hotels = Hotel.query.all()
    all_amenities = set()
    for h in hotels:
        for a in h.to_dict()["amenities"]:
            all_amenities.add(a)
    return jsonify(sorted(all_amenities)), 200


@hotel_bp.route("/cities/all", methods=["GET"])
def get_all_cities():
    cities = Hotel.query.with_entities(Hotel.city).distinct().all()
    return jsonify(sorted([c[0] for c in cities if c[0]]))
