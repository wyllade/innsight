import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Hotel, MapPin } from "lucide-react";
import { GRADIENTS, amenityIcon } from "./hotelUtils";

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
