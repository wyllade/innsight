const express = require("express");
const router = express.Router();
const { v4: uuidv4 } = require("uuid");
const { hotels, bookings, reviews } = require("../data/hotels");

// POST /api/bookings — create booking
router.post("/", (req, res) => {
  const { hotelId, checkIn, checkOut, guests, guestName, guestEmail, roomType } = req.body;

  if (!hotelId || !checkIn || !checkOut || !guestName || !guestEmail) {
    return res.status(400).json({
      error: "Missing required fields: hotelId, checkIn, checkOut, guestName, guestEmail",
    });
  }

  const hotel = hotels.find((h) => h.id === hotelId);
  if (!hotel) return res.status(404).json({ error: "Hotel not found" });

  const inDate = new Date(checkIn);
  const outDate = new Date(checkOut);
  if (isNaN(inDate) || isNaN(outDate))
    return res.status(400).json({ error: "Invalid date format. Use YYYY-MM-DD" });
  if (outDate <= inDate)
    return res.status(400).json({ error: "checkOut must be after checkIn" });

  // Check availability — overlapping bookings
  const overlapping = bookings.filter(
    (b) =>
      b.hotelId === hotelId &&
      b.status !== "cancelled" &&
      new Date(b.checkIn) < outDate &&
      new Date(b.checkOut) > inDate
  );
  if (overlapping.length > 0) {
    return res.status(409).json({ error: "Hotel is not available for the selected dates" });
  }

  // Find room type if specified
  let pricePerNight = hotel.pricePerNight;
  let selectedRoom = null;
  if (roomType && hotel.rooms) {
    selectedRoom = hotel.rooms.find((r) => r.type.toLowerCase() === roomType.toLowerCase());
    if (selectedRoom) {
      pricePerNight = selectedRoom.pricePerNight;
      if (selectedRoom.available <= 0) {
        return res.status(409).json({ error: "Selected room type is sold out" });
      }
    }
  }

  // Validate guest count against max guests
  const numGuests = guests || 1;
  if (selectedRoom && numGuests > selectedRoom.maxGuests) {
    return res.status(400).json({
      error: `Selected room type (${selectedRoom.type}) max ${selectedRoom.maxGuests} guests`,
    });
  }

  const nights = Math.ceil((outDate - inDate) / (1000 * 60 * 60 * 24));
  const subtotal = nights * pricePerNight;
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
    guests: numGuests,
    guestName,
    guestEmail,
    roomType: selectedRoom ? selectedRoom.type : null,
    pricePerNight,
    subtotal,
    taxes,
    total,
    status: "confirmed",
    cancellationPolicy: hotel.cancellationPolicy || "non_refundable",
    createdAt: new Date().toISOString(),
  };

  bookings.push(booking);

  // Decrement room availability
  if (selectedRoom) {
    selectedRoom.available = Math.max(0, selectedRoom.available - 1);
  }

  res.status(201).json({ message: "Booking confirmed!", booking });
});

// GET /api/bookings — list all bookings
router.get("/", (req, res) => {
  const { email } = req.query;
  let result = bookings;
  if (email) {
    result = bookings.filter((b) => b.guestEmail.toLowerCase() === email.toLowerCase());
  }
  res.json({ total: result.length, bookings: result });
});

// GET /api/bookings/:id — get single booking
router.get("/:id", (req, res) => {
  const booking = bookings.find((b) => b.id === req.params.id);
  if (!booking) return res.status(404).json({ error: "Booking not found" });
  res.json(booking);
});

// PATCH /api/bookings/:id — modify booking (dates, guests)
router.patch("/:id", (req, res) => {
  const booking = bookings.find((b) => b.id === req.params.id);
  if (!booking) return res.status(404).json({ error: "Booking not found" });
  if (booking.status === "cancelled") {
    return res.status(400).json({ error: "Cannot modify a cancelled booking" });
  }

  const { checkIn, checkOut, guests } = req.body;
  if (checkIn) booking.checkIn = checkIn;
  if (checkOut) booking.checkOut = checkOut;
  if (guests) booking.guests = guests;

  // Recalculate price
  const inDate = new Date(booking.checkIn);
  const outDate = new Date(booking.checkOut);
  if (!isNaN(inDate) && !isNaN(outDate) && outDate > inDate) {
    const nights = Math.ceil((outDate - inDate) / (1000 * 60 * 60 * 24));
    booking.nights = nights;
    booking.subtotal = nights * booking.pricePerNight;
    booking.taxes = Math.round(booking.subtotal * 0.16);
    booking.total = booking.subtotal + booking.taxes;
  }

  res.json({ message: "Booking updated", booking });
});

// DELETE /api/bookings/:id — cancel booking
router.delete("/:id", (req, res) => {
  const idx = bookings.findIndex((b) => b.id === req.params.id);
  if (idx === -1) return res.status(404).json({ error: "Booking not found" });
  bookings[idx].status = "cancelled";
  res.json({ message: "Booking cancelled", booking: bookings[idx] });
});

module.exports = router;
