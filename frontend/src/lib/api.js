// api.js - ML Visualizer backend client
// Falls back to deterministic mock data when backend is unreachable.

const API_BASE = process.env.REACT_APP_BACKEND_URL
  ? `${process.env.REACT_APP_BACKEND_URL}/api`
  : null;

export const isBackendConfigured = Boolean(API_BASE);

if (!isBackendConfigured) {
  console.info("[api] No REACT_APP_BACKEND_URL - running in demo mode.");
}

function mockRegression() {
  const x = Array.from({ length: 50 }, (_, i) => i * 0.5);
  const y_true = x.map((v) => 2 * v + 0.5 + (Math.random() - 0.5) * 2);
  const y_pred = x.map((v) => 2 * v + 0.5);
  return {
    scatter_x: x,
    scatter_y: y_true,
    curve_x: x,
    curve_y: y_pred,
    cost_history: Array.from({ length: 100 }, (_, i) => 10 * Math.exp(-i / 20)),
    coefficients: [2.0, 0.5, -0.1],
    feature_names: ["x1", "x2", "bias"],
    stopped_at_epoch: null,
  };
}

function mockKNN() {
  const pts = Array.from({ length: 100 }, () => [
    (Math.random() - 0.5) * 4,
    (Math.random() - 0.5) * 4,
  ]);
  const labels = pts.map((p) => (p[0] ** 2 + p[1] ** 2 < 2 ? 0 : 1));
  const G = 30;
  const mesh_xx = Array.from({ length: G }, () =>
    Array.from({ length: G }, (_, j) => -2 + (j / G) * 4)
  );
  const mesh_yy = Array.from({ length: G }, (_, i) =>
    Array.from({ length: G }, () => -2 + (i / G) * 4)
  );
  const mesh_zz = mesh_xx.map((row, i) =>
    row.map((x, j) => (x ** 2 + mesh_yy[i][j] ** 2 < 2 ? 0 : 1))
  );
  return {
    train_points: pts,
    train_labels: labels,
    mesh_xx,
    mesh_yy,
    mesh_zz,
    test_prediction: null,
    neighbor_indices: [],
  };
}

function mockTree() {
  return {
    tree_json: {
      name: "petal_length <= 2.45",
      attributes: { gini: 0.667, samples: 150 },
      children: [
        {
          name: "Leaf: setosa",
          attributes: { gini: 0.0, samples: 50 },
          children: []
        },
        {
          name: "petal_width <= 1.75",
          attributes: { gini: 0.5, samples: 100 },
          children: [
            {
              name: "Leaf: versicolor",
              attributes: { gini: 0.0, samples: 54 },
              children: []
            },
            {
              name: "Leaf: virginica",
              attributes: { gini: 0.0, samples: 46 },
              children: []
            }
          ]
        }
      ]
    },
    accuracy: 0.97,
    depth: 3,
    n_leaves: 3,
    feature_importances: {
      "petal_length": 0.45,
      "petal_width": 0.42,
      "sepal_length": 0.08,
      "sepal_width": 0.05
    }
  };
}

function mockGA() {
  const gens = 50;
  const history = Array.from({ length: gens }, (_, i) => {
    const pts = Array.from({ length: 30 }, () => [
      (Math.random() - 0.5) * 4 * Math.exp(-i / 30),
      (Math.random() - 0.5) * 4 * Math.exp(-i / 30),
    ]);
    const fitness = pts.map((p) => p[0] ** 2 + p[1] ** 2);
    const bestIdx = fitness.indexOf(Math.min(...fitness));
    return {
      generation: i,
      best_fitness: 100 * Math.exp(-i / 10) + 0.01,
      avg_fitness: 200 * Math.exp(-i / 15) + 5,
      points: pts,
      fitness_values: fitness,
      best_point: pts[bestIdx],
    };
  });
  const G = 40;
  const span = 5;
  const contour_x = [Array.from({ length: G }, (_, i) => -span + (i / G) * 2 * span)];
  const contour_y = Array.from({ length: G }, (_, i) => [-span + (i / G) * 2 * span]);
  const contour_z = contour_y.map((row) => contour_x[0].map((x) => x ** 2 + row[0] ** 2));
  return {
    history,
    contour_x,
    contour_y,
    contour_z,
    span,
    converged_at_generation: 45
  };
}

async function apiFetch(path, body, signal) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal,
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

async function withFallback(path, body, mockFn, signal) {
  if (!isBackendConfigured) {
    await new Promise((resolve) => setTimeout(resolve, 250));
    return { data: mockFn(), isDemo: true };
  }
  try {
    const data = await apiFetch(path, body, signal);
    return { data, isDemo: false };
  } catch (err) {
    if (err.name === "AbortError") throw err;
    console.warn(`[api] ${path} failed, using demo data:`, err.message);
    return { data: mockFn(), isDemo: true };
  }
}

export async function runRegression(req, signal) {
  return withFallback("/regression", req, mockRegression, signal);
}

export async function runKNN(req, signal) {
  return withFallback("/knn", req, mockKNN, signal);
}

export async function runDecisionTree(req, signal) {
  return withFallback("/decision_tree", req, mockTree, signal);
}

export async function runGA(req, signal) {
  return withFallback("/genetic_algorithm", req, mockGA, signal);
}

export async function uploadDataset(file) {
  if (!isBackendConfigured) throw new Error("Backend not configured.");
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/upload-dataset`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || "Upload failed");
  }

  return response.json();
}

export async function getDataset(name) {
  if (!isBackendConfigured) return null;
  const response = await fetch(`${API_BASE}/datasets/${name}`);
  if (!response.ok) return null;
  return response.json();
}

export async function listDatasets() {
  if (!isBackendConfigured) return ["iris", "breast_cancer", "moons", "circles", "blobs", "linear", "sine", "quadratic"];
  const response = await fetch(`${API_BASE}/datasets`);
  if (!response.ok) return [];
  const json = await response.json();
  return json.datasets || [];
}
