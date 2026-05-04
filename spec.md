# ML Visualizer GUI — Master Specification (`spec.md`)

> **Single source of truth.** Feed this file into every AI tool in the pipeline — UI generators (v0, Lovable, Bolt.new), backend coders (Cursor, Aider, Windsurf, Claude Code), and test writers alike.

---

## 1. Project Overview

An interactive, academic-grade GUI for visualizing and tuning four families of Machine Learning algorithms: **Regression**, **K-Nearest Neighbors (KNN)**, **Decision Trees**, and **Genetic Algorithms**. Graded on five criteria:

| # | Criterion |
|---|-----------|
| 1 | Quality and usability of the GUI |
| 2 | Number and relevance of adjustable parameters |
| 3 | Effectiveness of graphical representations |
| 4 | Additional enhancements that improve model performance/understanding |
| 5 | Clarity and completeness of documentation |

---

## 2. Architecture

The project uses a **decoupled Client–Server architecture** to allow UI and ML logic to be developed in parallel.

```
┌─────────────────────────────────┐        HTTP/REST (JSON)        ┌──────────────────────────────┐
│         FRONTEND (React)        │ ◄────────────────────────────► │      BACKEND (FastAPI)        │
│  v0 / Lovable / Bolt.new        │                                 │  Cursor / Aider / Claude Code │
└─────────────────────────────────┘                                 └──────────────────────────────┘
```

### 2.1 Frontend Stack

| Concern | Technology |
|---------|-----------|
| Framework | React 18+ with Vite (TypeScript) |
| Styling | Tailwind CSS |
| Component Library | Shadcn UI (Slider, Switch, Select, Card, Tooltip, Drawer) |
| Data Visualization | Plotly.js via `react-plotly.js` |
| Tree Visualization | `react-d3-tree` |
| State Management | Zustand or React Context |
| HTTP Client | `axios` with 300 ms debounce on slider inputs |

### 2.2 Backend Stack

| Concern | Technology |
|---------|-----------|
| Framework | Python 3.11+, FastAPI |
| ML & Math | `scikit-learn`, `numpy`, `scipy`, `pandas` |
| Data Validation | Pydantic v2 models (strict typing, range validators) |
| Testing | `pytest` + `pytest-asyncio` |
| Server | `uvicorn` |

---

## 3. Global UI Layout

Every page shares the same shell:

```
┌──────────────────────────────────────────────────────────────────────┐
│  TOP NAV: [Regression] [KNN] [Decision Trees] [Genetic Algorithms]  [?Docs]  │
├───────────────────────┬──────────────────────────────────────────────┤
│                       │                                              │
│   LEFT SIDEBAR        │           MAIN VISUALIZATION AREA           │
│   (Control Panel)     │   (Plotly charts / react-d3-tree)           │
│                       │   Supports split-screen / side-by-side      │
│   • Algorithm selector│                                              │
│   • All hyperparameter│                                              │
│     sliders/dropdowns │                                              │
│   • Run / Reset btn   │                                              │
│                       │                                              │
├───────────────────────┴──────────────────────────────────────────────┤
│  BOTTOM METRICS PANEL: Real-time stats, logs, coefficient tracker    │
└──────────────────────────────────────────────────────────────────────┘
```

**Global UX rules:**
- Show Shadcn skeleton loaders while awaiting API responses.
- Debounce all slider `onChange` events by **300 ms** before firing API calls.
- Each algorithm page has an **"ⓘ Theory"** drawer/modal (see §7).
- Mobile-responsive layout (Tailwind `lg:` breakpoints for sidebar collapse).

---

## 4. Algorithm Specifications

---

### 4.1 Regression Family

**Algorithms:** Linear Regression (Custom Gradient Descent), Polynomial Regression, Ridge, Lasso, Elastic Net.

#### 4.1.1 Dataset
- Synthetic 2D dataset generated server-side.
- Adjustable **noise level** slider (0.0 – 1.0) on the frontend.

#### 4.1.2 Adjustable Parameters

| Parameter | Control | Range / Options |
|-----------|---------|-----------------|
| Algorithm | Dropdown | Linear GD, Polynomial, Ridge, Lasso, Elastic Net |
| Learning Rate (α) | Logarithmic slider | 0.0001 → 1.0 |
| Epochs / Iterations | Number input | 1 → 10 000 |
| Polynomial Degree | Slider | 1, 2, 3, 4 |
| Regularization Penalty (λ/α) | Select | 0.01, 0.1, 1, 10, 100 |
| l1_ratio (Elastic Net only) | Slider | 0.2, 0.5, 0.8 |
| Noise Level | Slider | 0.0 → 1.0 |
| Early Stopping | Toggle (Checkbox) | On / Off |

