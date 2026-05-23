import { useState, useEffect, useCallback } from "react";
import { useSearchParams } from "react-router-dom";
import { API } from "../api.js";
import HotelCard from "../components/HotelCard.jsx";
import Spinner from "../components/Spinner.jsx";
import { amenityIcon } from "../components/HotelCard.jsx";

export default function Results() {
  const [searchParams, setSearchParams] = useSearchParams();

  const [hotels, setHotels] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [allAmenities, setAllAmenities] = useState([]);
  const [maxPriceLimit, setMaxPriceLimit] = useState(1000);

  // Derive filter state from URL params
  const city = searchParams.get("city") || "";
  const q = searchParams.get("q") || "";
  const sort = searchParams.get("sort") || "";
  const maxPrice = searchParams.get("maxPrice") || "";
  const stars = searchParams.get("stars") || "";
  const typeParam = searchParams.get("type") || "";
  const selectedAmenities = searchParams.get("amenities")?.split(",").filter(Boolean) || [];

  useEffect(() => {
    async function loadAmenities() {
      try {
        const amenities = await API.getAmenities();
        setAllAmenities(amenities);
      } catch {
        setAllAmenities(["Swimming Pool", "Free WiFi", "Gym", "Breakfast", "Spa", "Parking", "Restaurant", "Bar"]);
      }
    }
    loadAmenities();
  }, []);

  const fetchHotels = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = {};
      if (city) params.city = city;
      if (q) params.q = q;
      if (sort) params.sort = sort;
      if (maxPrice && Number(maxPrice) < maxPriceLimit) params.maxPrice = maxPrice;
      if (stars) params.stars = stars;
      if (typeParam) params.type = typeParam;
      if (selectedAmenities.length) params.amenities = selectedAmenities.join(",");

      const data = await API.getHotels(params);
      setHotels(data.results);
      setTotal(data.total);

      // Dynamic max price from data (FIX #5)
      if (data.results.length > 0) {
        const highest = Math.max(...data.results.map((h) => h.pricePerNight));
        setMaxPriceLimit((prev) => Math.max(prev, highest));
      }
    } catch (e) {
      setError(e.message);
      setHotels([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  }, [city, q, sort, maxPrice, stars, typeParam, selectedAmenities.join(","), maxPriceLimit]);

  useEffect(() => {
    fetchHotels();
  }, [fetchHotels]);

  function updateParam(key, value) {
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev);
      if (value) next.set(key, value);
      else next.delete(key);
      return next;
    });
  }

  function toggleAmenity(amenity) {
    const current = new Set(selectedAmenities);
    if (current.has(amenity)) current.delete(amenity);
    else current.add(amenity);
    updateParam("amenities", [...current].join(","));
  }

  function toggleType(type) {
    const current = new Set(typeParam ? typeParam.split(",") : []);
    if (current.has(type)) current.delete(type);
    else current.add(type);
    updateParam("type", [...current].join(","));
  }

  function handleApplyFilters() {
    // All state already in URL params via individual handlers,
    // but we re-fetch explicitly
    fetchHotels();
  }

  return (
    <div className="results-layout">
      <aside className="sidebar">
        <div className="filter-section">
          <h3>Price per night</h3>
          <input
            type="range"
            className="price-range"
            min="0"
            max={maxPriceLimit}
            value={maxPrice || maxPriceLimit}
            step="10"
            onChange={(e) => {
              const val = e.target.value;
              updateParam("maxPrice", Number(val) >= maxPriceLimit ? "" : val);
            }}
          />
          <div className="price-labels">
            <span>$0</span>
            <span>{maxPrice && Number(maxPrice) < maxPriceLimit ? `Up to $${maxPrice}` : "Any price"}</span>
          </div>
        </div>

        <div className="filter-section">
          <h3>Star rating</h3>
          <div className="star-filter">
            {["3", "4", "5"].map((s) => (
              <button
                key={s}
                className={`star-btn ${stars === s ? "active" : ""}`}
                onClick={() => updateParam("stars", stars === s ? "" : s)}
              >
                {s}+ ★
              </button>
            ))}
          </div>
        </div>

        <div className="filter-section">
          <h3>Property type</h3>
          {["Hotel", "Resort", "Boutique", "Hostel"].map((t) => (
            <label className="filter-check" key={t}>
              <input
                type="checkbox"
                checked={typeParam.includes(t)}
                onChange={() => toggleType(t)}
              />
              {" "}{t}
            </label>
          ))}
        </div>

        <div className="filter-section">
          <h3>Amenities</h3>
          {allAmenities.map((a) => (
            <label className="filter-check" key={a}>
              <input
                type="checkbox"
                checked={selectedAmenities.includes(a)}
                onChange={() => toggleAmenity(a)}
              />
              {" "}{amenityIcon(a)} {a}
            </label>
          ))}
        </div>

        <button className="apply-btn" onClick={handleApplyFilters}>
          Apply Filters
        </button>
      </aside>

      <main className="results-main">
        <div className="results-header">
          <div>
            <h2 id="results-title">{city ? `${city} Hotels` : "All Hotels"}</h2>
            <div className="results-count">
              {loading ? "Searching..." : `Showing ${total} propert${total === 1 ? "y" : "ies"}`}
            </div>
          </div>
          <select
            className="sort-select"
            value={sort}
            onChange={(e) => updateParam("sort", e.target.value)}
          >
            <option value="">Best match</option>
            <option value="price_asc">Price: Low to High</option>
            <option value="price_desc">Price: High to Low</option>
            <option value="rating">Top Rated</option>
            <option value="reviews">Most Reviewed</option>
          </select>
        </div>

        <div className="hotel-grid" id="hotel-grid">
          {loading ? (
            <div style={{ gridColumn: "1 / -1" }}>
              <Spinner text="Loading hotels..." />
            </div>
          ) : error ? (
            <div className="error-state" style={{ gridColumn: "1 / -1" }}>
              <h3>Could not load hotels</h3>
              <p>Make sure the backend server is running at <code>http://localhost:3001</code></p>
              <p style={{ marginTop: 8, fontSize: 12 }}>{error}</p>
            </div>
          ) : hotels.length === 0 ? (
            <div className="error-state" style={{ gridColumn: "1 / -1" }}>
              <h3>No hotels found</h3>
              <p>Try adjusting your filters or search terms.</p>
            </div>
          ) : (
            hotels.map((h, i) => <HotelCard key={h.id} hotel={h} index={i} />)
          )}
        </div>
      </main>
    </div>
  );
}
