// api.js — Innsight API client
const BASE_URL = window.INNSIGHT_API_URL || "http://localhost:3001";

async function apiFetch(path, options = {}) {
  const url = `${BASE_URL}${path}`;
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "API error");
  return data;
}

const API = {
  // Hotels
  getHotels: (params = {}) => {
    const qs = new URLSearchParams(
      Object.fromEntries(Object.entries(params).filter(([, v]) => v !== "" && v != null))
    ).toString();
    return apiFetch(`/api/hotels${qs ? "?" + qs : ""}`);
  },
  getHotel: (id) => apiFetch(`/api/hotels/${id}`),
  getAmenities: () => apiFetch("/api/hotels/amenities/all"),
  getCities: () => apiFetch("/api/hotels/cities/all"),

  // Bookings
  createBooking: (payload) =>
    apiFetch("/api/bookings", { method: "POST", body: JSON.stringify(payload) }),
  getBooking: (id) => apiFetch(`/api/bookings/${id}`),
  cancelBooking: (id) => apiFetch(`/api/bookings/${id}`, { method: "DELETE" }),
};

window.API = API;