#### 4.1.3 Graphical Representations

| Chart | Description |
|-------|-------------|
| **Scatter + Fit** | Plotly scatter of raw data points overlaid with the fitted regression line/curve. Updates live. |
| **Cost vs. Iterations** | Plotly line graph showing gradient descent convergence curve. |
| **Coefficient Bar Chart** | Dynamic bar chart of feature weights. Coefficients that drop to zero (Lasso) are highlighted in red. |

#### 4.1.4 Required Enhancements

1. **Early Stopping:** When the toggle is ON, the backend halts training if the cost function increases for **5 consecutive iterations**. The API response includes `stopped_at_epoch`. The UI displays an amber alert banner: *"Early stopping triggered at epoch {X}."*
2. **Lasso Zero-Coefficient Tracker:** As the penalty (λ) increases, the coefficient bar chart animates weights snapping to zero, with a live counter: *"X of N features zeroed out."*

---

### 4.2 K-Nearest Neighbors (KNN)

**Mode:** Classification and Regression (toggled by user).

#### 4.2.1 Dataset

| Mode | Dataset Options |
|------|----------------|
| Classification | Moons, Circles, Blobs (Sklearn `make_*`) |
| Regression | Sine wave with adjustable Gaussian noise |

#### 4.2.2 Adjustable Parameters

| Parameter | Control | Range / Options |
|-----------|---------|-----------------|
| Task Mode | Toggle | Classification / Regression |
| K (Neighbors) | Integer slider | 1 → 50 |
| Distance Metric | Dropdown | Euclidean, Manhattan |
| Weighting | Toggle | Uniform / Distance-Weighted |
| Dataset | Dropdown | Moons, Circles, Blobs, Sine |

#### 4.2.3 Graphical Representations

| Chart | Description |
|-------|-------------|
| **Decision Boundary Plot** | Plotly scatter of training points. Colored background meshgrid encodes predicted class for every point in 2D space. |
| **Test Point Interaction** | User clicks on the plot to place a test point. A circle radius visually connects it to its K nearest neighbors (drawn as lines). Tooltip shows predicted class/value. |

#### 4.2.4 Required Enhancements

1. **Boundary Comparison Mode:** A split-screen or quick-toggle that renders the **Uniform** decision boundary alongside the **Distance-Weighted** boundary on the same dataset simultaneously, so users can observe the difference.

---

### 4.3 Decision Trees

**Algorithms:** Decision Tree Classifier and Decision Tree Regressor (`sklearn.tree`).

#### 4.3.1 Dataset
- Classification: Iris, Breast Cancer (Sklearn built-ins), or synthetic Blobs.
- Regressor: Synthetic polynomial data.

#### 4.3.2 Adjustable Parameters

| Parameter | Control | Range / Options |
|-----------|---------|-----------------|
| Task Mode | Toggle | Classifier / Regressor |
| Splitting Criterion | Dropdown | Gini Impurity, Entropy (Info Gain) |
| Max Depth | Slider | None (unconstrained), 1 → 10 |
| Min Samples Split | Slider | 2 → 20 |
| Min Samples Leaf | Slider | 1 → 20 |
| Dataset | Dropdown | Iris, Breast Cancer, Blobs |

#### 4.3.3 Graphical Representations

| Chart | Description |
|-------|-------------|
| **Node-Link Tree Diagram** | `react-d3-tree` interactive tree. Pan, zoom supported. Hover tooltip on each node shows: split rule (e.g., `petal_length ≤ 2.45`), Gini/Entropy value, sample count, class distribution. |
| **2D Decision Boundary** *(optional)* | Plotly meshgrid showing decision regions for 2-feature datasets. |

#### 4.3.4 Required Enhancements

1. **Side-by-Side Gini vs. Entropy Comparison:** The UI renders **Tree A (Gini)** and **Tree B (Entropy)** simultaneously on the same dataset. Metrics panel shows accuracy, depth, and leaf count for each.
2. **Pruning Demonstration:** As the user drags the **Max Depth** slider, the tree diagram animates — nodes beyond the depth limit are grayed out / hidden in real time, visually demonstrating overfitting mitigation.

---

### 4.4 Genetic Algorithms (Evolutionary Computation)

**Algorithm:** Real-Coded Genetic Algorithm applied to benchmark optimization functions.

