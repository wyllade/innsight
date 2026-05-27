import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, get_db
from app.models.hotel import Hotel
from app.routes import hotels, bookings, auth

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

app.include_router(auth.router)
app.include_router(hotels.router)
app.include_router(bookings.router)

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=3001, reload=True)
