require("dotenv").config();
const express = require("express");
const cors = require("cors");
const { errorHandler, requestLogger, notFound } = require("./src/middleware/errorHandler");
const hotelsRouter = require("./src/routes/hotels");
const bookingsRouter = require("./src/routes/bookings");

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors({ origin: "*" }));
app.use(express.json());
app.use(requestLogger);


app.get("/", (req, res) => {
  res.json({
    name: "Innsight API",
    version: "1.0.0",
    endpoints: {
      hotels: {
        list: "GET /api/hotels?city=&amenities=&minPrice=&maxPrice=&stars=&type=&sort=&q=",
        single: "GET /api/hotels/:id",
        allAmenities: "GET /api/hotels/amenities/all",
        allCities: "GET /api/hotels/cities/all",
      },
      bookings: {
        create: "POST /api/bookings",
        list: "GET /api/bookings",
        single: "GET /api/bookings/:id",
        modify: "PATCH /api/bookings/:id",
        cancel: "DELETE /api/bookings/:id",
      },
    },
  });
});

app.use("/api/hotels", hotelsRouter);
app.use("/api/bookings", bookingsRouter);

app.use(notFound);
app.use(errorHandler);


app.listen(PORT, () => {
  console.log(`\n🏨  Innsight API running at http://localhost:${PORT}`);
  console.log(`📖  Docs: http://localhost:${PORT}/\n`);
});

module.exports = app;
