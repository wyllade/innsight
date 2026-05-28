const API_BASE_URL = import.meta.env.DEV
  ? "/api"
  : ((import.meta.env.VITE_API_URL || "") + "/api");

const normalizeHotel = (h) => {
  if (!h) return h;
  return {
    ...h,
    id: String(h.id),
    pricePerNight: h.price_per_night ?? h.price ?? 0,
    location: h.city ?? h.location ?? "Unknown",
    reviews: h.reviews_count ?? (Array.isArray(h.reviews) ? h.reviews.length : (typeof h.reviews === 'number' ? h.reviews : 0))
  };
};

export const API = {
  getHotels: async (params = {}) => {
    let url = `${API_BASE_URL}/hotels`;
    const queryParts = [];
    if (params.city) queryParts.push(`city=${encodeURIComponent(params.city)}`);
    if (params.amenities) queryParts.push(`amenities=${encodeURIComponent(params.amenities)}`);
    if (queryParts.length > 0) url += `?${queryParts.join("&")}`;
    
    const response = await fetch(url);
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
      rooms: data
    };
  },

  getHotelReviews: async (hotelId) => {
    const response = await fetch(`${API_BASE_URL}/hotels/${hotelId}/reviews`);
    if (!response.ok) throw new Error("Failed to fetch reviews");
    const data = await response.json();
    return {
      reviews: data
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
        hotel_id: parseInt(bookingData.hotelId),
        checkin_date: bookingData.checkIn,
        checkout_date: bookingData.checkOut,
        total_price: 150.0,
        user_email: bookingData.guestEmail,
        customer_name: bookingData.guestName
      })
    });
    if (!response.ok) throw new Error("Failed to create booking");
    const data = await response.json();
    return {
      booking: data
    };
  },

  getBookings: async (payload = {}) => {
    const targetEmail = payload.email || "";
    const response = await fetch(`${API_BASE_URL}/bookings?email=${encodeURIComponent(targetEmail)}`);
    if (!response.ok) throw new Error("Failed to fetch history");
    const data = await response.json();
    return data.map(b => ({
      ...b,
      hotelName: b.hotel_name || "Unknown Hotel"
    }));
  },

  getBookingHistory: async (email) => {
    const response = await fetch(`${API_BASE_URL}/bookings?email=${encodeURIComponent(email)}`);
    if (!response.ok) throw new Error("Failed to fetch history");
    const data = await response.json();
    return data.map(b => ({
      ...b,
      hotelName: b.hotel_name || "Unknown Hotel"
    }));
  },

  cancelBooking: async (bookingId) => {
    return { message: "Cancelled successfully" };
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
