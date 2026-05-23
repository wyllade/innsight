import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { API } from "../api.js";
import { amenityIcon, GRADIENTS } from "../components/HotelCard.jsx";
import BookingModal from "../components/BookingModal.jsx";
import Spinner from "../components/Spinner.jsx";
import { useToast } from "../components/Toast.jsx";

export default function Detail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const showToast = useToast();

  const [hotel, setHotel] = useState(null);
  const [rooms, setRooms] = useState([]);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [booking, setBooking] = useState(null);

  const [checkin, setCheckin] = useState("");
  const [checkout, setCheckout] = useState("");
  const [guestName, setGuestName] = useState("");
  const [guestEmail, setGuestEmail] = useState("");
  const [guests, setGuests] = useState(1);
  const [selectedRoom, setSelectedRoom] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [activeImage, setActiveImage] = useState(0);

  // New review form
  const [reviewAuthor, setReviewAuthor] = useState("");
  const [reviewRating, setReviewRating] = useState(5);
  const [reviewText, setReviewText] = useState("");

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const [hotelData, roomsData, reviewsData] = await Promise.all([
          API.getHotel(id),
          API.getHotelRooms(id),
          API.getHotelReviews(id),
        ]);
        setHotel(hotelData);
        setRooms(roomsData.rooms || []);
        setReviews(reviewsData.reviews || []);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  function getEffectivePrice() {
    if (!hotel) return 0;
    if (selectedRoom) {
      const room = rooms.find((r) => r.type === selectedRoom);
      if (room) return room.pricePerNight;
    }
    return hotel.pricePerNight;
  }

  function calcPrice() {
    if (!hotel || !checkin || !checkout) return null;
    const nights = Math.max(1, Math.ceil((new Date(checkout) - new Date(checkin)) / 86400000));
    const ppn = getEffectivePrice();
    const sub = nights * ppn;
    const tax = Math.round(sub * 0.16);
    return { nights, sub, tax, total: sub + tax, ppn };
  }

  async function handleBooking() {
    if (!hotel) return;
    if (!checkin || !checkout || !guestName.trim() || !guestEmail.trim()) {
      showToast("Please fill in all fields");
      return;
    }

    setSubmitting(true);
    try {
      const res = await API.createBooking({
        hotelId: hotel.id,
        checkIn: checkin,
        checkOut: checkout,
        guests: Number(guests),
        guestName: guestName.trim(),
        guestEmail: guestEmail.trim(),
        roomType: selectedRoom || undefined,
      });
      setBooking(res.booking);
    } catch (e) {
      showToast("Booking failed: " + e.message);
    } finally {
      setSubmitting(false);
    }
  }

  async function handleSubmitReview() {
    if (!reviewAuthor.trim() || !reviewText.trim()) {
      showToast("Please fill in all review fields");
      return;
    }
    try {
      const res = await API.addHotelReview(id, {
        author: reviewAuthor.trim(),
        rating: reviewRating,
        text: reviewText.trim(),
      });
      setReviews((prev) => [res.review, ...prev]);
      setReviewAuthor("");
      setReviewText("");
      setReviewRating(5);
      showToast("Review submitted!");
    } catch (e) {
      showToast("Failed to submit review: " + e.message);
    }
  }

  if (loading) {
    return (
      <div className="detail-wrap" style={{ display: "flex", justifyContent: "center", paddingTop: 80 }}>
        <Spinner text="Loading hotel details..." />
      </div>
    );
  }

  if (error || !hotel) {
    return (
      <div className="detail-wrap">
        <button className="back-btn" onClick={() => navigate("/results")}>← Back to results</button>
        <div className="error-state">
          <h3>Failed to load hotel</h3>
          <p>{error || "Hotel not found"}</p>
        </div>
      </div>
    );
  }

  const idx = Math.abs(hotel.id?.charCodeAt(1) || 0) % GRADIENTS.length;
  const price = calcPrice();
  const images = hotel.images?.length ? hotel.images : [];
  const policyMap = {
    free_cancellation: "✅ Free cancellation",
    partial_refund: "⚠️ Partial refund available",
    non_refundable: "🚫 Non-refundable",
  };

  return (
    <div className="detail-wrap">
      <button className="back-btn" onClick={() => navigate("/results")}>← Back to results</button>

      {/* Image gallery */}
      {images.length > 0 ? (
        <div className="detail-hero" style={{ padding: 0, overflow: "hidden" }}>
          <img
            src={images[activeImage]}
            alt={hotel.name}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
          {images.length > 1 && (
            <div style={{
              position: "absolute", bottom: 16, left: "50%", transform: "translateX(-50%)",
              display: "flex", gap: 8,
            }}>
              {images.map((_, i) => (
                <button
                  key={i}
                  onClick={() => setActiveImage(i)}
                  style={{
                    width: 10, height: 10, borderRadius: "50%", border: "none",
                    background: i === activeImage ? "var(--accent)" : "rgba(255,255,255,0.4)",
                    cursor: "pointer", padding: 0,
                  }}
                />
              ))}
            </div>
          )}
        </div>
      ) : (
        <div className="detail-hero" style={{ background: GRADIENTS[idx] }}>
          <span>{hotel.emoji || "🏨"}</span>
        </div>
      )}

      <div className="detail-grid">
        <div className="detail-main">
          <div className="detail-name">{hotel.name}</div>
          <div className="detail-meta">
            <span className="detail-loc">📍 {hotel.location}</span>
            <span className="detail-rating-big">★ {hotel.rating}  ({hotel.reviews.toLocaleString()} reviews)</span>
            <span style={{
              background: "var(--surface2)", border: "1px solid var(--border)",
              borderRadius: 40, padding: "4px 12px", fontSize: 12, color: "var(--muted)",
            }}>
              {hotel.type}
            </span>
          </div>

          <p className="detail-desc">{hotel.description}</p>

          {/* Room types */}
          {rooms.length > 0 && (
            <>
              <div className="detail-section-title">Available Rooms</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 10, marginBottom: 28 }}>
                {rooms.map((r) => (
                  <label
                    key={r.type}
                    className={`amenity-item ${selectedRoom === r.type ? "active" : ""}`}
                    style={{
                      cursor: "pointer", border: selectedRoom === r.type
                        ? "1px solid var(--accent)" : "1px solid var(--border)",
                    }}
                  >
                    <input
                      type="radio"
                      name="roomType"
                      value={r.type}
                      checked={selectedRoom === r.type}
                      onChange={() => setSelectedRoom(r.type)}
                      style={{ accentColor: "var(--accent)" }}
                    />
                    <div style={{ flex: 1 }}>
                      <div style={{ fontWeight: 500, color: "var(--text)" }}>{r.type}</div>
                      <div style={{ fontSize: 12, color: "var(--muted)" }}>
                        Up to {r.maxGuests} guests | {r.available} left
                      </div>
                    </div>
                    <div style={{ fontWeight: 700, color: "var(--accent)" }}>
                      ${r.pricePerNight}
                      <span style={{ fontWeight: 400, fontSize: 11, color: "var(--muted)" }}>/night</span>
                    </div>
                  </label>
                ))}
              </div>
            </>
          )}

          {/* Amenities */}
          <div className="detail-section-title">Amenities &amp; features</div>
          <div className="amenity-grid">
            {(hotel.amenities || []).map((a) => (
              <div className="amenity-item" key={a}>
                <span style={{ fontSize: 18 }}>{amenityIcon(a)}</span> {a}
              </div>
            ))}
          </div>

          {/* Policies */}
          <div className="detail-section-title">Policies</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 8, marginBottom: 28 }}>
            <div style={{ fontSize: 13, color: "var(--muted)" }}>
              🕐 Check-in: {hotel.checkIn || "14:00"} — Check-out: {hotel.checkOut || "12:00"}
            </div>
            <div style={{ fontSize: 13, color: "var(--muted)" }}>
              {hotel.petsAllowed ? "🐾 Pets welcome" : "🚫 No pets"}
            </div>
            <div style={{ fontSize: 13, color: "var(--muted)" }}>🚭 Non-smoking property</div>
            <div style={{ fontSize: 13, color: "var(--muted)" }}>
              💳 {(hotel.payments || []).join(", ")}
            </div>
            <div style={{ fontSize: 13, color: "var(--accent)" }}>
              {policyMap[hotel.cancellationPolicy] || "📋 Standard cancellation policy"}
            </div>
          </div>

          {/* Reviews */}
          <div className="detail-section-title">Guest Reviews</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 14, marginBottom: 28 }}>
            {reviews.length === 0 && (
              <div style={{ fontSize: 13, color: "var(--muted)" }}>No reviews yet. Be the first!</div>
            )}
            {reviews.map((r) => (
              <div key={r.id} style={{
                background: "var(--surface)", border: "1px solid var(--border)",
                borderRadius: "var(--radius-sm)", padding: 14,
              }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                  <span style={{ fontWeight: 500, fontSize: 14 }}>{r.author}</span>
                  <span style={{ color: "var(--accent)", fontSize: 13 }}>★ {r.rating}</span>
                </div>
                <p style={{ fontSize: 13, color: "var(--muted)", marginBottom: 4 }}>{r.text}</p>
                <span style={{ fontSize: 11, color: "var(--muted)" }}>{r.date}</span>
              </div>
            ))}
          </div>

          {/* Add review */}
          <div className="detail-section-title">Write a Review</div>
          <div style={{
            background: "var(--surface)", border: "1px solid var(--border)",
            borderRadius: "var(--radius-sm)", padding: 16, marginBottom: 28,
          }}>
            <input className="guest-input" placeholder="Your name"
              value={reviewAuthor} onChange={(e) => setReviewAuthor(e.target.value)} />
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
              <span style={{ fontSize: 13, color: "var(--muted)" }}>Rating:</span>
              {[1, 2, 3, 4, 5].map((s) => (
                <button
                  key={s}
                  onClick={() => setReviewRating(s)}
                  style={{
                    background: "none", border: "none", cursor: "pointer",
                    fontSize: 20, color: s <= reviewRating ? "var(--accent)" : "var(--border)",
                    transition: "color 0.15s", padding: 0,
                  }}
                >
                  ★
                </button>
              ))}
            </div>
            <textarea className="guest-input" placeholder="Share your experience..."
              value={reviewText} onChange={(e) => setReviewText(e.target.value)}
              style={{ minHeight: 80, resize: "vertical", fontFamily: "var(--font-body)" }} />
            <button className="apply-btn" onClick={handleSubmitReview}
              style={{ marginTop: 0 }}>Submit Review</button>
          </div>
        </div>

        {/* Booking card */}
        <div>
          <div className="booking-card">
            <div className="booking-price">
              ${getEffectivePrice()} <span>/ night</span>
            </div>
            <hr className="booking-divider" />

            <div className="date-row">
              <input className="date-input" type="date" value={checkin}
                onChange={(e) => setCheckin(e.target.value)} placeholder="Check-in" />
              <input className="date-input" type="date" value={checkout}
                onChange={(e) => setCheckout(e.target.value)} placeholder="Check-out" />
            </div>

            <input className="guest-input" placeholder="Full name"
              value={guestName} onChange={(e) => setGuestName(e.target.value)} />
            <input className="guest-input" type="email" placeholder="Email address"
              value={guestEmail} onChange={(e) => setGuestEmail(e.target.value)} />
            <input className="guest-input" type="number" min="1" max="10"
              value={guests} onChange={(e) => setGuests(Number(e.target.value))} placeholder="Guests" />

            <button className="book-btn" onClick={handleBooking} disabled={submitting}>
              {submitting ? "Processing..." : "Reserve Now"}
            </button>
            <div className="book-note">No charge yet — confirm on next step</div>

            <hr className="booking-divider" />
            <div style={{ fontSize: 13, display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
              <span style={{ color: "var(--muted)" }}>Rate</span>
              <span>${getEffectivePrice()} / night</span>
            </div>
            <div style={{ fontSize: 13, display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
              <span style={{ color: "var(--muted)" }}>Taxes (16%)</span>
              <span>{price ? `$${price.tax}` : "—"}</span>
            </div>
            <hr className="booking-divider" />
            <div style={{ display: "flex", justifyContent: "space-between", fontWeight: 500 }}>
              <span>Total</span>
              <span style={{ color: "var(--accent)" }}>
                {price ? `$${price.total} (${price.nights} night${price.nights > 1 ? "s" : ""})` : "—"}
              </span>
            </div>
          </div>
        </div>
      </div>

      <BookingModal booking={booking} onClose={() => setBooking(null)} />
    </div>
  );
}
