import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { API } from "../api.js";
import Spinner from "../components/Spinner.jsx";
import { useToast } from "../components/Toast.jsx";

export default function MyBookings() {
  const navigate = useNavigate();
  const showToast = useToast();

  const [email, setEmail] = useState("");
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  async function handleLookup() {
    if (!email.trim()) {
      showToast("Please enter your email");
      return;
    }
    setLoading(true);
    setSearched(true);
    try {
      const data = await API.getBookings({ email: email.trim() });
      setBookings(data.bookings || []);
    } catch (e) {
      showToast("Failed to load bookings");
      setBookings([]);
    } finally {
      setLoading(false);
    }
  }

  async function handleCancel(bookingId) {
    if (!confirm("Are you sure you want to cancel this booking?")) return;
    try {
      await API.cancelBooking(bookingId);
      setBookings((prev) =>
        prev.map((b) => (b.id === bookingId ? { ...b, status: "cancelled" } : b))
      );
      showToast("Booking cancelled");
    } catch (e) {
      showToast("Failed to cancel booking");
    }
  }

  function getStatusStyle(status) {
    switch (status) {
      case "confirmed":
        return { color: "var(--accent3)" };
      case "cancelled":
        return { color: "#e74c3c" };
      default:
        return { color: "var(--muted)" };
    }
  }

  return (
    <div className="detail-wrap" style={{ maxWidth: 700 }}>
      <button className="back-btn" onClick={() => navigate("/")}>← Back to home</button>

      <h1 style={{
        fontFamily: "var(--font-display)", fontSize: 32, fontWeight: 700,
        marginBottom: 24,
      }}>
        My Bookings
      </h1>

      <div style={{
        background: "var(--surface)", border: "1px solid var(--border)",
        borderRadius: "var(--radius)", padding: 20, marginBottom: 28,
      }}>
        <div style={{ fontSize: 13, color: "var(--muted)", marginBottom: 10 }}>
          Enter the email address you used to book:
        </div>
        <div style={{ display: "flex", gap: 10 }}>
          <input
            className="search-field"
            type="email"
            placeholder="your@email.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleLookup()}
          />
          <button className="search-btn" onClick={handleLookup} disabled={loading}>
            {loading ? "Searching..." : "Find Bookings"}
          </button>
        </div>
      </div>

      {loading && <Spinner text="Looking up bookings..." />}

      {!loading && searched && bookings.length === 0 && (
        <div className="error-state">
          <h3>No bookings found</h3>
          <p>No bookings were found for this email address.</p>
        </div>
      )}

      {!loading && bookings.length > 0 && (
        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
          {bookings.map((b) => (
            <div key={b.id} style={{
              background: "var(--surface)", border: "1px solid var(--border)",
              borderRadius: "var(--radius)", padding: 18,
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start", marginBottom: 12 }}>
                <div>
                  <div style={{ fontWeight: 600, fontSize: 16 }}>{b.hotelName}</div>
                  <div style={{ fontSize: 12, color: "var(--muted)" }}>{b.hotelLocation}</div>
                </div>
                <div style={{ textAlign: "right" }}>
                  <div style={{
                    fontSize: 12, fontWeight: 500, textTransform: "uppercase",
                    ...getStatusStyle(b.status),
                  }}>
                    {b.status}
                  </div>
                  <div style={{ fontSize: 11, color: "var(--muted)", marginTop: 2 }}>
                    {b.id?.split("-")[0].toUpperCase()}
                  </div>
                </div>
              </div>

              <div style={{
                display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 10,
                fontSize: 13, color: "var(--muted)", marginBottom: 12,
              }}>
                <div>
                  <span style={{ display: "block", fontSize: 11, color: "var(--text)", fontWeight: 500 }}>Check-in</span>
                  {b.checkIn}
                </div>
                <div>
                  <span style={{ display: "block", fontSize: 11, color: "var(--text)", fontWeight: 500 }}>Check-out</span>
                  {b.checkOut}
                </div>
                <div>
                  <span style={{ display: "block", fontSize: 11, color: "var(--text)", fontWeight: 500 }}>Guests</span>
                  {b.guests}
                </div>
                <div>
                  <span style={{ display: "block", fontSize: 11, color: "var(--text)", fontWeight: 500 }}>Room</span>
                  {b.roomType || "Standard"}
                </div>
                <div>
                  <span style={{ display: "block", fontSize: 11, color: "var(--text)", fontWeight: 500 }}>Nights</span>
                  {b.nights}
                </div>
                <div>
                  <span style={{ display: "block", fontSize: 11, color: "var(--text)", fontWeight: 500 }}>Total</span>
                  <span style={{ color: "var(--accent)", fontWeight: 700 }}>${b.total}</span>
                </div>
              </div>

              {b.status === "confirmed" && (
                <button
                  className="back-btn"
                  onClick={() => handleCancel(b.id)}
                  style={{ color: "#e74c3c", borderColor: "rgba(231,76,60,0.3)" }}
                >
                  Cancel Booking
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
