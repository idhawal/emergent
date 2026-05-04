import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Home from "@/components/Home";
import RegressionPage from "@/components/regression/RegressionPage";
import KNNPage from "@/components/knn/KNNPage";
import TreePage from "@/components/decision-tree/TreePage";
import GAPage from "@/components/genetic/GAPage";

function App() {
  return (
    <div className="App">
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
    </div>
  );
}

export default App;
