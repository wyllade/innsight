import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav>
      <Link to="/" className="logo" onClick={() => window.scrollTo(0, 0)}>
        Inn<span>sight</span>
      </Link>
      <div className="nav-links">
        <Link to="/">Discover</Link>
        <Link to="/results">Browse Hotels</Link>
      </div>
      <Link to="/results" className="nav-btn">Search Hotels</Link>
    </nav>
  );
}
