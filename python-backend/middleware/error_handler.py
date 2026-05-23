import math
import logging
from datetime import datetime

logger = logging.getLogger("innsight")


def best_match_score(hotel: dict) -> float:
    return hotel["rating"] * math.log10(hotel["reviews"] + 1)


def filter_hotels(
    hotels: list[dict],
    q: str = "",
    city: str = "",
    amenities: str = "",
    min_price: str = "",
    max_price: str = "",
    stars: str = "",
    prop_type: str = "",
    sort: str = "",
) -> list[dict]:
    results = list(hotels)

    if q:
        lq = q.lower()
        results = [
            h
            for h in results
            if lq in h["name"].lower()
            or lq in h["location"].lower()
            or lq in h["description"].lower()
            or any(lq in a.lower() for a in h["amenities"])
        ]

    if city:
        lcity = city.lower()
        results = [h for h in results if lcity in h["city"].lower()]

    if amenities:
        requested = [a.strip().lower() for a in amenities.split(",")]
        results = [
            h
            for h in results
            if all(
                any(ra in ha.lower() for ha in h["amenities"]) for ra in requested
            )
        ]

    if min_price:
        results = [h for h in results if h["pricePerNight"] >= int(min_price)]

    if max_price:
        results = [h for h in results if h["pricePerNight"] <= int(max_price)]

    if stars:
        min_stars = int(stars)
        results = [h for h in results if h["stars"] >= min_stars]

    if prop_type:
        ltype = prop_type.lower()
        results = [h for h in results if h["type"].lower() == ltype]

    sort_map = {
        "price_asc": lambda h: h["pricePerNight"],
        "price_desc": lambda h: -h["pricePerNight"],
        "rating": lambda h: -h["rating"],
        "reviews": lambda h: -h["reviews"],
    }

    if sort and sort in sort_map:
        results.sort(key=sort_map[sort])
    else:
        results.sort(key=best_match_score, reverse=True)

    return results


def create_booking_record(
    booking_id: str,
    hotel: dict,
    check_in: str,
    check_out: str,
    guests: int,
    guest_name: str,
    guest_email: str,
) -> dict:
    in_date = datetime.strptime(check_in, "%Y-%m-%d")
    out_date = datetime.strptime(check_out, "%Y-%m-%d")
    nights = max(1, (out_date - in_date).days)
    subtotal = nights * hotel["pricePerNight"]
    taxes = round(subtotal * 0.16)
    total = subtotal + taxes

    return {
        "id": booking_id,
        "hotelId": hotel["id"],
        "hotelName": hotel["name"],
        "hotelLocation": hotel["location"],
        "checkIn": check_in,
        "checkOut": check_out,
        "nights": nights,
        "guests": guests,
        "guestName": guest_name,
        "guestEmail": guest_email,
        "pricePerNight": hotel["pricePerNight"],
        "subtotal": subtotal,
        "taxes": taxes,
        "total": total,
        "status": "confirmed",
        "createdAt": datetime.utcnow().isoformat() + "Z",
    }
