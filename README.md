# 🏨 Innsight — Hotel Discovery App

Full-stack hotel discovery web application with **React** (frontend), **Node.js / Express** (backend), and **Python / FastAPI** (parallel backend).

---

## Project Structure

```
innsight/
├── backend/                     # Node.js / Express API (port 3001)
│   ├── server.js
│   ├── data/hotels.js
│   ├── routes/hotels.js
│   ├── routes/bookings.js
│   └── middleware/errorHandler.js
├── python-backend/              # Python / FastAPI API (port 3002)
│   ├── main.py
│   ├── requirements.txt
│   ├── data/hotels.py
│   ├── routes/hotels.py
│   ├── routes/bookings.py
│   ├── models/hotel.py
│   ├── models/booking.py
│   └── middleware/error_handler.py
└── frontend/                    # React SPA (Vite, port 3000)
    ├── src/
    │   ├── main.jsx
    │   ├── App.jsx              # Router + ToastProvider
    │   ├── App.css              # Full design system
    │   ├── api.js               # API client (env-configurable base URL)
    │   ├── pages/
    │   │   ├── Landing.jsx      # Hero search, amenity pills, stats
    │   │   ├── Results.jsx      # Sidebar filters + hotel grid
    │   │   └── Detail.jsx       # Hotel info + booking form
    │   └── components/
    │       ├── Navbar.jsx
    │       ├── HotelCard.jsx
    │       ├── BookingModal.jsx
    │       ├── Toast.jsx
    │       └── Spinner.jsx
    ├── index.html
    ├── vite.config.js
    └── package.json
```

---

## Quick Start

### 1. Choose a Backend

**Option A — Node.js (Express) on port 3001:**
```bash
cd backend
npm install
npm run dev        # nodemon for auto-reload
```

**Option B — Python (FastAPI) on port 3002:**
```bash
cd python-backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 3002
```

### 2. Start the Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at **http://localhost:3000**

By default the React app calls `http://localhost:3001` (Node.js). To switch to the Python backend:
```bash
# On Windows PowerShell:
$env:VITE_API_URL="http://localhost:3002"
npm run dev

# On Mac/Linux:
VITE_API_URL=http://localhost:3002 npm run dev
```

---

## API Reference

Both backends expose the same endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/hotels` | List/search hotels with filters |
| GET | `/api/hotels/:id` | Get a single hotel |
| GET | `/api/hotels/amenities/all` | All unique amenities |
| GET | `/api/hotels/cities/all` | All cities |
| POST | `/api/bookings` | Create a booking |
| GET | `/api/bookings` | List all bookings |
| GET | `/api/bookings/:id` | Get a booking |
| DELETE | `/api/bookings/:id` | Cancel a booking |

### Query Parameters — `GET /api/hotels`

| Param | Type | Description |
|-------|------|-------------|
| `q` | string | Free-text search |
| `city` | string | Filter by city name |
| `amenities` | string | Comma-separated amenities |
| `minPrice` | number | Minimum price per night |
| `maxPrice` | number | Maximum price per night |
| `stars` | number | Minimum star rating (3, 4, 5) |
| `type` | string | Property type: Hotel, Resort, Boutique, Hostel |
| `sort` | string | `price_asc`, `price_desc`, `rating`, `reviews` |

---

## Features

- **Landing page** — hero search with amenity pills, live stats from API
- **Results page** — sidebar filters (price, stars, type, amenities) + hotel grid with sort
- **URL-persisted filters** — all search params in the URL (bookmarkable/shareable)
- **Detail page** — full hotel info, amenity grid, policies, booking form with live price calc
- **Booking confirmation** — modal with full booking summary
- **Loading/empty/error states** — consistent UX across all pages
- **Offline mode** — graceful fallback if API is unreachable
- **Parallel backends** — Node.js or Python, switch via environment variable
