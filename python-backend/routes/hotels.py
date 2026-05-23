from fastapi import APIRouter, Query
from data.hotels import hotels
from middleware.error_handler import filter_hotels

router = APIRouter()


@router.get("")
def list_hotels(
    q: str = Query(""),
    city: str = Query(""),
    amenities: str = Query(""),
    minPrice: str = Query(""),
    maxPrice: str = Query(""),
    stars: str = Query(""),
    type: str = Query(""),
    sort: str = Query(""),
):
    results = filter_hotels(
        hotels, q, city, amenities, minPrice, maxPrice, stars, type, sort
    )
    return {"total": len(results), "results": results}


@router.get("/{hotel_id}")
def get_hotel(hotel_id: str):
    for h in hotels:
        if h["id"] == hotel_id:
            return h
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Hotel not found")


@router.get("/amenities/all")
def get_amenities():
    all_amenities = sorted(set(a for h in hotels for a in h["amenities"]))
    return all_amenities


@router.get("/cities/all")
def get_cities():
    cities = sorted(set(h["city"] for h in hotels))
    return cities
