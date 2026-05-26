import { Component } from "react";
import { Zap } from "lucide-react";

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, info) {
    console.error("ErrorBoundary caught:", error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <Zap size={64} strokeWidth={1.5} style={{ marginBottom: 16 }} />
          <h1>Something went wrong</h1>
          <p>An unexpected error occurred. Please try refreshing the page.</p>
          <button onClick={() => window.location.reload()} className="search-btn">
            Refresh Page
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
