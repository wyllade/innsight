import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.hotel import Hotel

router = APIRouter(prefix="/api/hotels", tags=["Hotels"])

@router.get("")
def get_hotels(
    city: Optional[str] = None,
    amenities: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    sort: Optional[str] = None,
    type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Hotel)
    if city:
        query = query.filter(Hotel.city.ilike(f"%{city}%"))
    hotels = query.all()
    if amenities:
        target_amenities = [a.strip() for a in amenities.split(",") if a.strip()]
        filtered_hotels = []
        for h in hotels:
            if all(amenity in h.amenities for amenity in target_amenities):
                filtered_hotels.append(h)
        hotels = filtered_hotels
    output_data = [{
        "id": h.id,
        "name": h.name,
        "city": h.city,
        "description": h.description,
        "price_per_night": h.price_per_night,
        "price": h.price_per_night,
        "image_url": h.image_url,
        "rating": h.rating,
        "amenities": h.amenities,
        "reviews_count": 12
    } for h in hotels]
    return {
        "total": len(output_data),
        "data": output_data,
        "hotels": output_data
    }

@router.get("/featured")
def get_featured_hotels(db: Session = Depends(get_db)):
    hotels = db.query(Hotel).filter(Hotel.rating >= 4.7).all()
    return [{
        "id": h.id,
        "name": h.name,
        "city": h.city,
        "description": h.description,
        "price_per_night": h.price_per_night,
        "price": h.price_per_night,
        "image_url": h.image_url,
        "rating": h.rating,
        "amenities": h.amenities
    } for h in hotels]

@router.get("/amenities/all")
def get_all_amenities(db: Session = Depends(get_db)):
    hotels = db.query(Hotel).all()
    amenities_set = set()
    for h in hotels:
        amenities_set.update(h.amenities)
    return list(amenities_set)

@router.get("/cities/all")
def get_all_cities(db: Session = Depends(get_db)):
    results = db.query(Hotel.city).distinct().all()
    return [r[0] for r in results]

@router.get("/{hotel_id}")
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    h = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return {
        "id": h.id,
        "name": h.name,
        "city": h.city,
        "description": h.description,
        "price_per_night": h.price_per_night,
        "price": h.price_per_night,
        "image_url": h.image_url,
        "rating": h.rating,
        "amenities": h.amenities
    }

@router.get("/{hotel_id}/rooms")
def get_hotel_rooms(hotel_id: int):
    return [
        {"id": 101, "name": "Deluxe King Room", "price": 120.0, "capacity": 2},
        {"id": 102, "name": "Executive Suite", "price": 200.0, "capacity": 4}
    ]

@router.get("/{hotel_id}/reviews")
def get_hotel_reviews(hotel_id: int):
    return [
        {"id": 1, "author": "John Doe", "text": "Incredible stay!", "rating": 5},
        {"id": 2, "author": "Jane Smith", "text": "Very clean and spacious rooms.", "rating": 4}
    ]
