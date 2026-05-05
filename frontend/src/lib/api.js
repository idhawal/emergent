// API layer for ML Visualizer backend.
// Makes HTTP requests to FastAPI backend per spec.md §5 contracts.

const API_BASE = process.env.REACT_APP_BACKEND_URL 
  ? `${process.env.REACT_APP_BACKEND_URL}/api`
  : null;

if (!API_BASE) {
  console.warn("[api.js] REACT_APP_BACKEND_URL is not set — using mock data.");
}

// Mock data generators
function generateMockRegressionData() {
  const x = Array.from({ length: 50 }, (_, i) => i * 0.5);
  const y_true = x.map(v => 2 * v + 0.5 + (Math.random() - 0.5) * 2);
  const y_pred = x.map(v => 2 * v + 0.5);
  
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

function generateMockKNNData() {
  const points = Array.from({ length: 100 }, () => [
    (Math.random() - 0.5) * 4,
    (Math.random() - 0.5) * 4
  ]);
  const labels = points.map(p => (p[0] * p[0] + p[1] * p[1] < 2 ? 0 : 1));
  
  const gridSize = 30;
  const mesh_xx = Array.from({ length: gridSize }, (_, i) => 
    Array.from({ length: gridSize }, (_, j) => -2 + (j / gridSize) * 4)
  );
  const mesh_yy = Array.from({ length: gridSize }, (_, i) => 
    Array.from({ length: gridSize }, () => -2 + (i / gridSize) * 4)
  );
  const mesh_zz = mesh_xx.map((row, i) => 
    row.map((x, j) => (x * x + mesh_yy[i][j] * mesh_yy[i][j] < 2 ? 0 : 1))
  );
  
  return {
    train_points: points,
    train_labels: labels,
    mesh_xx,
    mesh_yy,
    mesh_zz,
    test_prediction: null,
    neighbor_indices: [],
  };
}

function generateMockTreeData() {
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

function generateMockGAData() {
  const generations = 50;
  const history = [];
  
  for (let i = 0; i < generations; i++) {
    const best_fitness = 100 * Math.exp(-i / 10) + 0.01;
    const avg_fitness = 200 * Math.exp(-i / 15) + 5;
    const points = Array.from({ length: 30 }, () => [
      (Math.random() - 0.5) * 4 * Math.exp(-i / 30),
      (Math.random() - 0.5) * 4 * Math.exp(-i / 30)
    ]);
    const fitness_values = points.map(p => p[0] * p[0] + p[1] * p[1]);
    const best_idx = fitness_values.indexOf(Math.min(...fitness_values));
    
    history.push({
      generation: i,
      best_fitness,
      avg_fitness,
      points,
      fitness_values,
      best_point: points[best_idx]
    });
  }
  
  const gridSize = 40;
  const span = 5;
  const contour_x = [Array.from({ length: gridSize }, (_, i) => -span + (i / gridSize) * 2 * span)];
  const contour_y = Array.from({ length: gridSize }, (_, i) => [-span + (i / gridSize) * 2 * span]);
  const contour_z = contour_y.map(row => 
    contour_x[0].map(x => x * x + row[0] * row[0])
  );
  
  return {
    history,
    contour_x,
    contour_y,
    contour_z,
    span,
    converged_at_generation: 45
  };
}

// ---------- /api/regression ----------
export async function runRegression(req) {
  if (!API_BASE) {
    // Return mock data
    await new Promise(resolve => setTimeout(resolve, 300));
    return generateMockRegressionData();
  }
  
  try {
    const response = await fetch(`${API_BASE}/regression`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req),
    });
    if (!response.ok) {
      console.error(`Regression API error: ${response.status}`);
      return generateMockRegressionData();
    }
    return response.json();
  } catch (error) {
    console.error("Regression API network error:", error);
    return generateMockRegressionData();
  }
}

// ---------- /api/knn ----------
export async function runKNN(req) {
  if (!API_BASE) {
    await new Promise(resolve => setTimeout(resolve, 300));
    return generateMockKNNData();
  }
  
  try {
    const response = await fetch(`${API_BASE}/knn`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req),
    });
    if (!response.ok) {
      console.error(`KNN API error: ${response.status}`);
      return generateMockKNNData();
    }
    return response.json();
  } catch (error) {
    console.error("KNN API network error:", error);
    return generateMockKNNData();
  }
}

// ---------- /api/decision_tree ----------
export async function runDecisionTree(req) {
  if (!API_BASE) {
    await new Promise(resolve => setTimeout(resolve, 300));
    return generateMockTreeData();
  }
  
  try {
    const response = await fetch(`${API_BASE}/decision_tree`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req),
    });
    if (!response.ok) {
      console.error(`Decision Tree API error: ${response.status}`);
      return generateMockTreeData();
    }
    return response.json();
  } catch (error) {
    console.error("Decision Tree API network error:", error);
    return generateMockTreeData();
  }
}

// ---------- /api/genetic_algorithm ----------
export async function runGA(req) {
  if (!API_BASE) {
    await new Promise(resolve => setTimeout(resolve, 300));
    return generateMockGAData();
  }
  
  try {
    const response = await fetch(`${API_BASE}/genetic_algorithm`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req),
    });
    if (!response.ok) {
      console.error(`Genetic Algorithm API error: ${response.status}`);
      return generateMockGAData();
    }
    return response.json();
  } catch (error) {
    console.error("Genetic Algorithm API network error:", error);
    return generateMockGAData();
  }
}

// ---------- /api/upload-dataset ----------
export async function uploadDataset(file) {
  if (!API_BASE) {
    console.warn("Cannot upload dataset without backend URL");
    throw new Error("Backend URL not configured");
  }
  
  const formData = new FormData();
  formData.append("file", file);
  
  const response = await fetch(`${API_BASE}/upload-dataset`, {
    method: "POST",
    body: formData,
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Upload failed");
  }
  
  return response.json();
}

// ---------- /api/datasets/{name} ----------
export async function getDataset(name) {
  if (!API_BASE) {
    console.warn("Cannot fetch dataset without backend URL");
    return null;
  }
  
  const response = await fetch(`${API_BASE}/datasets/${name}`);
  if (!response.ok) {
    console.error(`Dataset API error: ${response.status}`);
    return null;
  }
  return response.json();
}
