import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import ErrorBoundary from "@/components/ErrorBoundary";
import Home from "@/components/Home";
import RegressionPage from "@/components/regression/RegressionPage";
import KNNPage from "@/components/knn/KNNPage";
import TreePage from "@/components/decision-tree/TreePage";
import GAPage from "@/components/genetic/GAPage";

/**
 * App - Root application component with routing and error handling
 * 
 * Routes:
 * - / - Home page with algorithm overview
 * - /regression - Regression algorithms (Linear, Polynomial, Ridge, Lasso, Elastic Net)
 * - /knn - K-Nearest Neighbors classifier and regressor
 * - /decision-tree - Decision Trees with Gini/Entropy comparison
 * - /genetic-algorithm - Genetic Algorithm optimization
 */
function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/regression" element={<RegressionPage />} />
          <Route path="/knn" element={<KNNPage />} />
          <Route path="/decision-tree" element={<TreePage />} />
          <Route path="/genetic-algorithm" element={<GAPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </ErrorBoundary>
  );
}

export default App;
