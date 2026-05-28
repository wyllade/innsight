const API_BASE_URL = import.meta.env.DEV
  ? "/api"
  : ((import.meta.env.VITE_API_URL || "") + "/api");

const normalizeHotel = (h) => {
  if (!h) return h;
  return {
    ...h,
    id: String(h.id),
    pricePerNight: h.pricePerNight ?? h.price_per_night ?? h.price ?? 0,
    location: h.location ?? h.city ?? "Unknown",
    reviews: typeof h.reviews === 'number' ? h.reviews : (h.reviews_count ?? 0)
  };
};

export const API = {
  getHotels: async (params = {}) => {
    const qs = new URLSearchParams(
      Object.fromEntries(Object.entries(params).filter(([, v]) => v !== "" && v != null))
    ).toString();
    const response = await fetch(`${API_BASE_URL}/hotels${qs ? "?" + qs : ""}`);
    if (!response.ok) throw new Error("Failed to fetch hotels");
    const data = await response.json();
    
    const rawList = data.hotels || data.results || data.data || [];
    return {
      results: rawList.map(normalizeHotel),
      total: data.total || rawList.length,
      totalPages: data.totalPages || 1
    };
  },

  getHotelDetails: async (hotelId) => {
    const response = await fetch(`${API_BASE_URL}/hotels/${hotelId}`);
    if (!response.ok) throw new Error("Failed to fetch hotel details");
    const data = await response.json();
    return normalizeHotel(data);
  },

  getHotel: async (hotelId) => {
    const response = await fetch(`${API_BASE_URL}/hotels/${hotelId}`);
    if (!response.ok) throw new Error("Failed to fetch hotel details");
    const data = await response.json();
    return normalizeHotel(data);
  },

  getHotelRooms: async (hotelId) => {
    const response = await fetch(`${API_BASE_URL}/hotels/${hotelId}/rooms`);
    if (!response.ok) throw new Error("Failed to fetch rooms");
    const data = await response.json();
    return {
      rooms: data.rooms || data
    };
  },

  getHotelReviews: async (hotelId) => {
    const response = await fetch(`${API_BASE_URL}/hotels/${hotelId}/reviews`);
    if (!response.ok) throw new Error("Failed to fetch reviews");
    const data = await response.json();
    return {
      reviews: data.reviews || data
    };
  },

  getReviews: async (hotelId) => {
    const response = await fetch(`${API_BASE_URL}/hotels/${hotelId}/reviews`);
    if (!response.ok) throw new Error("Failed to fetch reviews");
    return response.json();
  },

  addHotelReview: async (hotelId, reviewData) => {
    const response = await fetch(`${API_BASE_URL}/hotels/${hotelId}/reviews`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(reviewData)
    });
    if (!response.ok) throw new Error("Failed to submit review");
    return response.json();
  },

  submitReview: async (hotelId, author, text, rating) => {
    const response = await fetch(`${API_BASE_URL}/hotels/${hotelId}/reviews`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ author, text, rating: parseInt(rating) })
    });
    if (!response.ok) throw new Error("Failed to submit review");
    return response.json();
  },

  createBooking: async (bookingData) => {
    const response = await fetch(`${API_BASE_URL}/bookings`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        hotelId: bookingData.hotelId,
        checkIn: bookingData.checkIn,
        checkOut: bookingData.checkOut,
        guests: bookingData.guests || 1,
        guestName: bookingData.guestName,
        guestEmail: bookingData.guestEmail,
        roomType: bookingData.roomType || "",
      })
    });
    if (!response.ok) throw new Error("Failed to create booking");
    const data = await response.json();
    return {
      booking: data.booking || data
    };
  },

  getBookings: async (payload = {}) => {
    const targetEmail = payload.email || "";
    const response = await fetch(`${API_BASE_URL}/bookings?email=${encodeURIComponent(targetEmail)}`);
    if (!response.ok) throw new Error("Failed to fetch history");
    const data = await response.json();
    const list = data.bookings || data;
    return Array.isArray(list) ? list : [];
  },

  getBookingHistory: async (email) => {
    const response = await fetch(`${API_BASE_URL}/bookings?email=${encodeURIComponent(email)}`);
    if (!response.ok) throw new Error("Failed to fetch history");
    const data = await response.json();
    const list = data.bookings || data;
    return Array.isArray(list) ? list : [];
  },

  cancelBooking: async (bookingId) => {
    const response = await fetch(`${API_BASE_URL}/bookings/${bookingId}`, {
      method: "DELETE",
    });
    if (!response.ok) throw new Error("Failed to cancel booking");
    return response.json();
  },

  getAmenities: async () => {
    const response = await fetch(`${API_BASE_URL}/hotels/amenities/all`);
    if (!response.ok) throw new Error("Failed to fetch amenities");
    return response.json();
  },

  getCities: async () => {
    const response = await fetch(`${API_BASE_URL}/hotels/cities/all`);
    if (!response.ok) throw new Error("Failed to fetch cities");
    return response.json();
  }
};
