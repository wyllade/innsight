import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, get_db
from app.models.hotel import Hotel
from app.models.booking import Booking
from app.models.review import Review
from app.routes import auth, hotels, bookings

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    if db.query(Hotel).count() == 0:
        cities = ["Nairobi", "Mombasa", "Kisumu", "Nakuru"]
        hotel_names = ["Grand Oasis", "Urban Edge", "Savannah Lodge", "Hilton View", "Coral Reef", "Rift Valley Pavilions", "Serene Palms", "The Horizon", "Sunset Bay", "Peak View", "Lakeside Retreat", "The Sovereign"]
        amenity_presets = [
            ["Swimming Pool", "Free WiFi", "Gym", "Breakfast", "Spa"],
            ["Free WiFi", "Gym", "Restaurant", "Bar", "Parking"],
            ["Breakfast", "Parking", "Restaurant", "Swimming Pool"],
            ["Free WiFi", "Gym", "Breakfast", "Restaurant"],
            ["Swimming Pool", "Free WiFi", "Spa", "Bar"],
            ["Swimming Pool", "Free WiFi", "Breakfast", "Gym"]
        ]
        for i in range(12):
            city = cities[i % len(cities)]
            name = f"{hotel_names[i]} Resort"
            price = 80.0 + (i * 15)
            rating = round(4.2 + (i * 0.06) % 0.8, 1)
            hotel_obj = Hotel(
                name=name,
                city=city,
                description=f"Welcome to {name} in beautiful {city}. Experience premier luxury, exceptional local dining, and top-tier amenities designed for ultimate comfort.",
                price_per_night=price,
                image_url="",
                rating=rating
            )
            hotel_obj.amenities = amenity_presets[i % len(amenity_presets)]
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
