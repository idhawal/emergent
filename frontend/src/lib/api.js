// API layer for ML Visualizer backend.
// Makes HTTP requests to FastAPI backend per spec.md §5 contracts.

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

// ---------- /api/regression ----------
export async function runRegression(req) {
  const response = await fetch(`${API_BASE}/regression`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!response.ok) throw new Error(`Regression API error: ${response.status}`);
  return response.json();
}

// ---------- /api/knn ----------
export async function runKNN(req) {
  const response = await fetch(`${API_BASE}/knn`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!response.ok) throw new Error(`KNN API error: ${response.status}`);
  return response.json();
}

// ---------- /api/decision_tree ----------
export async function runDecisionTree(req) {
  const response = await fetch(`${API_BASE}/decision_tree`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!response.ok) throw new Error(`Decision Tree API error: ${response.status}`);
  return response.json();
}

// ---------- /api/genetic_algorithm ----------
export async function runGA(req) {
  const response = await fetch(`${API_BASE}/genetic_algorithm`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!response.ok) throw new Error(`Genetic Algorithm API error: ${response.status}`);
  return response.json();
}
