const express = require("express");
const router = express.Router();
const { hotels, bookings, reviews: allReviews } = require("../data/hotels");

// GET /api/hotels — search & filter
router.get("/", (req, res) => {
  const {
    city, amenities, minPrice, maxPrice, stars, type, sort, q,
    checkIn, checkOut, country, page: pageStr, limit: limitStr,
  } = req.query;

  let results = [...hotels];

  // Free-text search
  if (q) {
    const lq = q.toLowerCase();
    results = results.filter(
      (h) =>
        h.name.toLowerCase().includes(lq) ||
        h.location.toLowerCase().includes(lq) ||
        h.description.toLowerCase().includes(lq) ||
        h.amenities.some((a) => a.toLowerCase().includes(lq))
    );
  }

  // City filter
  if (city) {
    results = results.filter((h) =>
      h.city.toLowerCase().includes(city.toLowerCase())
    );
  }

  // Country filter
  if (country) {
    const lc = country.toLowerCase();
    results = results.filter((h) => h.country.toLowerCase().includes(lc));
  }

  // Amenity filter
  if (amenities) {
    const requested = amenities.split(",").map((a) => a.trim().toLowerCase());
    results = results.filter((h) =>
      requested.every((ra) =>
        h.amenities.some((ha) => ha.toLowerCase().includes(ra))
      )
    );
  }

  // Price range
  if (minPrice) results = results.filter((h) => h.pricePerNight >= Number(minPrice));
  if (maxPrice) results = results.filter((h) => h.pricePerNight <= Number(maxPrice));

  // Stars filter
  if (stars) {
    results = results.filter((h) => h.stars >= Number(stars));
  }

  // Property type — support comma-separated
  if (type) {
    const types = type.split(",").map((t) => t.trim().toLowerCase());
    results = results.filter((h) => types.includes(h.type.toLowerCase()));
  }

  // Availability check — filter out hotels with overlapping bookings
  if (checkIn && checkOut) {
    const inDate = new Date(checkIn);
    const outDate = new Date(checkOut);
    if (!isNaN(inDate) && !isNaN(outDate) && outDate > inDate) {
      results = results.filter((h) => {
        const overlapping = bookings.filter(
          (b) =>
            b.hotelId === h.id &&
            b.status !== "cancelled" &&
            new Date(b.checkIn) < outDate &&
            new Date(b.checkOut) > inDate
        );
        return overlapping.length === 0;
      });
    }
  }

  // Sorting
  switch (sort) {
    case "price_asc":
      results.sort((a, b) => a.pricePerNight - b.pricePerNight);
      break;
    case "price_desc":
      results.sort((a, b) => b.pricePerNight - a.pricePerNight);
      break;
    case "rating":
      results.sort((a, b) => b.rating - a.rating);
      break;
    case "reviews":
      results.sort((a, b) => b.reviews - a.reviews);
      break;
    default:
      // Best match: rating weighted by log10(reviews) — aligned with Python
      results.sort((a, b) => {
        const scoreA = a.rating * Math.log10(a.reviews + 1);
        const scoreB = b.rating * Math.log10(b.reviews + 1);
        return scoreB - scoreA;
      });
  }

  // Pagination
  const page = Math.max(1, parseInt(pageStr) || 1);
  const limit = Math.min(100, Math.max(1, parseInt(limitStr) || 20));
  const total = results.length;
  const totalPages = Math.ceil(total / limit);
  const start = (page - 1) * limit;
  const paginated = results.slice(start, start + limit);

  res.json({ total, page, limit, totalPages, results: paginated });
});

// GET /api/hotels/featured — top hotels for landing page
router.get("/featured", (req, res) => {
  const featured = [...hotels]
    .sort((a, b) => b.rating * Math.log10(b.reviews + 1) - a.rating * Math.log10(a.reviews + 1))
    .slice(0, 4);
  res.json({ total: featured.length, results: featured });
});

// GET /api/hotels/amenities/all — list all unique amenities
router.get("/amenities/all", (req, res) => {
  const all = [...new Set(hotels.flatMap((h) => h.amenities))].sort();
  res.json(all);
});

// GET /api/hotels/cities/all — list all cities
router.get("/cities/all", (req, res) => {
  const cities = [...new Set(hotels.map((h) => h.city))].sort();
  res.json(cities);
});

// GET /api/hotels/:id/rooms — room types for a hotel
router.get("/:id/rooms", (req, res) => {
  const hotel = hotels.find((h) => h.id === req.params.id);
  if (!hotel) return res.status(404).json({ error: "Hotel not found" });
  res.json({ rooms: hotel.rooms || [] });
});

// GET /api/hotels/:id/reviews — list reviews for a hotel
router.get("/:id/reviews", (req, res) => {
  const hotel = hotels.find((h) => h.id === req.params.id);
  if (!hotel) return res.status(404).json({ error: "Hotel not found" });
  const hotelReviews = allReviews.filter((r) => r.hotelId === req.params.id);
  res.json({ total: hotelReviews.length, reviews: hotelReviews });
});

// POST /api/hotels/:id/reviews — add a review
router.post("/:id/reviews", (req, res) => {
  const hotel = hotels.find((h) => h.id === req.params.id);
  if (!hotel) return res.status(404).json({ error: "Hotel not found" });

  const { author, rating, text } = req.body;
  if (!author || !rating || !text) {
    return res.status(400).json({ error: "Missing required fields: author, rating, text" });
  }

  const numRating = Number(rating);
  if (numRating < 1 || numRating > 5) {
    return res.status(400).json({ error: "Rating must be between 1 and 5" });
  }

  const review = {
    id: "r" + Date.now(),
    hotelId: req.params.id,
    author: author.trim(),
    rating: numRating,
    text: text.trim(),
    date: new Date().toISOString().split("T")[0],
  };

  allReviews.push(review);

  // Update hotel's average rating and review count
  const hotelReviews = allReviews.filter((r) => r.hotelId === req.params.id);
  const avgRating = hotelReviews.reduce((s, r) => s + r.rating, 0) / hotelReviews.length;
  hotel.rating = Math.round(avgRating * 10) / 10;
  hotel.reviews = hotelReviews.length;

  res.status(201).json({ message: "Review added", review });
});

// GET /api/hotels/:id/availability — check date availability
router.get("/:id/availability", (req, res) => {
  const hotel = hotels.find((h) => h.id === req.params.id);
  if (!hotel) return res.status(404).json({ error: "Hotel not found" });

  const { checkIn, checkOut } = req.query;
  if (!checkIn || !checkOut) {
    return res.status(400).json({ error: "checkIn and checkOut are required" });
  }

  const inDate = new Date(checkIn);
  const outDate = new Date(checkOut);
  if (isNaN(inDate) || isNaN(outDate) || outDate <= inDate) {
    return res.status(400).json({ error: "Invalid date range" });
  }

  const overlapping = bookings.filter(
    (b) =>
      b.hotelId === hotel.id &&
      b.status !== "cancelled" &&
      new Date(b.checkIn) < outDate &&
      new Date(b.checkOut) > inDate
  );

  res.json({
    hotelId: hotel.id,
    checkIn,
    checkOut,
    available: overlapping.length === 0,
    overlappingBookings: overlapping.length,
  });
});

// GET /api/hotels/:id — single hotel
router.get("/:id", (req, res) => {
  const hotel = hotels.find((h) => h.id === req.params.id);
  if (!hotel) return res.status(404).json({ error: "Hotel not found" });
  res.json(hotel);
});

module.exports = router;
