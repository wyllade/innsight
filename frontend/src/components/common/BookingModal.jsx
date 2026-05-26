import { Sparkles } from "lucide-react";

export default function BookingModal({ booking, onClose }) {
  if (!booking) return null;

  return (
    <div className="confirm-overlay show" onClick={onClose}>
      <div className="confirm-box" onClick={(e) => e.stopPropagation()}>
        <div className="confirm-icon"><Sparkles size={48} strokeWidth={1.5} /></div>
        <h2>Booking Confirmed!</h2>
        <p>Your reservation is locked in. Details below.</p>
        <div className="confirm-detail">
          <div><span>Hotel</span><span>{booking.hotelName}</span></div>
          <div><span>Booking ID</span><span style={{ fontSize: 11 }}>
            {booking.id?.split("-")[0].toUpperCase()}
          </span></div>
          <div><span>Check-in</span><span>{booking.checkIn}</span></div>
          <div><span>Check-out</span><span>{booking.checkOut}</span></div>
          <div><span>Nights</span><span>{booking.nights}</span></div>
          <div><span>Guests</span><span>{booking.guests}</span></div>
          <div><span>Total</span><span>${booking.total}</span></div>
        </div>
        <p style={{ fontSize: 12, color: "var(--muted)", marginBottom: 16 }}>
          A confirmation has been sent to your email.
        </p>
        <button className="confirm-close" onClick={onClose}>Done</button>
      </div>
    </div>
  );
}
