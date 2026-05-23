import { useNavigate } from "react-router-dom";
import PageHelmet from "../components/PageHelmet.jsx";

export default function NotFound() {
  const navigate = useNavigate();

  return (
    <div className="not-found">
      <PageHelmet title="Page Not Found" description="The page you're looking for doesn't exist." />
      <div className="not-found-icon">🔍</div>
      <h1>404 — Page Not Found</h1>
      <p>Looks like this page checked out early. The room might have been deleted or the link was wrong.</p>
      <div className="not-found-actions">
        <button className="back-btn" onClick={() => navigate("/")}>
          ← Go Home
        </button>
        <button className="search-btn" onClick={() => navigate("/results")}>
          Browse Hotels
        </button>
      </div>
    </div>
  );
}
