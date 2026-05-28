from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
from typing import Optional
from app.database import get_db
from app.models.hotel import Hotel

router = APIRouter(prefix="/api/hotels", tags=["Hotels"])


def _find_by_public_id(db: Session, public_id: str):
    hotel = db.query(Hotel).filter(Hotel.public_id == public_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel


@router.get("")
def get_hotels(
    city: Optional[str] = None,
    q: Optional[str] = None,
    amenities: Optional[str] = None,
    minPrice: Optional[float] = None,
    maxPrice: Optional[float] = None,
    stars: Optional[int] = None,
    type: Optional[str] = None,
    sort: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Hotel)

    if city:
        query = query.filter(Hotel.city.ilike(f"%{city}%"))
    if q:
        query = query.filter(
            Hotel.name.ilike(f"%{q}%") | Hotel.description.ilike(f"%{q}%")
        )
    if minPrice is not None:
        query = query.filter(Hotel.price_per_night >= minPrice)
    if maxPrice is not None:
        query = query.filter(Hotel.price_per_night <= maxPrice)
    if stars is not None:
        query = query.filter(Hotel.stars >= stars)
    if type:
        types = [t.strip() for t in type.split(",")]
        query = query.filter(Hotel.hotel_type.in_(types))

    # Amenities filter (Python-side)
    if amenities:
        wanted = [a.strip().lower() for a in amenities.split(",")]
        all_h = query.all()
        filtered = []
        for h in all_h:
            h_amenities = [a.lower() for a in h.amenities]
            if any(a in h_amenities for a in wanted):
                filtered.append(h)
        hotel_ids = [h.id for h in filtered]
        query = db.query(Hotel).filter(Hotel.id.in_(hotel_ids))

    # Sorting
    if sort == "price_asc":
        query = query.order_by(Hotel.price_per_night.asc())
    elif sort == "price_desc":
        query = query.order_by(Hotel.price_per_night.desc())
    elif sort == "rating":
        query = query.order_by(Hotel.rating.desc())
    elif sort == "reviews":
        query = query.order_by(Hotel.reviews_count.desc())

    total = query.count()
    total_pages = (total + limit - 1) // limit
    hotels = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "totalPages": total_pages,
        "results": [h.to_dict() for h in hotels],
    }


@router.get("/featured")
def get_featured(db: Session = Depends(get_db)):
    hotels = db.query(Hotel).order_by(Hotel.rating.desc()).limit(6).all()
    return [h.to_dict() for h in hotels]


@router.get("/amenities/all")
def get_all_amenities(db: Session = Depends(get_db)):
    hotels = db.query(Hotel).all()
    all_set = set()
    for h in hotels:
        all_set.update(h.amenities)
    return sorted(all_set)


@router.get("/cities/all")
def get_all_cities(db: Session = Depends(get_db)):
    results = db.query(Hotel.city).distinct().all()
    return sorted([r[0] for r in results if r[0]])


@router.get("/{public_id}")
def get_hotel(public_id: str, db: Session = Depends(get_db)):
    hotel = _find_by_public_id(db, public_id)
    return hotel.to_dict()


@router.get("/{public_id}/rooms")
def get_hotel_rooms(public_id: str, db: Session = Depends(get_db)):
    hotel = _find_by_public_id(db, public_id)
    return {"rooms": hotel.rooms}


@router.get("/{public_id}/reviews")
def get_hotel_reviews(public_id: str):
    return {"reviews": []}


@router.post("/{public_id}/reviews")
def add_hotel_review(public_id: str, body: dict, db: Session = Depends(get_db)):
    _find_by_public_id(db, public_id)
    return {
        "review": {
            "id": f"r{datetime.utcnow().strftime('%y%m%d%H%M%S')}",
            "hotelId": public_id,
            "author": body.get("author", "Anonymous"),
            "rating": body.get("rating", 5),
            "text": body.get("text", ""),
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
        }
    }


@router.get("/{public_id}/availability")
def check_availability(public_id: str, db: Session = Depends(get_db)):
    hotel = _find_by_public_id(db, public_id)
    return {"available": True, "rooms": hotel.rooms}
