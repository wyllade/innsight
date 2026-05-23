import { Component } from "react";

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
        <div
          style={{
            display: "flex", flexDirection: "column",
            alignItems: "center", justifyContent: "center",
            minHeight: "100vh", padding: 40, textAlign: "center",
          }}
        >
          <div style={{ fontSize: 64, marginBottom: 16 }}>⚡</div>
          <h1 style={{ fontFamily: "var(--font-display)", fontSize: 28, marginBottom: 8 }}>
            Something went wrong
          </h1>
          <p style={{ color: "var(--muted)", fontSize: 14, marginBottom: 24 }}>
            An unexpected error occurred. Please try refreshing the page.
          </p>
          <button
            onClick={() => window.location.reload()}
            className="search-btn"
          >
            Refresh Page
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
