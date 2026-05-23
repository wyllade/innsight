import { Routes, Route } from "react-router-dom";
import { ToastProvider } from "./components/Toast.jsx";
import Navbar from "./components/Navbar.jsx";
import Landing from "./pages/Landing.jsx";
import Results from "./pages/Results.jsx";
import Detail from "./pages/Detail.jsx";

export default function App() {
  return (
    <ToastProvider>
      <Navbar />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/results" element={<Results />} />
        <Route path="/hotel/:id" element={<Detail />} />
      </Routes>
    </ToastProvider>
  );
}
