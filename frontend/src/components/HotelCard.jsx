import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Hotel, MapPin, Waves, Wifi, Dumbbell, Coffee, Sparkles, Car,
  UtensilsCrossed, Wine, Plane, PawPrint, ConciergeBell, Presentation, Check,
} from "lucide-react";

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
  "Swimming Pool": Waves, "Free WiFi": Wifi, "Gym": Dumbbell, "Breakfast": Coffee,
  "Spa": Sparkles, "Parking": Car, "Restaurant": UtensilsCrossed, "Bar": Wine,
  "Airport Shuttle": Plane, "Pet Friendly": PawPrint, "Room Service": ConciergeBell, "Conference": Presentation,
};

export function amenityIcon(a, size = 14) {
  const Icon = AMENITY_ICONS[a];
  return Icon ? <Icon size={size} /> : <Check size={size} />;
}

export { GRADIENTS };

export default function HotelCard({ hotel, index = 0 }) {
  const navigate = useNavigate();
  const [imgError, setImgError] = useState(false);
  const tags = (hotel.amenities || []).slice(0, 3).map((a) => (
    <span className="hotel-amenity" key={a}>{amenityIcon(a, 12)} {a}</span>
  ));

  const hasImage = hotel.images && hotel.images[0] && !imgError;

  return (
    <div className="hotel-card" onClick={() => navigate(`/hotel/${hotel.id}`)}>
      <div
        className="hotel-img-placeholder"
        style={{
          background: hasImage
            ? `url(${hotel.images[0]}) center/cover no-repeat`
            : GRADIENTS[index % GRADIENTS.length],
        }}
      >
        {!hasImage && <Hotel size={52} strokeWidth={1.5} />}
        {hasImage && (
          <img
            src={hotel.images[0]}
            alt=""
            style={{ display: "none" }}
            onError={() => setImgError(true)}
          />
        )}
        {hotel.badge && <span className="hotel-badge">{hotel.badge}</span>}
      </div>
      <div className="hotel-body">
        <div className="hotel-name">{hotel.name}</div>
        <div className="hotel-location">
          <MapPin size={12} style={{ verticalAlign: "middle", marginRight: 2 }} /> {hotel.location}
        </div>
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
