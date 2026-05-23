import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { API } from "../api.js";
import Spinner from "../components/Spinner.jsx";
import PageHelmet from "../components/PageHelmet.jsx";
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

  return (
    <>
      <PageHelmet
        title="My Bookings"
        description="View and manage your hotel bookings. Look up reservations by email address."
      />
      <div className="bookings-page">
        <button className="back-btn" onClick={() => navigate("/")} aria-label="Back to home">
          ← Back to home
        </button>

        <h1 className="bookings-title">
          My Bookings
        </h1>

        <div className="bookings-search">
          <label htmlFor="booking-email" className="bookings-search-label">
            Enter the email address you used to book:
          </label>
          <div className="bookings-search-row">
            <input
              id="booking-email"
              className="search-field"
              type="email"
              placeholder="your@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleLookup()}
              aria-label="Email address for booking lookup"
            />
            <button className="search-btn" onClick={handleLookup} disabled={loading}
              aria-label="Find bookings">
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
          <div className="booking-list" role="list" aria-label="Your bookings">
            {bookings.map((b) => (
              <div key={b.id} className="booking-card-item" role="listitem">
                <div className="booking-card-header">
                  <div>
                    <div className="booking-card-name">{b.hotelName}</div>
                    <div className="booking-card-location">{b.hotelLocation}</div>
                  </div>
                  <div style={{ textAlign: "right" }}>
                    <div className={`booking-card-status ${b.status}`}>
                      {b.status}
                    </div>
                    <div className="booking-card-id">
                      {b.id?.split("-")[0].toUpperCase()}
                    </div>
                  </div>
                </div>

                <div className="booking-card-details">
                  <div>
                    <span className="booking-detail-label">Check-in</span>
                    {b.checkIn}
                  </div>
                  <div>
                    <span className="booking-detail-label">Check-out</span>
                    {b.checkOut}
                  </div>
                  <div>
                    <span className="booking-detail-label">Guests</span>
                    {b.guests}
                  </div>
                  <div>
                    <span className="booking-detail-label">Room</span>
                    {b.roomType || "Standard"}
                  </div>
                  <div>
                    <span className="booking-detail-label">Nights</span>
                    {b.nights}
                  </div>
                  <div>
                    <span className="booking-detail-label">Total</span>
                    <span className="booking-detail-total">${b.total}</span>
                  </div>
                </div>

                {b.status === "confirmed" && (
                  <button
                    className="booking-cancel-btn"
                    onClick={() => handleCancel(b.id)}
                    aria-label={`Cancel booking at ${b.hotelName}`}
                  >
                    Cancel Booking
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
}
