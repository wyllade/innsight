import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { API } from "../services/api.js";
import Spinner from "../components/common/Spinner.jsx";
import PageHelmet from "../components/common/PageHelmet.jsx";
import { useToast } from "../components/common/Toast.jsx";

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
      setBookings(Array.isArray(data) ? data : []);
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
        prev.map((b) =>
          b.id === bookingId ? { ...b, status: "cancelled" } : b
        )
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
        description="View and manage your hotel bookings."
      />

      <div className="bookings-page">
        <button className="back-btn" onClick={() => navigate("/")}>
          ← Back to home
        </button>

        <h1 className="bookings-title">My Bookings</h1>

        <div className="bookings-search">
          <input
            type="email"
            placeholder="your@email.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleLookup()}
          />

          <button onClick={handleLookup} disabled={loading}>
            {loading ? "Searching..." : "Find Bookings"}
          </button>
        </div>

        {loading && <Spinner text="Looking up bookings..." />}

        {!loading && searched && bookings.length === 0 && (
          <p>No bookings found</p>
        )}

        {!loading && bookings.length > 0 && (
          <div className="booking-list">
            {bookings.map((b) => (
              <div key={b.id} className="booking-card-item">
                <div className="booking-card-header">
                  <div>
                    <div className="booking-card-name">{b.hotelName}</div>
                    <div className="booking-card-location">
                      {b.hotel_name}
                    </div>
                  </div>

                  <div>
                    <div className={`booking-card-status ${b.status}`}>
                      {b.status}
                    </div>
                    <div className="booking-card-id">{b.id}</div>
                  </div>
                </div>

                <div className="booking-card-details">
                  <div>
                    <strong>Check-in:</strong> {b.checkin_date}
                  </div>
                  <div>
                    <strong>Check-out:</strong> {b.checkout_date}
                  </div>
                  <div>
                    <strong>Total:</strong> ${b.total_price}
                  </div>
                </div>

                {b.status === "confirmed" && (
                  <button onClick={() => handleCancel(b.id)}>
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