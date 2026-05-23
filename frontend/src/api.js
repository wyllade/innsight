const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:3001";

async function apiFetch(path, options = {}) {
  const url = `${BASE_URL}${path}`;
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || data.detail || "API error");
  return data;
}

export const API = {
  getHotels: (params = {}) => {
    const qs = new URLSearchParams(
      Object.fromEntries(Object.entries(params).filter(([, v]) => v !== "" && v != null))
    ).toString();
    return apiFetch(`/api/hotels${qs ? "?" + qs : ""}`);
  },
  getFeatured: () => apiFetch("/api/hotels/featured"),
  getHotel: (id) => apiFetch(`/api/hotels/${id}`),
  getHotelRooms: (id) => apiFetch(`/api/hotels/${id}/rooms`),
  getHotelReviews: (id) => apiFetch(`/api/hotels/${id}/reviews`),
  addHotelReview: (id, payload) =>
    apiFetch(`/api/hotels/${id}/reviews`, { method: "POST", body: JSON.stringify(payload) }),
  checkAvailability: (id, params) => {
    const qs = new URLSearchParams(params).toString();
    return apiFetch(`/api/hotels/${id}/availability?${qs}`);
  },
  getAmenities: () => apiFetch("/api/hotels/amenities/all"),
  getCities: () => apiFetch("/api/hotels/cities/all"),
  createBooking: (payload) =>
    apiFetch("/api/bookings", { method: "POST", body: JSON.stringify(payload) }),
  getBooking: (id) => apiFetch(`/api/bookings/${id}`),
  getBookings: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return apiFetch(`/api/bookings${qs ? "?" + qs : ""}`);
  },
  updateBooking: (id, payload) =>
    apiFetch(`/api/bookings/${id}`, { method: "PATCH", body: JSON.stringify(payload) }),
  cancelBooking: (id) => apiFetch(`/api/bookings/${id}`, { method: "DELETE" }),
};
