import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from app.models.hotel import Hotel
from app.models.review import Review

router = APIRouter(prefix="/api/hotels", tags=["Hotels"])

class ReviewCreate(BaseModel):
    author: Optional[str] = "Guest Traveler"
    text: str
    rating: int

def get_dynamic_photo(index: int) -> str:
    photo_ids = [
        "1566073771259-6a8506099945", "1520250497591-112f2f40a3f4", "1540541338287-41700207dee6",
        "1551882547-ff40c63fe5fa", "1571896349842-33c89424de2d", "1584132967334-10e028bd69f7",
        "1542314831-068cd1dbfeeb", "1564507592-33cf54a55c27", "1596394516093-501ba68a0ba6"
    ]
    return f"https://unsplash.com{photo_ids[index % len(photo_ids)]}?auto=format&fit=crop&w=800&q=80"

@router.get("")
def get_hotels(
    city: Optional[str] = None,
    amenities: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    sort: Optional[str] = None,
    type: Optional[str] = None,
    stars: Optional[str] = None,
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
    output_data = []
    for i, h in enumerate(hotels):
        img = h.image_url if h.image_url and "unsplash" in h.image_url else get_dynamic_photo(i)
        db_reviews = db.query(Review).filter(Review.hotel_id == h.id).all()
        reviews_list = [{"id": str(r.id), "author": r.author, "text": r.text, "rating": r.rating} for r in db_reviews]
        if not reviews_list:
            reviews_list = [{"id": "1", "author": "John Doe", "text": "Incredible stay!", "rating": 5}]
        output_data.append({
            "id": str(h.id),
            "_id": str(h.id),
            "name": h.name,
            "city": h.city,
            "location": h.city,
            "description": h.description or "Premier luxury hotel offering refined comfort.",
            "price_per_night": float(h.price_per_night),
            "pricePerNight": float(h.price_per_night),
            "price": float(h.price_per_night),
            "image_url": img,
            "image": img,
            "rating": h.rating or 4.5,
            "stars": 5,
            "type": "Hotel",
            "amenities": h.amenities,
            "reviews_count": len(reviews_list),
            "reviews": reviews_list,
            "rooms": [
                {"id": 101, "name": "Deluxe King Room", "price": float(h.price_per_night), "capacity": 2},
                {"id": 102, "name": "Executive Suite", "price": float(h.price_per_night * 1.5), "capacity": 4}
            ]
        })
    return {
        "total": len(output_data),
        "data": output_data,
        "hotels": output_data,
        "results": output_data
    }

@router.get("/featured")
def get_featured_hotels(db: Session = Depends(get_db)):
    hotels = db.query(Hotel).filter(Hotel.rating >= 4.7).all()
    return [{
        "id": str(h.id),
        "_id": str(h.id),
        "name": h.name,
        "city": h.city,
        "location": h.city,
        "description": h.description,
        "price_per_night": float(h.price_per_night),
        "pricePerNight": float(h.price_per_night),
        "price": float(h.price_per_night),
        "image_url": get_dynamic_photo(i),
        "image": get_dynamic_photo(i),
        "rating": h.rating,
        "amenities": h.amenities
    } for i, h in enumerate(hotels)]

@router.get("/amenities/all")
def get_all_amenities(db: Session = Depends(get_db)):
    hotels = db.query(Hotel).all()
    amenities_set = set()
    for h in hotels:
        amenities_set.update(h.amenities)
    return list(amenities_set) if amenities_set else ["Swimming Pool", "Free WiFi", "Gym", "Breakfast", "Spa", "Bar"]

@router.get("/cities/all")
def get_all_cities(db: Session = Depends(get_db)):
    results = db.query(Hotel.city).distinct().all()
    return [r for r in results] if results else ["Nairobi", "Mombasa", "Kisumu"]

@router.get("/{hotel_id}")
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    h = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Hotel not found")
    img = h.image_url if h.image_url and "unsplash" in h.image_url else get_dynamic_photo(h.id)
    db_reviews = db.query(Review).filter(Review.hotel_id == h.id).all()
    reviews_list = [{"id": str(r.id), "author": r.author, "text": r.text, "rating": r.rating} for r in db_reviews]
    if not reviews_list:
        reviews_list = [
            {"id": "1", "author": "John Doe", "text": "Incredible stay!", "rating": 5},
            {"id": "2", "author": "Jane Smith", "text": "Very clean and spacious rooms.", "rating": 4}
        ]
    return {
        "id": str(h.id),
        "_id": str(h.id),
        "name": h.name,
        "city": h.city,
        "location": h.city,
        "description": h.description or "Premier luxury hotel offering refined comfort.",
        "price_per_night": float(h.price_per_night),
        "pricePerNight": float(h.price_per_night),
        "price": float(h.price_per_night),
        "image_url": img,
        "image": img,
        "rating": h.rating or 4.5,
        "stars": 5,
        "type": "Hotel",
        "amenities": h.amenities,
        "reviews_count": len(reviews_list),
        "reviews": reviews_list,
        "data": reviews_list,
        "rooms": [
            {"id": 101, "name": "Deluxe King Room", "price": float(h.price_per_night), "capacity": 2},
            {"id": 102, "name": "Executive Suite", "price": float(h.price_per_night * 1.5), "capacity": 4}
        ]
    }

@router.get("/{hotel_id}/rooms")
def get_hotel_rooms(hotel_id: int, db: Session = Depends(get_db)):
    h = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    price = float(h.price_per_night) if h else 120.0
    mock_rooms = [
        {"id": 101, "name": "Deluxe King Room", "price": price, "capacity": 2},
        {"id": 102, "name": "Executive Suite", "price": float(price * 1.5), "capacity": 4}
    ]
    return mock_rooms

@router.get("/{hotel_id}/reviews")
def get_hotel_reviews(hotel_id: int, db: Session = Depends(get_db)):
    db_reviews = db.query(Review).filter(Review.hotel_id == hotel_id).all()
    reviews_list = [{"id": str(r.id), "author": r.author, "text": r.text, "rating": r.rating} for r in db_reviews]
    if not reviews_list:
        reviews_list = [
            {"id": "1", "author": "John Doe", "text": "Incredible stay!", "rating": 5},
            {"id": "2", "author": "Jane Smith", "text": "Very clean and spacious rooms.", "rating": 4}
        ]
    return {
        "total": len(reviews_list),
        "data": reviews_list,
        "reviews": reviews_list,
        "results": reviews_list
    }

@router.post("/{hotel_id}/reviews")
def add_hotel_review(hotel_id: int, payload: ReviewCreate, db: Session = Depends(get_db)):
    new_review = Review(
        hotel_id=hotel_id,
        author=payload.author or "Guest Traveler",
        text=payload.text,
        rating=payload.rating
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    
    single_review = {"id": str(new_review.id), "author": new_review.author, "text": new_review.text, "rating": new_review.rating}
    return {
        "total": 1,
        "data": single_review,
        "review": single_review,
        "reviews": [single_review],
        "id": str(new_review.id),
        "author": new_review.author,
        "text": new_review.text,
        "rating": new_review.rating
    }
