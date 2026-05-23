const express = require("express");
const router = express.Router();
const { v4: uuidv4 } = require("uuid");
const { hotels, bookings } = require("../data/hotels");

// POST /api/bookings — create booking
router.post("/", (req, res) => {
  const { hotelId, checkIn, checkOut, guests, guestName, guestEmail } = req.body;

  // Validate required fields
  if (!hotelId || !checkIn || !checkOut || !guestName || !guestEmail) {
    return res.status(400).json({
      error: "Missing required fields: hotelId, checkIn, checkOut, guestName, guestEmail",
    });
  }

  // Validate hotel exists
  const hotel = hotels.find((h) => h.id === hotelId);
  if (!hotel) return res.status(404).json({ error: "Hotel not found" });

  // Validate dates
  const inDate = new Date(checkIn);
  const outDate = new Date(checkOut);
  if (isNaN(inDate) || isNaN(outDate))
    return res.status(400).json({ error: "Invalid date format. Use YYYY-MM-DD" });
  if (outDate <= inDate)
    return res.status(400).json({ error: "checkOut must be after checkIn" });

  // Calculate price
  const nights = Math.ceil((outDate - inDate) / (1000 * 60 * 60 * 24));
  const subtotal = nights * hotel.pricePerNight;
  const taxes = Math.round(subtotal * 0.16);
  const total = subtotal + taxes;

  const booking = {
    id: uuidv4(),
    hotelId,
    hotelName: hotel.name,
    hotelLocation: hotel.location,
    checkIn,
    checkOut,
    nights,
    guests: guests || 1,
    guestName,
    guestEmail,
    pricePerNight: hotel.pricePerNight,
    subtotal,
    taxes,
    total,
    status: "confirmed",
    createdAt: new Date().toISOString(),
  };

  bookings.push(booking);

  res.status(201).json({
    message: "Booking confirmed!",
    booking,
  });
});

// GET /api/bookings — list all bookings (admin)
router.get("/", (req, res) => {
  res.json({ total: bookings.length, bookings });
});

// GET /api/bookings/:id — get single booking
router.get("/:id", (req, res) => {
  const booking = bookings.find((b) => b.id === req.params.id);
  if (!booking) return res.status(404).json({ error: "Booking not found" });
  res.json(booking);
});

// DELETE /api/bookings/:id — cancel booking
router.delete("/:id", (req, res) => {
  const idx = bookings.findIndex((b) => b.id === req.params.id);
  if (idx === -1) return res.status(404).json({ error: "Booking not found" });
  bookings[idx].status = "cancelled";
  res.json({ message: "Booking cancelled", booking: bookings[idx] });
});

module.exports = router;