#### 4.4.1 Benchmark Functions

| Function | Formula (2D) |
|----------|-------------|
| Sphere | `f(x) = Σ xᵢ²` |
| Rosenbrock | `f(x,y) = (1-x)² + 100(y-x²)²` |
| Rastrigin | `f(x) = 10n + Σ [xᵢ² - 10cos(2πxᵢ)]` |

#### 4.4.2 Adjustable Parameters

| Parameter | Control | Range / Options |
|-----------|---------|-----------------|
| Benchmark Function | Dropdown | Sphere, Rosenbrock, Rastrigin |
| Population Size | Slider | 10 → 200 |
| Mutation Rate | Slider | 0.0 → 1.0 |
| Crossover Rate | Slider | 0.0 → 1.0 |
| Generations | Number input | 1 → 500 |
| Distribution Index ηₘ (mutation) | Slider | 1 → 50 |
| Distribution Index ηc (crossover) | Slider | 1 → 50 |

#### 4.4.3 Graphical Representations

| Chart | Description |
|-------|-------------|
| **2D Contour + Population** | Plotly 2D contour plot of selected benchmark function. Population individuals overlaid as scatter points. Color encodes fitness. |
| **Playback Controls** | Play ▶ / Pause ⏸ / Step Forward ⏭ / Scrub slider to animate population movement across generations. |
| **Fitness vs. Generations** | Plotly dual line chart: Best Fitness and Average Fitness over generations. |

#### 4.4.4 Required Enhancements

1. **Convergence Speed Comparison Cards:** After a run, metric cards display generation at which best fitness was found for the selected function, allowing parameter-to-parameter comparison.
2. **Function Switcher with State Preservation:** When the user switches benchmark functions via dropdown, previous fitness history is preserved in a "ghost" overlay on the Fitness chart for direct comparison.

---

## 5. API Data Contracts

All requests are `POST`. All responses are `application/json`. Pydantic models enforce all input ranges server-side.

### `POST /api/regression`

```json
// Request
{
  "algo": "lasso",              // "linear_gd" | "polynomial" | "ridge" | "lasso" | "elastic_net"
  "learning_rate": 0.01,
  "epochs": 1000,
  "poly_degree": 1,
  "penalty": 10.0,
  "l1_ratio": 0.5,
  "noise": 0.3,
  "early_stopping": true
}

// Response
{
  "curve_x": [float, ...],
  "curve_y": [float, ...],
  "scatter_x": [float, ...],
  "scatter_y": [float, ...],
  "cost_history": [float, ...],
  "coefficients": [float, ...],
  "feature_names": ["string", ...],
  "stopped_at_epoch": 342         // null if early stopping not triggered
}
```

### `POST /api/knn`

```json
// Request
{
  "k": 5,
  "metric": "euclidean",          // "euclidean" | "manhattan"
  "weights": "distance",          // "uniform" | "distance"
  "task": "classification",       // "classification" | "regression"
  "dataset": "moons",             // "moons" | "circles" | "blobs" | "sine"
  "test_point": [1.2, -0.5]       // null if no test point placed
}

// Response
{
  "train_points": [[float, float], ...],
  "train_labels": [int, ...],
  "mesh_xx": [[float, ...], ...],
  "mesh_yy": [[float, ...], ...],
  "mesh_zz": [[int, ...], ...],
  "neighbor_indices": [int, ...],
  "test_prediction": 1            // int (class) or float (regression value)
}
```

### `POST /api/decision_tree`

```json
// Request
{
  "task": "classifier",           // "classifier" | "regressor"
  "criterion": "gini",            // "gini" | "entropy"
  "max_depth": 3,                 // null for unconstrained
  "min_samples_split": 2,
  "min_samples_leaf": 1,
  "dataset": "iris"               // "iris" | "breast_cancer" | "blobs"
}

// Response
{
  "tree_json": { /* nested node structure — see §5.1 */ },
  "accuracy": 0.96,
  "depth": 3,
  "n_leaves": 8,
  "feature_importances": {"feature_name": float, ...}
}
```

#### 5.1 `tree_json` Node Schema (for `react-d3-tree`)

```json
{
  "name": "petal_length ≤ 2.45",
  "attributes": {
    "gini": 0.32,
    "samples": 150,
    "class_dist": [50, 50, 50]
  },
  "children": [ /* recursive same structure */ ]
}
```

### `POST /api/genetic_algorithm`

