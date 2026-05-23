import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { API } from "../api.js";
import Spinner from "../components/Spinner.jsx";
import { amenityIcon } from "../components/HotelCard.jsx";

export default function Landing() {
  const navigate = useNavigate();
  const [allAmenities, setAllAmenities] = useState([]);
  const [selectedAmenities, setSelectedAmenities] = useState(new Set());
  const [stats, setStats] = useState({ hotels: null, amenities: null });
  const [loading, setLoading] = useState(true);
  const [location, setLocation] = useState("");
  const [checkin, setCheckin] = useState("");
  const [checkout, setCheckout] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const [amenitiesRes, hotelsRes] = await Promise.all([
          API.getAmenities(),
          API.getHotels(),
        ]);
        setAllAmenities(amenitiesRes);
        setStats({ hotels: hotelsRes.total + "+", amenities: amenitiesRes.length + "+" });
      } catch {
        const fallback = ["Swimming Pool", "Free WiFi", "Gym", "Breakfast", "Spa", "Parking", "Restaurant", "Bar"];
        setAllAmenities(fallback);
        setStats({ hotels: "12,400+", amenities: "200+" });
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  function togglePill(amenity) {
    setSelectedAmenities((prev) => {
      const next = new Set(prev);
      if (next.has(amenity)) next.delete(amenity);
      else next.add(amenity);
      return next;
    });
  }

  function handleSearch() {
    const params = new URLSearchParams();
    if (location.trim()) params.set("city", location.trim());
    if (selectedAmenities.size) params.set("amenities", [...selectedAmenities].join(","));
    if (checkin) params.set("checkin", checkin);
    if (checkout) params.set("checkout", checkout);
    navigate(`/results${params.toString() ? "?" + params.toString() : ""}`);
  }

  return (
    <div className="hero">
      <div className="hero-bg"></div>
      <div className="hero-badge">✦ Smarter Hotel Discovery</div>
      <h1>Find hotels by the <em>life</em> you want to live</h1>
      <p>Search by amenities, not just addresses. Rooftop pool? Gym at 6am? Breakfast included? We've got you.</p>

      <div className="search-card">
        <div className="search-row">
          <input
            className="search-field"
            placeholder="🏙  City or destination..."
            style={{ flex: 2 }}
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
          <input className="search-field" type="date" value={checkin} onChange={(e) => setCheckin(e.target.value)} />
          <input className="search-field" type="date" value={checkout} onChange={(e) => setCheckout(e.target.value)} />
          <button className="search-btn" onClick={handleSearch}>Search →</button>
        </div>
        <div>
          <div style={{ fontSize: 12, color: "var(--muted)", marginBottom: 8, letterSpacing: "0.05em", textTransform: "uppercase" }}>
            Popular amenities
          </div>
          <div className="amenity-pills">
            {loading ? (
              <Spinner text="Loading amenities..." />
            ) : (
              allAmenities.slice(0, 8).map((a) => (
                <button
                  key={a}
                  className={`pill ${selectedAmenities.has(a) ? "active" : ""}`}
                  onClick={() => togglePill(a)}
                >
                  {amenityIcon(a)} {a}
                </button>
              ))
            )}
          </div>
        </div>
      </div>

      <div className="stats-strip">
        <div className="stat">
          <div className="stat-num">{stats.hotels || "—"}</div>
          <div className="stat-label">Hotels Listed</div>
        </div>
        <div className="stat">
          <div className="stat-num">48</div>
          <div className="stat-label">Countries</div>
        </div>
        <div className="stat">
          <div className="stat-num">{stats.amenities || "—"}</div>
          <div className="stat-label">Amenity Filters</div>
        </div>
        <div className="stat">
          <div className="stat-num">4.9★</div>
          <div className="stat-label">User Rating</div>
        </div>
      </div>
    </div>
  );
}
