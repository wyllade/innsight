import { useNavigate } from "react-router-dom";

const GRADIENTS = [
  "linear-gradient(135deg,#1a1635 0%,#2d1f4a 100%)",
  "linear-gradient(135deg,#0f2a1a 0%,#1a3d2b 100%)",
  "linear-gradient(135deg,#1a1a2e 0%,#16213e 100%)",
  "linear-gradient(135deg,#2a1a0f 0%,#3d2b1a 100%)",
  "linear-gradient(135deg,#1a1a1a 0%,#2d2d2d 100%)",
  "linear-gradient(135deg,#1a1228 0%,#2a1a3d 100%)",
  "linear-gradient(135deg,#0d1f2a 0%,#1a3040 100%)",
  "linear-gradient(135deg,#1f1a0d 0%,#302a1a 100%)",
];

const AMENITY_ICONS = {
  "Swimming Pool": "🏊", "Free WiFi": "📶", "Gym": "💪", "Breakfast": "🍳",
  "Spa": "🧖", "Parking": "🅿️", "Restaurant": "🍽️", "Bar": "🍸",
  "Airport Shuttle": "✈️", "Pet Friendly": "🐾", "Room Service": "🛎️", "Conference": "📊",
};

export function amenityIcon(a) {
  return AMENITY_ICONS[a] || "✓";
}

export { GRADIENTS };

export default function HotelCard({ hotel, index = 0 }) {
  const navigate = useNavigate();
  const tags = (hotel.amenities || []).slice(0, 3).map((a) => (
    <span className="hotel-amenity" key={a}>{amenityIcon(a)} {a}</span>
  ));

  return (
    <div className="hotel-card" onClick={() => navigate(`/hotel/${hotel.id}`)}>
      <div className="hotel-img-placeholder" style={{ background: GRADIENTS[index % GRADIENTS.length] }}>
        <span>{hotel.emoji || "🏨"}</span>
        {hotel.badge && <span className="hotel-badge">{hotel.badge}</span>}
      </div>
      <div className="hotel-body">
        <div className="hotel-name">{hotel.name}</div>
        <div className="hotel-location">📍 {hotel.location}</div>
        <div className="hotel-amenities">{tags}</div>
        <div className="hotel-footer">
          <div className="hotel-price">${hotel.pricePerNight} <span>/ night</span></div>
          <div className="hotel-rating">
            ★ {hotel.rating} <span style={{ color: "var(--muted)", fontWeight: 400 }}>
              ({hotel.reviews.toLocaleString()})
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
