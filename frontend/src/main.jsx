import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App.jsx";
import "./App.css";

// Hide skeleton once React hydrates
const rootEl = document.getElementById("root");
if (rootEl) {
  const sk = rootEl.querySelector(".sk-init");
  if (sk) sk.style.display = "none";
}

createRoot(rootEl).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>
);
