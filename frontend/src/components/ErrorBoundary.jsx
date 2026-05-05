import React from "react";
import { AlertCircle } from "lucide-react";

/**
 * ErrorBoundary - React error boundary component
 * Catches JavaScript errors anywhere in the child component tree
 * Provides graceful error UI instead of white screen of death
 * 
 * Usage:
 * <ErrorBoundary>
 *   <YourComponent />
 * </ErrorBoundary>
 */
export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Log error to console and external service
    console.error("ErrorBoundary caught error:", error, errorInfo);
    
    // Store error info in state for display
    this.setState({
      error,
      errorInfo,
    });

    // Optionally log to external error tracking service (e.g., Sentry)
    // logErrorToService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex items-center justify-center min-h-screen bg-neutral-950 p-4">
          <div className="max-w-md w-full">
            <div className="rounded-lg border border-red-800 bg-red-950/30 p-6 space-y-4">
              <div className="flex items-center gap-3">
                <AlertCircle className="h-6 w-6 text-red-500 flex-shrink-0" />
                <h1 className="text-lg font-semibold text-red-300">Something went wrong</h1>
              </div>

              <p className="text-sm text-red-200">
                An unexpected error occurred. Please try refreshing the page or go back home.
              </p>

              {process.env.NODE_ENV === "development" && this.state.error && (
                <div className="mt-4 pt-4 border-t border-red-800">
                  <p className="text-xs font-mono text-red-300 mb-2">Error details:</p>
                  <pre className="text-xs text-red-200 bg-neutral-900 p-2 rounded overflow-auto max-h-40">
                    {this.state.error.toString()}
                  </pre>
                  {this.state.errorInfo && (
                    <pre className="text-xs text-red-200 bg-neutral-900 p-2 rounded overflow-auto max-h-40 mt-2">
                      {this.state.errorInfo.componentStack}
                    </pre>
                  )}
                </div>
              )}

              <div className="flex gap-2 pt-2">
                <button
                  onClick={() => window.location.href = "/"}
                  className="flex-1 px-4 py-2 rounded bg-red-600 hover:bg-red-700 text-white font-medium text-sm transition-colors"
                >
                  Go Home
                </button>
                <button
                  onClick={() => window.location.reload()}
                  className="flex-1 px-4 py-2 rounded border border-red-600 hover:bg-red-950 text-red-300 font-medium text-sm transition-colors"
                >
                  Refresh
                </button>
              </div>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
