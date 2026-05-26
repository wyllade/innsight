import { useState, useEffect, useCallback } from "react";
import { useSearchParams } from "react-router-dom";
import { Calendar } from "lucide-react";
import { API } from "../api.js";
import HotelCard from "../components/HotelCard.jsx";
import Spinner from "../components/Spinner.jsx";
import PageHelmet from "../components/PageHelmet.jsx";
import { amenityIcon } from "../components/HotelCard.jsx";

const SITE_URL = import.meta.env.VITE_SITE_URL || "https://innsight.app";

export default function Results() {
  const [searchParams, setSearchParams] = useSearchParams();

  const [hotels, setHotels] = useState([]);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [allAmenities, setAllAmenities] = useState([]);
  const [maxPriceLimit, setMaxPriceLimit] = useState(1000);

  const city = searchParams.get("city") || "";
  const q = searchParams.get("q") || "";
  const sort = searchParams.get("sort") || "";
  const maxPrice = searchParams.get("maxPrice") || "";
  const stars = searchParams.get("stars") || "";
  const typeParam = searchParams.get("type") || "";
  const checkin = searchParams.get("checkin") || "";
  const checkout = searchParams.get("checkout") || "";
  const selectedAmenities = searchParams.get("amenities")?.split(",").filter(Boolean) || [];
  const page = parseInt(searchParams.get("page")) || 1;

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
      if (checkin) params.checkIn = checkin;
      if (checkout) params.checkOut = checkout;
      params.page = page;
      params.limit = 20;

      const data = await API.getHotels(params);
      setHotels(data.results);
      setTotal(data.total);
      setTotalPages(data.totalPages || 1);

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
  }, [city, q, sort, maxPrice, stars, typeParam, selectedAmenities.join(","), checkin, checkout, page, maxPriceLimit]);

  useEffect(() => {
    fetchHotels();
  }, [fetchHotels]);

  function updateParam(key, value) {
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev);
      if (value) next.set(key, value);
      else next.delete(key);
      if (key !== "page") next.delete("page");
      return next;
    });
  }

  function goToPage(p) {
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev);
      next.set("page", String(p));
      return next;
    });
  }

  function toggleAmenity(amenity) {
    const current = new Set(selectedAmenities);
    if (current.has(amenity)) current.delete(amenity);
    else current.add(amenity);
    updateParam("amenities", [...current].join(","));
  }

  const pageTitle = city ? `${city} Hotels` : "Browse Hotels";
  const pageDesc = city
    ? `Discover the best hotels in ${city}. Filter by price, amenities, star rating, and more.`
    : "Browse our full collection of hotels. Filter by price, amenities, location, and star rating to find your perfect stay.";
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "itemListElement": hotels.slice(0, 10).map((h, i) => ({
      "@type": "ListItem",
      "position": i + 1,
      "item": {
        "@type": "Hotel",
        "name": h.name,
        "url": `${SITE_URL}/hotel/${h.id}`,
        "image": h.images?.[0] || "",
        "address": { "@type": "PostalAddress", "addressLocality": h.city },
      },
    })),
  };

  return (
    <>
      <PageHelmet title={pageTitle} description={pageDesc} jsonLd={jsonLd} />
      <div className="results-layout">
        <aside className="sidebar" role="complementary" aria-label="Filters">
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
              aria-label="Maximum price per night"
            />
            <div className="price-labels">
              <span>$0</span>
              <span>{maxPrice && Number(maxPrice) < maxPriceLimit ? `Up to $${maxPrice}` : "Any price"}</span>
            </div>
          </div>

          <div className="filter-section">
            <h3>Star rating</h3>
            <div className="star-filter" role="group" aria-label="Star rating">
              {["3", "4", "5"].map((s) => (
                <button
                  key={s}
                  className={`star-btn ${stars === s ? "active" : ""}`}
                  onClick={() => updateParam("stars", stars === s ? "" : s)}
                  aria-pressed={stars === s}
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
                  onChange={() => {
                    const current = new Set(typeParam ? typeParam.split(",") : []);
                    if (current.has(t)) current.delete(t);
                    else current.add(t);
                    updateParam("type", [...current].join(","));
                  }}
                />
                {" "}{t}
              </label>
            ))}
          </div>

          <div className="filter-section">
            <h3 id="amenities-heading">Amenities</h3>
            {allAmenities.map((a) => (
              <label className="filter-check" key={a}>
                <input
                  type="checkbox"
                  checked={selectedAmenities.includes(a)}
                  onChange={() => toggleAmenity(a)}
                />
                {" "}{amenityIcon(a, 14)} {a}
              </label>
            ))}
          </div>
        </aside>

        <main className="results-main" id="main-content" role="main">
          <div className="results-header">
            <div>
              <h2>{pageTitle}</h2>
              <div className="results-count" aria-live="polite">
                {loading ? "Searching..." : `Showing ${total} propert${total === 1 ? "y" : "ies"}`}
              </div>
            </div>
            <select
              className="sort-select"
              value={sort}
              onChange={(e) => updateParam("sort", e.target.value)}
              aria-label="Sort results"
            >
              <option value="">Best match</option>
              <option value="price_asc">Price: Low to High</option>
              <option value="price_desc">Price: High to Low</option>
              <option value="rating">Top Rated</option>
              <option value="reviews">Most Reviewed</option>
            </select>
          </div>

          {checkin && checkout && (
            <div style={{
              fontSize: 12, color: "var(--accent)", marginBottom: 16,
              padding: "6px 12px", background: "rgba(201,169,110,0.08)",
              borderRadius: "var(--radius-sm)", display: "inline-flex", alignItems: "center", gap: 4,
            }}>
              <Calendar size={12} /> {checkin} → {checkout}
            </div>
          )}

          <div className="hotel-grid" role="list" aria-label="Hotel results">
            {loading ? (
              <div style={{ gridColumn: "1 / -1" }}>
                <Spinner text="Loading hotels..." />
              </div>
            ) : error ? (
              <div className="error-state" style={{ gridColumn: "1 / -1" }} role="alert">
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

          {totalPages > 1 && !loading && (
            <nav aria-label="Pagination" style={{
              display: "flex", justifyContent: "center", gap: 8, marginTop: 32,
            }}>
              <button
                className="back-btn"
                disabled={page <= 1}
                onClick={() => goToPage(page - 1)}
                style={{ opacity: page <= 1 ? 0.4 : 1 }}
                aria-label="Previous page"
              >
                ← Previous
              </button>
              {Array.from({ length: Math.min(totalPages, 10) }, (_, i) => {
                const p = i + 1;
                return (
                  <button
                    key={p}
                    className="star-btn"
                    style={p === page ? {
                      background: "rgba(201,169,110,0.12)",
                      borderColor: "var(--accent)", color: "var(--accent)",
                    } : {}}
                    onClick={() => goToPage(p)}
                    aria-label={`Page ${p}`}
                    aria-current={p === page ? "page" : undefined}
                  >
                    {p}
                  </button>
                );
              })}
              <button
                className="back-btn"
                disabled={page >= totalPages}
                onClick={() => goToPage(page + 1)}
                style={{ opacity: page >= totalPages ? 0.4 : 1 }}
                aria-label="Next page"
              >
                Next →
              </button>
            </nav>
          )}
        </main>
      </div>
    </>
  );
}
