from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from routes.hotels import router as hotels_router
from routes.bookings import router as bookings_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = FastAPI(title="Innsight API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "name": "Innsight API",
        "version": "1.0.0",
        "endpoints": {
            "hotels": {
                "list": "GET /api/hotels?city=&amenities=&minPrice=&maxPrice=&stars=&type=&sort=&q=",
                "single": "GET /api/hotels/{id}",
                "allAmenities": "GET /api/hotels/amenities/all",
                "allCities": "GET /api/hotels/cities/all",
            },
            "bookings": {
                "create": "POST /api/bookings",
                "list": "GET /api/bookings",
                "single": "GET /api/bookings/{id}",
                "modify": "PATCH /api/bookings/{id}",
                "cancel": "DELETE /api/bookings/{id}",
            },
        },
    }


app.include_router(hotels_router, prefix="/api/hotels")
app.include_router(bookings_router, prefix="/api/bookings")
