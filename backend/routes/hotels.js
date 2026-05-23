const express = require("express");
const router = express.Router();
const { hotels } = require("../data/hotels");

// GET /api/hotels — search & filter
router.get("/", (req, res) => {
  const {
    city,
    amenities,     // comma-separated
    minPrice,
    maxPrice,
    stars,
    type,
    sort,
    q,             // free-text search
  } = req.query;

  let results = [...hotels];

  // Free-text search on name, location, description
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
    const minStars = Number(stars);
    results = results.filter((h) => h.stars >= minStars);
  }

  // Property type
  if (type) {
    results = results.filter(
      (h) => h.type.toLowerCase() === type.toLowerCase()
    );
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
      // Best match: rating weighted by reviews
      results.sort((a, b) => b.rating * Math.log(b.reviews) - a.rating * Math.log(a.reviews));
  }

  res.json({
    total: results.length,
    results,
  });
});

// GET /api/hotels/:id — single hotel
router.get("/:id", (req, res) => {
  const hotel = hotels.find((h) => h.id === req.params.id);
  if (!hotel) return res.status(404).json({ error: "Hotel not found" });
  res.json(hotel);
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

module.exports = router;
