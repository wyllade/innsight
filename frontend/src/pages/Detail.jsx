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
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [booking, setBooking] = useState(null);

  const [checkin, setCheckin] = useState("");
  const [checkout, setCheckout] = useState("");
  const [guestName, setGuestName] = useState("");
  const [guestEmail, setGuestEmail] = useState("");
  const [guests, setGuests] = useState(1);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const data = await API.getHotel(id);
        setHotel(data);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  function calcPrice() {
    if (!hotel || !checkin || !checkout) return null;
    const nights = Math.max(1, Math.ceil((new Date(checkout) - new Date(checkin)) / 86400000));
    const sub = nights * hotel.pricePerNight;
    const tax = Math.round(sub * 0.16);
    return { nights, sub, tax, total: sub + tax };
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
      });
      setBooking(res.booking);
    } catch (e) {
      showToast("Booking failed: " + e.message);
    } finally {
      setSubmitting(false);
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

  return (
    <div className="detail-wrap">
      <button className="back-btn" onClick={() => navigate("/results")}>← Back to results</button>

      <div className="detail-hero" style={{ background: GRADIENTS[idx] }}>
        <span>{hotel.emoji || "🏨"}</span>
      </div>

      <div className="detail-grid">
        <div className="detail-main">
          <div className="detail-name">{hotel.name}</div>
          <div className="detail-meta">
            <span className="detail-loc">📍 {hotel.location}</span>
            <span className="detail-rating-big">★ {hotel.rating}  ({hotel.reviews.toLocaleString()} reviews)</span>
            <span style={{
              background: "var(--surface2)", border: "1px solid var(--border)",
              borderRadius: 40, padding: "4px 12px", fontSize: 12, color: "var(--muted)"
            }}>
              {hotel.type}
            </span>
          </div>

          <p className="detail-desc">{hotel.description}</p>

          <div className="detail-section-title">Amenities &amp; features</div>
          <div className="amenity-grid">
            {(hotel.amenities || []).map((a) => (
              <div className="amenity-item" key={a}>
                <span style={{ fontSize: 18 }}>{amenityIcon(a)}</span> {a}
              </div>
            ))}
          </div>

          <div className="detail-section-title">Policies</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
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
          </div>
        </div>

        <div>
          <div className="booking-card">
            <div className="booking-price">
              ${hotel.pricePerNight} <span>/ night</span>
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
              value={guests} onChange={(e) => setGuests(e.target.value)} placeholder="Guests" />

            <button className="book-btn" onClick={handleBooking} disabled={submitting}>
              {submitting ? "Processing..." : "Reserve Now"}
            </button>
            <div className="book-note">No charge yet — confirm on next step</div>

            <hr className="booking-divider" />
            <div style={{ fontSize: 13, display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
              <span style={{ color: "var(--muted)" }}>Rate</span>
              <span>${hotel.pricePerNight} / night</span>
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
