# 🏨 Innsight — Hotel Discovery App

Full-stack hotel discovery web application built with **Node.js / Express** (backend) and **Vanilla JS** (frontend).

---

## Project Structure

```
innsight/
├── backend/
│   ├── server.js              # Express entry point
│   ├── package.json
│   ├── data/
│   │   └── hotels.js          # Hotel seed data + in-memory bookings store
│   ├── routes/
│   │   ├── hotels.js          # GET /api/hotels, /api/hotels/:id, /amenities/all
│   │   └── bookings.js        # POST/GET/DELETE /api/bookings
│   └── middleware/
│       └── errorHandler.js    # Request logger, error handler, 404
└── frontend/
    ├── package.json
    └── public/
        ├── index.html         # Full SPA — Landing, Results, Detail pages
        └── api.js             # API client (fetch wrapper)
```

---

## Quick Start

### 1. Start the Backend

```bash
cd backend
npm install
npm run dev        # uses nodemon for auto-reload
# OR
npm start          # plain node
```

Backend runs at **http://localhost:3001**

### 2. Start the Frontend

```bash
cd frontend
npm install
npm start
```

Frontend runs at **http://localhost:3000**

Open http://localhost:3000 in your browser.

---

## API Reference

### Base URL
```
http://localhost:3001
```

### Hotels

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/hotels` | List/search hotels with filters |
| GET | `/api/hotels/:id` | Get a single hotel |
| GET | `/api/hotels/amenities/all` | All unique amenities |
| GET | `/api/hotels/cities/all` | All cities |

#### Query Parameters — `GET /api/hotels`

| Param | Type | Description |
|-------|------|-------------|
| `q` | string | Free-text search (name, location, description, amenities) |
| `city` | string | Filter by city name |
| `amenities` | string | Comma-separated amenities e.g. `Swimming Pool,Gym` |
| `minPrice` | number | Minimum price per night |
| `maxPrice` | number | Maximum price per night |
| `stars` | number | Minimum star rating (3, 4, or 5) |
| `type` | string | Property type: Hotel, Resort, Boutique, Hostel |
| `sort` | string | `price_asc`, `price_desc`, `rating`, `reviews` |

#### Example Requests

```bash
# Search Nairobi hotels with pool and gym under $300
curl "http://localhost:3001/api/hotels?city=Nairobi&amenities=Swimming Pool,Gym&maxPrice=300"

# Top rated hotels
curl "http://localhost:3001/api/hotels?sort=rating"

# Full text search
curl "http://localhost:3001/api/hotels?q=beachfront"
```

### Bookings

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/bookings` | Create a booking |
| GET | `/api/bookings` | List all bookings |
| GET | `/api/bookings/:id` | Get a booking by ID |
| DELETE | `/api/bookings/:id` | Cancel a booking |

#### POST `/api/bookings` — Request Body

```json
{
  "hotelId": "h001",
  "checkIn": "2025-09-01",
  "checkOut": "2025-09-05",
  "guests": 2,
  "guestName": "Jane Mwangi",
  "guestEmail": "jane@example.com"
}
```

#### Response

```json
{
  "message": "Booking confirmed!",
  "booking": {
    "id": "uuid-here",
    "hotelId": "h001",
    "hotelName": "The Nairobi Grand",
    "checkIn": "2025-09-01",
    "checkOut": "2025-09-05",
    "nights": 4,
    "guests": 2,
    "guestName": "Jane Mwangi",
    "subtotal": 1120,
    "taxes": 179,
    "total": 1299,
    "status": "confirmed",
    "createdAt": "2025-05-23T10:00:00.000Z"
  }
}
```

---

## What's Built

### Frontend (SPA — no framework)
- **Landing page** — hero search with amenity pills, live stats from API
- **Results page** — sidebar filters (price, stars, type, amenities) + hotel grid
- **Detail page** — hotel info, full amenity list, policies, live booking form with price calc
- **Booking confirmation** — modal with full booking summary
- **Offline mode** — graceful fallback if API is unreachable

### Backend (Express REST API)
- Full search & filter engine (7 parameters)
- Smart default sort (rating × log(reviews))
- Booking validation (dates, required fields, price calculation)
- 16% tax auto-calculation
- Request logging middleware
- Global error handler

---

## Next Steps / Roadmap

- [ ] Add a database (SQLite → PostgreSQL)
- [ ] User authentication (JWT)
- [ ] Image upload for hotel photos
- [ ] Google Maps / Mapbox integration
- [ ] Email confirmation (Nodemailer / SendGrid)
- [ ] Admin dashboard for hotel management
- [ ] Review & rating system
- [ ] MPESA payment integration (Daraja API)
