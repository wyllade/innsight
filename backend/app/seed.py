import json
from app.extensions import db
from app.models.hotel import Hotel
from app.models.booking import Booking


HOTELS = [
  {
    "id": "h001", "name": "The Nairobi Grand", "location": "Westlands, Nairobi",
    "country": "Kenya", "city": "Nairobi", "emoji": "castle",
    "badge": "Top Pick",
    "images": ["https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800","https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800","https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800"],
    "rooms": [{"type":"Deluxe King","pricePerNight":420,"maxGuests":2,"available":5},{"type":"Executive Suite","pricePerNight":630,"maxGuests":3,"available":3},{"type":"Presidential Penthouse","pricePerNight":1020,"maxGuests":4,"available":1}],
    "pricePerNight": 420, "rating": 4.9, "reviewsCount": 1284, "stars": 5, "hotelType": "Hotel",
    "amenities": ["Swimming Pool","Free WiFi","Gym","Breakfast","Spa","Restaurant","Bar"],
    "description": "A landmark of understated luxury rising above the Westlands skyline.",
    "checkIn": "14:00", "checkOut": "12:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","MPESA"], "cancellationPolicy": "free_cancellation", "lat": -1.2638, "lng": 36.8076
  },
  {
    "id": "h002", "name": "Savanna Boutique Hotel", "location": "Karen, Nairobi",
    "country": "Kenya", "city": "Nairobi", "emoji": "leaf",
    "badge": "Eco Friendly",
    "images": ["https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800","https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800"],
    "rooms": [{"type":"Garden Room","pricePerNight":248,"maxGuests":2,"available":4},{"type":"Terrace Suite","pricePerNight":330,"maxGuests":2,"available":2}],
    "pricePerNight": 248, "rating": 4.7, "reviewsCount": 843, "stars": 4, "hotelType": "Boutique",
    "amenities": ["Free WiFi","Breakfast","Parking","Restaurant","Pet Friendly"],
    "description": "Nestled in Karen's leafy suburb, Savanna Boutique is a solar-powered haven.",
    "checkIn": "14:00", "checkOut": "11:00", "petsAllowed": True, "smoking": False,
    "payments": ["Visa","Mastercard","MPESA"], "cancellationPolicy": "free_cancellation", "lat": -1.3187, "lng": 36.7103
  },
  {
    "id": "h003", "name": "Kizingo Sky Suites", "location": "Kilimani, Nairobi",
    "country": "Kenya", "city": "Nairobi", "emoji": "city",
    "badge": "New",
    "images": ["https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800","https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800","https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800"],
    "rooms": [{"type":"Studio Suite","pricePerNight":315,"maxGuests":2,"available":6},{"type":"Sky Loft","pricePerNight":510,"maxGuests":3,"available":2},{"type":"Corner Penthouse","pricePerNight":780,"maxGuests":4,"available":1}],
    "pricePerNight": 315, "rating": 4.8, "reviewsCount": 378, "stars": 5, "hotelType": "Hotel",
    "amenities": ["Swimming Pool","Free WiFi","Gym","Bar","Room Service","Conference"],
    "description": "Kizingo redefines the Nairobi city-break with floor-to-ceiling glass.",
    "checkIn": "15:00", "checkOut": "12:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","Amex","MPESA"], "cancellationPolicy": "partial_refund", "lat": -1.2864, "lng": 36.7857
  },
  {
    "id": "h004", "name": "Rift Valley Lodge", "location": "Limuru Road, Nairobi",
    "country": "Kenya", "city": "Nairobi", "emoji": "mountain",
    "badge": None,
    "images": ["https://images.unsplash.com/photo-1540541338287-41700207dee6?w=800","https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800"],
    "rooms": [{"type":"Standard Room","pricePerNight":480,"maxGuests":2,"available":8},{"type":"Premium Lodge","pricePerNight":720,"maxGuests":3,"available":4}],
    "pricePerNight": 480, "rating": 4.6, "reviewsCount": 561, "stars": 5, "hotelType": "Resort",
    "amenities": ["Swimming Pool","Free WiFi","Breakfast","Spa","Restaurant","Airport Shuttle","Parking"],
    "description": "Set on 14 acres of highland forest on the city's edge.",
    "checkIn": "14:00", "checkOut": "11:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","MPESA"], "cancellationPolicy": "partial_refund", "lat": -1.1667, "lng": 36.6167
  },
  {
    "id": "h005", "name": "Urban Rest Nairobi", "location": "CBD, Nairobi",
    "country": "Kenya", "city": "Nairobi", "emoji": "building",
    "badge": "Best Value",
    "images": ["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800","https://images.unsplash.com/photo-1505577058444-a3dab90d4253?w=800"],
    "rooms": [{"type":"Standard Single","pricePerNight":134,"maxGuests":1,"available":10},{"type":"Standard Double","pricePerNight":165,"maxGuests":2,"available":8}],
    "pricePerNight": 134, "rating": 4.3, "reviewsCount": 2109, "stars": 3, "hotelType": "Hotel",
    "amenities": ["Free WiFi","Gym","Breakfast","Parking"],
    "description": "No frills — just spotless rooms and the fastest WiFi in the CBD.",
    "checkIn": "14:00", "checkOut": "12:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","MPESA","Cash"], "cancellationPolicy": "free_cancellation", "lat": -1.2833, "lng": 36.8167
  },
  {
    "id": "h006", "name": "Pangani Heritage Inn", "location": "Pangani, Nairobi",
    "country": "Kenya", "city": "Nairobi", "emoji": "mosque",
    "badge": None,
    "images": ["https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?w=800","https://images.unsplash.com/photo-1606402179428-a57976d71fa4?w=800"],
    "rooms": [{"type":"Heritage Room","pricePerNight":195,"maxGuests":2,"available":5},{"type":"Colonial Suite","pricePerNight":285,"maxGuests":3,"available":2}],
    "pricePerNight": 195, "rating": 4.5, "reviewsCount": 447, "stars": 4, "hotelType": "Boutique",
    "amenities": ["Free WiFi","Breakfast","Restaurant","Bar","Room Service"],
    "description": "Built inside a restored 1940s colonial house with courtyard bar.",
    "checkIn": "13:00", "checkOut": "11:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","MPESA"], "cancellationPolicy": "free_cancellation", "lat": -1.272, "lng": 36.838
  },
  {
    "id": "h007", "name": "Mombasa Pearl Resort", "location": "Nyali, Mombasa",
    "country": "Kenya", "city": "Mombasa", "emoji": "beach",
    "badge": "Beachfront",
    "images": ["https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=800","https://images.unsplash.com/photo-1540541338287-41700207dee6?w=800","https://images.unsplash.com/photo-1551918120-9739cb430c6d?w=800"],
    "rooms": [{"type":"Ocean View Room","pricePerNight":368,"maxGuests":2,"available":6},{"type":"Beach Suite","pricePerNight":570,"maxGuests":3,"available":3},{"type":"Presidential Villa","pricePerNight":975,"maxGuests":5,"available":1}],
    "pricePerNight": 368, "rating": 4.8, "reviewsCount": 931, "stars": 5, "hotelType": "Resort",
    "amenities": ["Swimming Pool","Free WiFi","Breakfast","Spa","Restaurant","Bar","Parking","Airport Shuttle"],
    "description": "White coral sand and turquoise Indian Ocean at a full-service beachfront resort.",
    "checkIn": "14:00", "checkOut": "11:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","Amex","MPESA"], "cancellationPolicy": "partial_refund", "lat": -4.0435, "lng": 39.7195
  },
  {
    "id": "h008", "name": "Diani Beach House", "location": "Diani, Kwale County",
    "country": "Kenya", "city": "Diani", "emoji": "wave",
    "badge": None,
    "images": ["https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800","https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800"],
    "rooms": [{"type":"Garden Cottage","pricePerNight":278,"maxGuests":2,"available":4},{"type":"Oceanfront Villa","pricePerNight":435,"maxGuests":4,"available":2}],
    "pricePerNight": 278, "rating": 4.6, "reviewsCount": 302, "stars": 4, "hotelType": "Boutique",
    "amenities": ["Swimming Pool","Free WiFi","Breakfast","Restaurant","Parking","Pet Friendly"],
    "description": "An intimate 12-room house tucked behind a coral garden on Diani beach.",
    "checkIn": "14:00", "checkOut": "10:00", "petsAllowed": True, "smoking": False,
    "payments": ["Visa","Mastercard","MPESA"], "cancellationPolicy": "free_cancellation", "lat": -4.3167, "lng": 39.5667
  },
  {
    "id": "h009", "name": "Shibuya Capsule Tower", "location": "Shibuya, Tokyo",
    "country": "Japan", "city": "Tokyo", "emoji": "castle-jp",
    "badge": "Trending",
    "images": ["https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800","https://images.unsplash.com/photo-1536098561742-ca998e48cbcc?w=800","https://images.unsplash.com/photo-1566937169390-7adae16e4e2c?w=800"],
    "rooms": [{"type":"Capsule Pod","pricePerNight":180,"maxGuests":1,"available":12},{"type":"Zen Suite","pricePerNight":360,"maxGuests":2,"available":4},{"type":"Sky Penthouse","pricePerNight":630,"maxGuests":3,"available":2}],
    "pricePerNight": 180, "rating": 4.5, "reviewsCount": 1642, "stars": 4, "hotelType": "Boutique",
    "amenities": ["Free WiFi","Restaurant","Bar","Rooftop","Laundry","Concierge"],
    "description": "Eighteen floors of minimalist Japanese design above Shibuya Crossing.",
    "checkIn": "15:00", "checkOut": "11:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","Amex"], "cancellationPolicy": "free_cancellation", "lat": 35.6580, "lng": 139.7016
  },
  {
    "id": "h010", "name": "Le Rive Gauche", "location": "Saint-Germain, Paris",
    "country": "France", "city": "Paris", "emoji": "croissant",
    "badge": "Romantic",
    "images": ["https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800","https://images.unsplash.com/photo-1550340499-a6c60fc8280e?w=800","https://images.unsplash.com/photo-1453614512568-c4024d13c247?w=800"],
    "rooms": [{"type":"Classic Room","pricePerNight":525,"maxGuests":2,"available":6},{"type":"Balcony Suite","pricePerNight":870,"maxGuests":2,"available":3},{"type":"Penthouse Atelier","pricePerNight":1335,"maxGuests":4,"available":1}],
    "pricePerNight": 525, "rating": 4.8, "reviewsCount": 2156, "stars": 5, "hotelType": "Hotel",
    "amenities": ["Free WiFi","Breakfast","Bar","Room Service","Concierge","Valet Parking","Pet Friendly"],
    "description": "A quiet Saint-Germain side street hotel with creaking parquet and marble fireplaces.",
    "checkIn": "15:00", "checkOut": "12:00", "petsAllowed": True, "smoking": False,
    "payments": ["Visa","Mastercard","Amex"], "cancellationPolicy": "partial_refund", "lat": 48.8546, "lng": 2.3366
  },
  {
    "id": "h011", "name": "The Hudson Rest", "location": "Midtown, Manhattan",
    "country": "United States", "city": "New York", "emoji": "statue",
    "badge": "Top Pick",
    "images": ["https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=800","https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800","https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800"],
    "rooms": [{"type":"City Room","pricePerNight":375,"maxGuests":2,"available":10},{"type":"Executive King","pricePerNight":630,"maxGuests":2,"available":5},{"type":"Hudson Suite","pricePerNight":1125,"maxGuests":4,"available":2}],
    "pricePerNight": 375, "rating": 4.6, "reviewsCount": 3108, "stars": 4, "hotelType": "Hotel",
    "amenities": ["Free WiFi","Gym","Bar","Room Service","Concierge","Business Center","Restaurant"],
    "description": "Manhattan energy with floor-to-ceiling skyline views and a Bryant Park location.",
    "checkIn": "15:00", "checkOut": "12:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","Amex"], "cancellationPolicy": "free_cancellation", "lat": 40.7549, "lng": -73.9840
  },
  {
    "id": "h012", "name": "Harbour Glass Resort", "location": "Darling Harbour, Sydney",
    "country": "Australia", "city": "Sydney", "emoji": "kangaroo",
    "badge": "New",
    "images": ["https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=800","https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800","https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800"],
    "rooms": [{"type":"Harbour Room","pricePerNight":480,"maxGuests":2,"available":8},{"type":"Opera View Suite","pricePerNight":780,"maxGuests":3,"available":3},{"type":"Penthouse Marina","pricePerNight":1200,"maxGuests":4,"available":1}],
    "pricePerNight": 480, "rating": 4.9, "reviewsCount": 765, "stars": 5, "hotelType": "Resort",
    "amenities": ["Swimming Pool","Free WiFi","Breakfast","Gym","Restaurant","Bar","Parking","Airport Shuttle"],
    "description": "A shimmering glass crescent wrapped around Darling Harbour facing the Opera House.",
    "checkIn": "14:00", "checkOut": "11:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","Amex"], "cancellationPolicy": "partial_refund", "lat": -33.8727, "lng": 151.1988
  },
  {
    "id": "h013", "name": "Table Bay Haven", "location": "Victoria & Alfred Waterfront",
    "country": "South Africa", "city": "Cape Town", "emoji": "mountain",
    "badge": "Beachfront",
    "images": ["https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=800","https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800","https://images.unsplash.com/photo-1590490359683-658d3d23f972?w=800"],
    "rooms": [{"type":"Mountain View Room","pricePerNight":240,"maxGuests":2,"available":7},{"type":"Ocean Suite","pricePerNight":420,"maxGuests":3,"available":4},{"type":"Presidential Villa","pricePerNight":675,"maxGuests":5,"available":1}],
    "pricePerNight": 240, "rating": 4.7, "reviewsCount": 1194, "stars": 5, "hotelType": "Resort",
    "amenities": ["Swimming Pool","Free WiFi","Breakfast","Spa","Restaurant","Bar","Parking","Airport Shuttle"],
    "description": "Where Table Mountain meets the Atlantic at the V&A Waterfront.",
    "checkIn": "14:00", "checkOut": "11:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","Amex"], "cancellationPolicy": "free_cancellation", "lat": -33.9036, "lng": 18.4214
  },
  {
    "id": "h014", "name": "Ubud Canopy Retreat", "location": "Ubud, Bali",
    "country": "Indonesia", "city": "Bali", "emoji": "palm",
    "badge": "Eco Friendly",
    "images": ["https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=800","https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800","https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800"],
    "rooms": [{"type":"Jungle Bungalow","pricePerNight":180,"maxGuests":2,"available":5},{"type":"Rice Terrace Villa","pricePerNight":330,"maxGuests":3,"available":3},{"type":"Canopy Suite","pricePerNight":570,"maxGuests":4,"available":2}],
    "pricePerNight": 180, "rating": 4.7, "reviewsCount": 583, "stars": 4, "hotelType": "Resort",
    "amenities": ["Swimming Pool","Free WiFi","Breakfast","Spa","Restaurant","Bar","Pet Friendly"],
    "description": "Eleven bamboo-and-thatch villas suspended above the Ayung River gorge.",
    "checkIn": "14:00", "checkOut": "12:00", "petsAllowed": True, "smoking": False,
    "payments": ["Visa","Mastercard","Amex"], "cancellationPolicy": "free_cancellation", "lat": -8.5250, "lng": 115.2626
  },
  {
    "id": "h015", "name": "Aurora Glass Lodge", "location": "Thingvellir, Reykjavik",
    "country": "Iceland", "city": "Reykjavik", "emoji": "sparkles",
    "badge": "Top Pick",
    "images": ["https://images.unsplash.com/photo-1504214208698-ea1916a2195a?w=800","https://images.unsplash.com/photo-1520769669658-f07657f5a307?w=800","https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=800"],
    "rooms": [{"type":"Glass Cabin","pricePerNight":450,"maxGuests":2,"available":4},{"type":"Lava Suite","pricePerNight":720,"maxGuests":3,"available":2}],
    "pricePerNight": 450, "rating": 4.8, "reviewsCount": 621, "stars": 4, "hotelType": "Boutique",
    "amenities": ["Free WiFi","Breakfast","Spa","Restaurant","Bar","Parking","Hot Tub"],
    "description": "Six glass-roofed cabins scattered across a lava field in Thingvellir National Park.",
    "checkIn": "15:00", "checkOut": "11:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","Amex"], "cancellationPolicy": "partial_refund", "lat": 64.2550, "lng": -21.1325
  },
  {
    "id": "h016", "name": "Dar Essalam Riád", "location": "Medina, Marrakech",
    "country": "Morocco", "city": "Marrakech", "emoji": "mosque",
    "badge": "Romantic",
    "images": ["https://images.unsplash.com/photo-1597212618440-806262de4f6b?w=800","https://images.unsplash.com/photo-1590073242678-70ee3fc28f8e?w=800","https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800"],
    "rooms": [{"type":"Courtyard Room","pricePerNight":210,"maxGuests":2,"available":5},{"type":"Terrace Suite","pricePerNight":360,"maxGuests":2,"available":3},{"type":"Riad Royal","pricePerNight":600,"maxGuests":4,"available":1}],
    "pricePerNight": 210, "rating": 4.9, "reviewsCount": 847, "stars": 5, "hotelType": "Boutique",
    "amenities": ["Swimming Pool","Free WiFi","Breakfast","Spa","Restaurant","Bar","Airport Shuttle"],
    "description": "A 300-year-old riád hidden behind an unmarked door in the Marrakech Medina.",
    "checkIn": "14:00", "checkOut": "12:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","Cash"], "cancellationPolicy": "free_cancellation", "lat": 31.6311, "lng": -7.9885
  },
  {
    "id": "h017", "name": "Copacabana Palace", "location": "Copacabana, Rio de Janeiro",
    "country": "Brazil", "city": "Rio de Janeiro", "emoji": "beach",
    "badge": "Beachfront",
    "images": ["https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=800","https://images.unsplash.com/photo-1540541338287-41700207dee6?w=800","https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800"],
    "rooms": [{"type":"Ocean Room","pricePerNight":420,"maxGuests":2,"available":8},{"type":"Beach Suite","pricePerNight":675,"maxGuests":3,"available":4},{"type":"Presidential Suite","pricePerNight":1080,"maxGuests":4,"available":1}],
    "pricePerNight": 420, "rating": 4.7, "reviewsCount": 1342, "stars": 5, "hotelType": "Resort",
    "amenities": ["Swimming Pool","Free WiFi","Breakfast","Gym","Restaurant","Bar","Airport Shuttle","Spa"],
    "description": "Where Copacabana meets white marble — hosting diplomats and dreamers since 1923.",
    "checkIn": "14:00", "checkOut": "12:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","Amex"], "cancellationPolicy": "free_cancellation", "lat": -22.9711, "lng": -43.1823
  },
  {
    "id": "h018", "name": "Cancún Coral Resort", "location": "Zona Hotelera, Cancún",
    "country": "Mexico", "city": "Cancún", "emoji": "palm",
    "badge": "Top Pick",
    "images": ["https://images.unsplash.com/photo-1551918120-9739cb430c6d?w=800","https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800","https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800"],
    "rooms": [{"type":"Garden View Room","pricePerNight":330,"maxGuests":2,"available":10},{"type":"Oceanfront Suite","pricePerNight":570,"maxGuests":3,"available":5},{"type":"Royal Villa","pricePerNight":900,"maxGuests":5,"available":2}],
    "pricePerNight": 330, "rating": 4.6, "reviewsCount": 2018, "stars": 5, "hotelType": "Resort",
    "amenities": ["Swimming Pool","Free WiFi","Breakfast","Restaurant","Bar","Spa","Parking","Airport Shuttle"],
    "description": "Twelve acres of white sand with turquoise cenote-style pools.",
    "checkIn": "15:00", "checkOut": "11:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","Amex"], "cancellationPolicy": "partial_refund", "lat": 21.1619, "lng": -86.8515
  },
  {
    "id": "h019", "name": "Burj Sky Hotel", "location": "Downtown Dubai",
    "country": "United Arab Emirates", "city": "Dubai", "emoji": "building",
    "badge": "Luxury",
    "images": ["https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800","https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800","https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"],
    "rooms": [{"type":"Sky Room","pricePerNight":675,"maxGuests":2,"available":6},{"type":"Executive Suite","pricePerNight":1125,"maxGuests":3,"available":3},{"type":"Royal Penthouse","pricePerNight":1800,"maxGuests":5,"available":1}],
    "pricePerNight": 675, "rating": 4.9, "reviewsCount": 987, "stars": 5, "hotelType": "Hotel",
    "amenities": ["Swimming Pool","Free WiFi","Gym","Restaurant","Bar","Room Service","Spa","Parking","Concierge"],
    "description": "Rising 80 storeys above the Dubai Fountain with cloud-level hospitality.",
    "checkIn": "15:00", "checkOut": "12:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","Amex"], "cancellationPolicy": "partial_refund", "lat": 25.1972, "lng": 55.2744
  },
  {
    "id": "h020", "name": "Bangkok Spice Inn", "location": "Sukhumvit, Bangkok",
    "country": "Thailand", "city": "Bangkok", "emoji": "noodle",
    "badge": "Best Value",
    "images": ["https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800","https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800","https://images.unsplash.com/photo-1562778612-e1e0cda9915c?w=800"],
    "rooms": [{"type":"Standard Room","pricePerNight":128,"maxGuests":2,"available":14},{"type":"Deluxe Balcony","pricePerNight":210,"maxGuests":2,"available":6},{"type":"Sukhumvit Suite","pricePerNight":315,"maxGuests":3,"available":3}],
    "pricePerNight": 128, "rating": 4.4, "reviewsCount": 2673, "stars": 4, "hotelType": "Boutique",
    "amenities": ["Free WiFi","Breakfast","Restaurant","Bar","Rooftop","Laundry","Airport Shuttle"],
    "description": "A hidden laneway off Sukhumvit Soi 11 — the Bangkok you came for.",
    "checkIn": "14:00", "checkOut": "12:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","Cash"], "cancellationPolicy": "free_cancellation", "lat": 13.7367, "lng": 100.5603
  },
  {
    "id": "h021", "name": "Jaipur Maharaja Palace", "location": "Pink City, Jaipur",
    "country": "India", "city": "Jaipur", "emoji": "mosque",
    "badge": "Heritage",
    "images": ["https://images.unsplash.com/photo-1606402179428-a57976d71fa4?w=800","https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?w=800","https://images.unsplash.com/photo-1590073242678-70ee3fc28f8e?w=800"],
    "rooms": [{"type":"Royal Chamber","pricePerNight":285,"maxGuests":2,"available":5},{"type":"Maharaja Suite","pricePerNight":510,"maxGuests":3,"available":3},{"type":"Palace Penthouse","pricePerNight":870,"maxGuests":4,"available":1}],
    "pricePerNight": 285, "rating": 4.8, "reviewsCount": 756, "stars": 5, "hotelType": "Boutique",
    "amenities": ["Swimming Pool","Free WiFi","Breakfast","Restaurant","Bar","Spa","Parking","Room Service"],
    "description": "A restored 18th-century haveli in the heart of the Pink City.",
    "checkIn": "14:00", "checkOut": "11:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","Amex"], "cancellationPolicy": "free_cancellation", "lat": 26.9124, "lng": 75.7873
  },
  {
    "id": "h022", "name": "Hong Kong Harbour Peak", "location": "Central, Hong Kong",
    "country": "China", "city": "Hong Kong", "emoji": "city",
    "badge": "Trending",
    "images": ["https://images.unsplash.com/photo-1536098561742-ca998e48cbcc?w=800","https://images.unsplash.com/photo-1505577058444-a3dab90d4253?w=800","https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800"],
    "rooms": [{"type":"Harbour Room","pricePerNight":495,"maxGuests":2,"available":7},{"type":"Victoria Suite","pricePerNight":825,"maxGuests":3,"available":3},{"type":"Peak Penthouse","pricePerNight":1350,"maxGuests":4,"available":1}],
    "pricePerNight": 495, "rating": 4.7, "reviewsCount": 1102, "stars": 5, "hotelType": "Hotel",
    "amenities": ["Free WiFi","Gym","Restaurant","Bar","Room Service","Concierge","Business Center"],
    "description": "Forty floors above Victoria Harbour with Hong Kong's most famous skyline view.",
    "checkIn": "15:00", "checkOut": "12:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","Amex"], "cancellationPolicy": "partial_refund", "lat": 22.2825, "lng": 114.1581
  },
  {
    "id": "h023", "name": "The Mayfair London", "location": "Mayfair, London",
    "country": "United Kingdom", "city": "London", "emoji": "tophat",
    "badge": "Top Pick",
    "images": ["https://images.unsplash.com/photo-1453614512568-c4024d13c247?w=800","https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800","https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800"],
    "rooms": [{"type":"Classic Room","pricePerNight":570,"maxGuests":2,"available":6},{"type":"Park View Suite","pricePerNight":930,"maxGuests":2,"available":3},{"type":"Royal Mayfair","pricePerNight":1575,"maxGuests":4,"available":1}],
    "pricePerNight": 570, "rating": 4.8, "reviewsCount": 1820, "stars": 5, "hotelType": "Hotel",
    "amenities": ["Free WiFi","Breakfast","Gym","Restaurant","Bar","Room Service","Concierge","Pet Friendly"],
    "description": "An unassuming Georgian facade on a quiet Mayfair square with legendary afternoon tea.",
    "checkIn": "15:00", "checkOut": "12:00", "petsAllowed": True, "smoking": False,
    "payments": ["Visa","Mastercard","Amex"], "cancellationPolicy": "free_cancellation", "lat": 51.5072, "lng": -0.1404
  },
  {
    "id": "h024", "name": "Roma Dolce Vita", "location": "Trastevere, Rome",
    "country": "Italy", "city": "Rome", "emoji": "pasta",
    "badge": "Romantic",
    "images": ["https://images.unsplash.com/photo-1550340499-a6c60fc8280e?w=800","https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800","https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800"],
    "rooms": [{"type":"Trastevere Room","pricePerNight":390,"maxGuests":2,"available":5},{"type":"Terrace Suite","pricePerNight":630,"maxGuests":2,"available":3},{"type":"Dolce Vita Apartment","pricePerNight":975,"maxGuests":4,"available":1}],
    "pricePerNight": 390, "rating": 4.7, "reviewsCount": 1430, "stars": 4, "hotelType": "Boutique",
    "amenities": ["Free WiFi","Breakfast","Restaurant","Bar","Room Service","Concierge"],
    "description": "A cobblestone alley in Trastevere with a rooftop view of the Vatican.",
    "checkIn": "14:00", "checkOut": "11:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","Amex"], "cancellationPolicy": "free_cancellation", "lat": 41.8871, "lng": 12.4697
  },
  {
    "id": "h025", "name": "Barcelona Costa House", "location": "Barceloneta, Barcelona",
    "country": "Spain", "city": "Barcelona", "emoji": "building-eu",
    "badge": None,
    "images": ["https://images.unsplash.com/photo-1551918120-9739cb430c6d?w=800","https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800","https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800"],
    "rooms": [{"type":"Barceloneta Room","pricePerNight":300,"maxGuests":2,"available":6},{"type":"Costa Suite","pricePerNight":510,"maxGuests":3,"available":3},{"type":"Gaudi Penthouse","pricePerNight":780,"maxGuests":4,"available":1}],
    "pricePerNight": 300, "rating": 4.5, "reviewsCount": 967, "stars": 4, "hotelType": "Boutique",
    "amenities": ["Free WiFi","Breakfast","Restaurant","Bar","Rooftop","Airport Shuttle"],
    "description": "A converted fisherman's townhouse two blocks from Barceloneta beach.",
    "checkIn": "15:00", "checkOut": "11:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","Amex"], "cancellationPolicy": "free_cancellation", "lat": 41.3784, "lng": 2.1925
  },
  {
    "id": "h026", "name": "Nile Dream Hotel", "location": "Zamalek, Cairo",
    "country": "Egypt", "city": "Cairo", "emoji": "camel",
    "badge": "New",
    "images": ["https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=800","https://images.unsplash.com/photo-1562778612-e1e0cda9915c?w=800","https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800"],
    "rooms": [{"type":"Nile View Room","pricePerNight":225,"maxGuests":2,"available":8},{"type":"Pyramid Suite","pricePerNight":390,"maxGuests":3,"available":4},{"type":"Pharaoh Penthouse","pricePerNight":630,"maxGuests":4,"available":1}],
    "pricePerNight": 225, "rating": 4.5, "reviewsCount": 623, "stars": 4, "hotelType": "Hotel",
    "amenities": ["Swimming Pool","Free WiFi","Breakfast","Restaurant","Bar","Room Service","Airport Shuttle"],
    "description": "On leafy Zamalek island with feluccas drifting past your window on the Nile.",
    "checkIn": "14:00", "checkOut": "12:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","Cash"], "cancellationPolicy": "free_cancellation", "lat": 30.0647, "lng": 31.2202
  },
  {
    "id": "h027", "name": "Santorini Blue Dome", "location": "Oia, Santorini",
    "country": "Greece", "city": "Santorini", "emoji": "sunset",
    "badge": "Romantic",
    "images": ["https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800","https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800","https://images.unsplash.com/photo-1540541338287-41700207dee6?w=800"],
    "rooms": [{"type":"Caldera View Room","pricePerNight":510,"maxGuests":2,"available":5},{"type":"Sunset Suite","pricePerNight":840,"maxGuests":2,"available":3},{"type":"Blue Dome Villa","pricePerNight":1275,"maxGuests":4,"available":1}],
    "pricePerNight": 510, "rating": 4.9, "reviewsCount": 891, "stars": 5, "hotelType": "Resort",
    "amenities": ["Swimming Pool","Free WiFi","Breakfast","Restaurant","Bar","Spa","Airport Shuttle"],
    "description": "Carved into the Oia cliffside where whitewashed walls tumble towards the Aegean.",
    "checkIn": "15:00", "checkOut": "11:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","Amex"], "cancellationPolicy": "partial_refund", "lat": 36.4616, "lng": 25.3753
  },
  {
    "id": "h028", "name": "Marina Bay Suites", "location": "Marina Bay, Singapore",
    "country": "Singapore", "city": "Singapore", "emoji": "lion",
    "badge": "Luxury",
    "images": ["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800","https://images.unsplash.com/photo-1505577058444-a3dab90d4253?w=800","https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800"],
    "rooms": [{"type":"Harbour Room","pricePerNight":465,"maxGuests":2,"available":8},{"type":"Bay View Suite","pricePerNight":780,"maxGuests":3,"available":4},{"type":"Marina Penthouse","pricePerNight":1320,"maxGuests":4,"available":1}],
    "pricePerNight": 465, "rating": 4.8, "reviewsCount": 1254, "stars": 5, "hotelType": "Hotel",
    "amenities": ["Swimming Pool","Free WiFi","Gym","Restaurant","Bar","Room Service","Spa","Concierge","Business Center"],
    "description": "A gleaming Marina Bay tower where the infinity pool meets the Singapore Strait.",
    "checkIn": "15:00", "checkOut": "12:00", "petsAllowed": False, "smoking": False,
    "payments": ["Visa","Mastercard","Amex"], "cancellationPolicy": "partial_refund", "lat": 1.2834, "lng": 103.8607
  },
]


def seed_db(app):
    with app.app_context():
        if Hotel.query.first():
            return
        db.create_all()
        for h in HOTELS:
            hotel = Hotel(
                id=h["id"], name=h["name"], location=h["location"],
                country=h["country"], city=h["city"], emoji=h["emoji"],
                badge=h.get("badge"),
                images=json.dumps(h["images"]),
                rooms=json.dumps(h["rooms"]),
                price_per_night=h["pricePerNight"],
                rating=h["rating"], reviews_count=h["reviewsCount"],
                stars=h["stars"], hotel_type=h["hotelType"],
                amenities=json.dumps(h["amenities"]),
                description=h["description"],
                check_in=h["checkIn"], check_out=h["checkOut"],
                pets_allowed=h["petsAllowed"], smoking=h["smoking"],
                payments=json.dumps(h["payments"]),
                cancellation_policy=h["cancellationPolicy"],
                lat=h["lat"], lng=h["lng"]
            )
            db.session.add(hotel)
        db.session.commit()
        print(f"Seeded {len(HOTELS)} hotels")


if __name__ == "__main__":
    from app import create_app
    app = create_app()
    seed_db(app)
