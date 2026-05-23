import { Routes, Route } from "react-router-dom";
import { HelmetProvider } from "react-helmet-async";
import { ToastProvider } from "./components/Toast.jsx";
import ErrorBoundary from "./components/ErrorBoundary.jsx";
import Navbar from "./components/Navbar.jsx";
import Landing from "./pages/Landing.jsx";
import Results from "./pages/Results.jsx";
import Detail from "./pages/Detail.jsx";
import MyBookings from "./pages/MyBookings.jsx";
import NotFound from "./pages/NotFound.jsx";

export default function App() {
  return (
    <HelmetProvider>
      <ErrorBoundary>
        <ToastProvider>
          <Navbar />
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/results" element={<Results />} />
            <Route path="/hotel/:id" element={<Detail />} />
            <Route path="/bookings" element={<MyBookings />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </ToastProvider>
      </ErrorBoundary>
    </HelmetProvider>
  );
}
