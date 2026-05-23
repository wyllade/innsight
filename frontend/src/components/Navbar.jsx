import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <>
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>
      <nav role="navigation" aria-label="Main navigation">
        <Link to="/" className="logo" onClick={() => window.scrollTo(0, 0)} aria-label="Innsight home">
          Inn<span>sight</span>
        </Link>
        <div className="nav-links">
          <Link to="/">Discover</Link>
          <Link to="/results">Browse Hotels</Link>
          <Link to="/bookings">My Bookings</Link>
        </div>
        <Link to="/results" className="nav-btn" aria-label="Search hotels">
          Search Hotels
        </Link>
      </nav>
    </>
  );
}
