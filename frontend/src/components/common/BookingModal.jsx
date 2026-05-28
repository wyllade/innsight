// React import not required with new JSX transform

export default function BookingModal({ booking, onClose }) {
  if (!booking) return null;

  const bookingId =
    typeof booking.id === "string"
      ? booking.id.split("-")[0]
      : String(booking.id || "N/A");

  return (
    <div className={`confirm-overlay ${booking ? "show" : ""}`}>
      <div className="confirm-box">

        <div className="confirm-icon">🎉</div>

        <h2>Booking Confirmed</h2>

        <p>Your reservation has been successfully placed.</p>

        <div className="confirm-detail">

          <div>
            <span>Booking ID</span>
            <span>{bookingId}</span>
          </div>

          <div>
            <span>Email</span>
            <span>{booking.email || "N/A"}</span>
          </div>

          <div>
            <span>Check-in</span>
            <span>{booking.checkinDate || booking.checkin || "N/A"}</span>
          </div>

          <div>
            <span>Check-out</span>
            <span>{booking.checkoutDate || booking.checkout || "N/A"}</span>
          </div>

        </div>

        <button className="confirm-close" onClick={onClose}>
          Close
        </button>

      </div>
    </div>
  );
}