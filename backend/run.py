import json
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional

from app.database import Base, engine, get_db
from app.models.hotel import Hotel

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    if db.query(Hotel).count() == 0:
        sample_hotels = [
            {
                "name": "The Grand Oasis Resort",
                "city": "Nairobi",
                "description": "Luxurious stay with breathtaking views of the skyline and an incredible rooftop swimming pool.",
                "price_per_night": 150.0,
                "image_url": "https://unsplash.com",
                "rating": 4.8,
                "amenities": ["Swimming Pool", "Free WiFi", "Gym", "Breakfast", "Spa"]
            },
            {
                "name": "Urban Edge Boutique Hotel",
                "city": "Mombasa",
                "description": "Modern minimalism right next to the shorelines. Perfect for remote workers and travelers.",
                "price_per_night": 95.0,
                "image_url": "https://unsplash.com",
                "rating": 4.5,
                "amenities": ["Free WiFi", "Gym", "Restaurant", "Bar", "Parking"]
            },
            {
                "name": "Savannah Eco Lodge",
                "city": "Nanyuki",
                "description": "Unplug from the world and connect with nature in this highly sustainable eco lodge.",
                "price_per_night": 210.0,
                "image_url": "https://unsplash.com",
                "rating": 4.9,
                "amenities": ["Breakfast", "Parking", "Restaurant", "Swimming Pool"]
            }
        ]
        for h in sample_hotels:
            hotel_obj = Hotel(
                name=h["name"],
                city=h["city"],
                description=h["description"],
                price_per_night=h["price_per_night"],
                image_url=h["image_url"],
                rating=h["rating"]
            )
            hotel_obj.amenities = h["amenities"]
            db.add(hotel_obj)
        db.commit()
    db.close()
    yield

app = FastAPI(title="INNSIGHT API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/hotels")
def get_hotels(
    city: Optional[str] = None,
    amenities: Optional[str] = None,
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
        "image_url": h.image_url,
        "rating": h.rating,
        "amenities": h.amenities
    } for h in hotels]

    return {
        "total": len(output_data),
        "data": output_data
    }

@app.get("/api/hotels/featured")
def get_featured_hotels(db: Session = Depends(get_db)):
    hotels = db.query(Hotel).filter(Hotel.rating >= 4.7).all()
    return [{
        "id": h.id,
        "name": h.name,
        "city": h.city,
        "description": h.description,
        "price_per_night": h.price_per_night,
        "image_url": h.image_url,
        "rating": h.rating,
        "amenities": h.amenities
    } for h in hotels]

@app.get("/api/hotels/amenities/all")
def get_all_amenities(db: Session = Depends(get_db)):
    hotels = db.query(Hotel).all()
    amenities_set = set()
    for h in hotels:
        amenities_set.update(h.amenities)
    return list(amenities_set)

@app.get("/api/hotels/cities/all")
def get_all_cities(db: Session = Depends(get_db)):
    results = db.query(Hotel.city).distinct().all()
    return [r for r in results]

@app.get("/api/hotels/{hotel_id}")
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    h = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not h:
        return {"error": "Hotel not found"}
    return {
        "id": h.id,
        "name": h.name,
        "city": h.city,
        "description": h.description,
        "price_per_night": h.price_per_night,
        "image_url": h.image_url,
        "rating": h.rating,
        "amenities": h.amenities
    }

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=3001, reload=True)