```json
// Request
{
  "function": "rastrigin",        // "sphere" | "rosenbrock" | "rastrigin"
  "pop_size": 50,
  "mutation_rate": 0.1,
  "crossover_rate": 0.8,
  "generations": 100,
  "eta_m": 20,
  "eta_c": 15
}

// Response
{
  "contour_x": [[float, ...], ...],
  "contour_y": [[float, ...], ...],
  "contour_z": [[float, ...], ...],
  "history": [
    {
      "generation": 1,
      "points": [[float, float], ...],
      "fitness_values": [float, ...],
      "best_fitness": float,
      "avg_fitness": float,
      "best_point": [float, float]
    }
  ],
  "converged_at_generation": 45   // null if did not converge
}
```

---

## 6. Pydantic Validation Rules (Backend)

```python
# Examples — enforce these for all models

class RegressionRequest(BaseModel):
    algo: Literal["linear_gd","polynomial","ridge","lasso","elastic_net"]
    learning_rate: float = Field(gt=0, le=1.0)
    epochs: int = Field(ge=1, le=10000)
    poly_degree: int = Field(ge=1, le=4)
    penalty: float = Field(ge=0)
    l1_ratio: float = Field(ge=0.0, le=1.0)
    noise: float = Field(ge=0.0, le=1.0)
    early_stopping: bool = False

class KNNRequest(BaseModel):
    k: int = Field(ge=1, le=50)
    metric: Literal["euclidean", "manhattan"]
    weights: Literal["uniform", "distance"]
    task: Literal["classification", "regression"]
    dataset: Literal["moons", "circles", "blobs", "sine"]
    test_point: Optional[List[float]] = None

class DecisionTreeRequest(BaseModel):
    task: Literal["classifier", "regressor"]
    criterion: Literal["gini", "entropy"]
    max_depth: Optional[int] = Field(None, ge=1, le=10)
    min_samples_split: int = Field(ge=2, le=20)
    min_samples_leaf: int = Field(ge=1, le=20)
    dataset: Literal["iris", "breast_cancer", "blobs"]

class GeneticAlgorithmRequest(BaseModel):
    function: Literal["sphere", "rosenbrock", "rastrigin"]
    pop_size: int = Field(ge=10, le=200)
    mutation_rate: float = Field(ge=0.0, le=1.0)
    crossover_rate: float = Field(ge=0.0, le=1.0)
    generations: int = Field(ge=1, le=500)
    eta_m: float = Field(ge=1, le=50)
    eta_c: float = Field(ge=1, le=50)
```

---

## 7. Documentation / Theory Drawers (Criterion 5)

Every algorithm page has a persistent **"ⓘ Theory"** button that opens a side drawer. Required content:

| Section | Content |
|---------|---------|
| **Model Explanation** | Conceptual description (2–3 paragraphs) grounded in lecture material |
| **Mathematical Formulation** | Key equations rendered with KaTeX (e.g., Entropy, Gini, Information Gain, Gradient Descent update rule) |
| **Parameter Guide** | Table explaining what each slider/dropdown does mathematically and practically |
| **Usage Instructions** | Step-by-step walkthrough for that specific page |

### Key equations to include per algorithm

**Decision Tree:**
- Entropy: `Info(D) = -Σ pᵢ log₂(pᵢ)`
- Information Gain: `Gain(A) = Info(D) - InfoA(D)`
- Gini: `Gini(D) = 1 - Σ pᵢ²`

**Regression (Gradient Descent):**
- Cost: `J(θ) = (1/2m) Σ (hθ(xᵢ) - yᵢ)²`
- Update: `θⱼ := θⱼ - α · (∂J/∂θⱼ)`

**Lasso/Ridge:**
- Ridge: `J(θ) + λ Σ θⱼ²`
- Lasso: `J(θ) + λ Σ |θⱼ|`
- Elastic Net: `J(θ) + λ [l1_ratio · Σ|θⱼ| + (1-l1_ratio)/2 · Σθⱼ²]`

**KNN (Distance):**
- Euclidean: `d(x,y) = √Σ(xᵢ-yᵢ)²`
- Manhattan: `d(x,y) = Σ|xᵢ-yᵢ|`

---

## 8. QA, Testing, and Debugging Plan

### 8.1 Backend Unit Tests (`pytest`)

