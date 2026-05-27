import json
import uvicorn
import jwt
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

from app.database import Base, engine, get_db
from app.models.hotel import Hotel
from app.models.booking import Booking
from app.models.user import User

SECRET_KEY = "super-secret-key-change-in-production"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class BookingCreate(BaseModel):
    hotel_id: int
    checkin_date: str
    checkout_date: str
    total_price: float

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

def get_current_user_email(token: Optional[str] = Depends(oauth2_scheme)):
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except jwt.PyJWTError:
        return None

@app.post("/api/auth/register")
def register(payload: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(payload.password)
    new_user = User(email=payload.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@app.post("/api/auth/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not pwd_context.verify(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token_expiry = datetime.utcnow() + timedelta(days=1)
    token_data = {"sub": user.email, "exp": token_expiry}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"email": user.email}
    }

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
        raise HTTPException(status_code=404, detail="Hotel not found")
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

@app.post("/api/bookings")
def create_booking(
    payload: BookingCreate, 
    db: Session = Depends(get_db),
    current_user_email: Optional[str] = Depends(get_current_user_email),
    fallback_email: Optional[str] = Query(None)
):
    email_to_link = current_user_email or fallback_email
    if not email_to_link:
        raise HTTPException(status_code=401, detail="Authentication required or fallback email must be provided")

    hotel = db.query(Hotel).filter(Hotel.id == payload.hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    
    booking_obj = Booking(
        hotel_id=payload.hotel_id,
        user_email=email_to_link,
        checkin_date=payload.checkin_date,
        checkout_date=payload.checkout_date,
        total_price=payload.total_price
    )
    db.add(booking_obj)
    db.commit()
    db.refresh(booking_obj)
    return {
        "id": booking_obj.id,
        "hotel_id": booking_obj.hotel_id,
        "hotel_name": hotel.name,
        "user_email": booking_obj.user_email,
        "checkin_date": booking_obj.checkin_date,
        "checkout_date": booking_obj.checkout_date,
        "total_price": booking_obj.total_price,
        "status": booking_obj.status,
        "message": "booked"
    }

@app.get("/api/bookings")
def get_bookings(
    db: Session = Depends(get_db),
    current_user_email: Optional[str] = Depends(get_current_user_email),
    fallback_email: Optional[str] = Query(None)
):
    email_to_query = current_user_email or fallback_email
    if not email_to_query:
        raise HTTPException(status_code=401, detail="Authentication required or fallback email query parameter missing")

    bookings = db.query(Booking).filter(Booking.user_email == email_to_query).all()
    output_data = []
    for b in bookings:
        hotel = db.query(Hotel).filter(Hotel.id == b.hotel_id).first()
        output_data.append({
            "id": b.id,
            "hotel_id": b.hotel_id,
            "hotel_name": hotel.name if hotel else "Unknown Hotel",
            "image_url": hotel.image_url if hotel else None,
            "user_email": b.user_email,
            "checkin_date": b.checkin_date,
            "checkout_date": b.checkout_date,
            "total_price": b.total_price,
            "status": b.status
        })
    return output_data

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=3001, reload=True)
