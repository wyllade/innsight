import math
import time
from datetime import datetime
from fastapi import APIRouter, Query, HTTPException
from app.data.hotels import hotels, reviews as all_reviews, bookings
from app.middleware.error_handler import filter_hotels, paginate

router = APIRouter()


@router.get("")
def list_hotels(
    q: str = Query(""),
    city: str = Query(""),
    country: str = Query(""),
    amenities: str = Query(""),
    minPrice: str = Query(""),
    maxPrice: str = Query(""),
    stars: str = Query(""),
    type: str = Query(""),
    sort: str = Query(""),
    checkIn: str = Query(""),
    checkOut: str = Query(""),
    page: int = Query(1),
    limit: int = Query(20),
):
    results = filter_hotels(
        hotels, q, city, country, amenities, minPrice, maxPrice,
        stars, type, sort, checkIn, checkOut, bookings,
    )
    return paginate(results, page, limit)


@router.get("/featured")
def get_featured():
    featured = sorted(
        hotels, key=lambda h: h["rating"] * math.log10(h["reviews"] + 1), reverse=True
    )[:4]
    return {"total": len(featured), "results": featured}


@router.get("/amenities/all")
def get_amenities():
    all_amenities = sorted(set(a for h in hotels for a in h["amenities"]))
    return all_amenities


@router.get("/cities/all")
def get_cities():
    cities = sorted(set(h["city"] for h in hotels))
    return cities


@router.get("/{hotel_id}/rooms")
def get_hotel_rooms(hotel_id: str):
    for h in hotels:
        if h["id"] == hotel_id:
            return {"rooms": h.get("rooms", [])}
    raise HTTPException(status_code=404, detail="Hotel not found")


@router.get("/{hotel_id}/reviews")
def get_hotel_reviews(hotel_id: str):
    if not any(h["id"] == hotel_id for h in hotels):
        raise HTTPException(status_code=404, detail="Hotel not found")
    hotel_reviews = [r for r in all_reviews if r["hotelId"] == hotel_id]
    return {"total": len(hotel_reviews), "reviews": hotel_reviews}


@router.post("/{hotel_id}/reviews")
def add_hotel_review(hotel_id: str, body: dict):
    hotel = next((h for h in hotels if h["id"] == hotel_id), None)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    author = (body.get("author") or "").strip()
    rating = body.get("rating")
    text = (body.get("text") or "").strip()

    if not author or not rating or not text:
        raise HTTPException(status_code=400, detail="Missing required fields: author, rating, text")

    try:
        num_rating = float(rating)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Rating must be a number")

    if num_rating < 1 or num_rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    review = {
        "id": "r" + str(int(time.time() * 1000)),
        "hotelId": hotel_id,
        "author": author,
        "rating": num_rating,
        "text": text,
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
    }

    all_reviews.append(review)

    hotel_reviews = [r for r in all_reviews if r["hotelId"] == hotel_id]
    avg_rating = sum(r["rating"] for r in hotel_reviews) / len(hotel_reviews)
    hotel["rating"] = round(avg_rating, 1)
    hotel["reviews"] = len(hotel_reviews)

    return {"message": "Review added", "review": review}


@router.get("/{hotel_id}/availability")
def check_availability(hotel_id: str, checkIn: str = Query(...), checkOut: str = Query(...)):
    hotel = next((h for h in hotels if h["id"] == hotel_id), None)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    try:
        ci = datetime.strptime(checkIn, "%Y-%m-%d")
        co = datetime.strptime(checkOut, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    if co <= ci:
        raise HTTPException(status_code=400, detail="checkOut must be after checkIn")

    overlapping = [
        b for b in bookings
        if b["hotelId"] == hotel_id
        and b["status"] != "cancelled"
        and datetime.strptime(b["checkIn"], "%Y-%m-%d") < co
        and datetime.strptime(b["checkOut"], "%Y-%m-%d") > ci
    ]

    return {
        "hotelId": hotel_id,
        "checkIn": checkIn,
        "checkOut": checkOut,
        "available": len(overlapping) == 0,
        "overlappingBookings": len(overlapping),
    }


@router.get("/{hotel_id}")
def get_hotel(hotel_id: str):
    for h in hotels:
        if h["id"] == hotel_id:
            return h
    raise HTTPException(status_code=404, detail="Hotel not found")