| Test | Description |
|------|-------------|
| `test_gradient_descent_convergence` | Verify custom GD loss decreases monotonically on clean data |
| `test_early_stopping_trigger` | Assert training halts at correct epoch when cost increases ≥5 times consecutively |
| `test_gd_matches_sklearn` | Custom gradient descent coefficients match `LinearRegression` within tolerance 1e-2 |
| `test_lasso_zero_coefficients` | Confirm ≥1 coefficient is zero when penalty=100 on sparse data |
| `test_tree_json_structure` | Validate `tree_json` has `name`, `attributes`, and `children` keys recursively |
| `test_ga_fitness_decreases` | Best fitness in generation N ≤ best fitness in generation 1 for minimization |
| `test_pydantic_rejects_invalid` | Each endpoint rejects out-of-range values with HTTP 422 |

### 8.2 Frontend Checks

- Plotly charts resize correctly on window resize (use `useResizeObserver`).
- Slider debounce: no API call fires within 300 ms of last slider movement.
- Loading skeletons appear on every API call.
- Split-screen layout does not overflow on 1280px viewport.

---

## 9. Directory Structure

```
ml-visualizer/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/          # Navbar, Sidebar, MetricsPanel
│   │   │   ├── regression/      # RegressionPage, CostChart, CoeffChart
│   │   │   ├── knn/             # KNNPage, BoundaryPlot, TestPointLayer
│   │   │   ├── decision-tree/   # TreePage, TreeDiagram, ComparisonView
│   │   │   ├── genetic/         # GAPage, ContourPlot, FitnessChart, Playback
│   │   │   └── shared/          # TheoryDrawer, SkeletonLoader, AlertBanner
│   │   ├── hooks/               # useDebounce, useMLApi
│   │   ├── store/               # Zustand slices per algorithm
│   │   └── types/               # TypeScript interfaces mirroring API contracts
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app, CORS, router inclusion
│   │   ├── routers/
│   │   │   ├── regression.py
│   │   │   ├── knn.py
│   │   │   ├── decision_tree.py
│   │   │   └── genetic_algorithm.py
│   │   ├── models/              # Pydantic request/response models
│   │   ├── services/            # Pure ML logic (no FastAPI deps)
│   │   │   ├── regression_service.py
│   │   │   ├── knn_service.py
│   │   │   ├── tree_service.py
│   │   │   └── ga_service.py
│   │   └── utils/
│   │       └── tree_parser.py   # sklearn tree → react-d3-tree JSON
│   └── tests/
│       ├── test_regression.py
│       ├── test_knn.py
│       ├── test_decision_tree.py
│       └── test_ga.py
│
├── spec.md                      # ← this file
└── README.md
```

---

## 10. AI Agent Directives

### For UI Generators (v0, Lovable, Bolt.new)

- Use **Shadcn UI** components exclusively for controls.
- Mock all API responses using the JSON structures in §5 for initial previews.
- Use `react-plotly.js` for all charts — do not substitute with Chart.js or Recharts.
- Use `react-d3-tree` for the Decision Tree diagram — do not render as SVG manually.
- Implement the global layout from §3 exactly.
- Every page must include the **"ⓘ Theory"** button wired to a Shadcn `Sheet` (drawer).
- Add **amber `Alert`** component for Early Stopping notification in Regression page.
- Animate Lasso coefficient bar chart using Plotly's `animate` API.

### For Backend Coders (Cursor, Aider, Windsurf, Claude Code)

- All ML logic lives in `services/` — routers only parse requests and call services.
- Custom Gradient Descent must be **implemented from scratch with NumPy** (not sklearn). Sklearn is used only for Polynomial, Ridge, Lasso, Elastic Net.
- For the Decision Tree JSON, traverse `sklearn.tree_.Tree` object to produce the nested structure defined in §5.1 — do not use `export_graphviz`.
- Genetic Algorithm must implement **Simulated Binary Crossover (SBX)** and **Polynomial Mutation** using `eta_c` and `eta_m` as defined in the lecture material (Real Coded GA).
- All NumPy operations must be vectorized — avoid Python loops over samples.
- CORS must allow `http://localhost:3000` (and configurable via `.env`).

---

## 11. Environment & Setup

### Backend

```bash
# Create virtualenv
python -m venv venv && source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn scikit-learn numpy scipy pandas pydantic pytest pytest-asyncio

# Run dev server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
# Install dependencies
npm install

# Install key packages
npm install react-plotly.js plotly.js react-d3-tree @radix-ui/react-slider zustand axios

# Run dev server
npm run dev   # runs on http://localhost:3000
```

### `.env` (Backend root)

```
CORS_ORIGIN=http://localhost:3000
```

---

*End of spec.md — version 1.0*
