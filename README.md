# Emergent ML Visualizer — Interactive Academic GUI

> **Visualize, tune, and reason about four families of ML algorithms.**  
> A specification-first, decoupled client-server system for regression, KNN, decision trees, and genetic algorithms.

---

## 🎯 Overview

**Emergent** is a production-grade interactive GUI built strictly to the master specification (`spec.md`). It enables students and researchers to:

- **Visualize** decision boundaries, tree structures, population evolution, and regression fits in real-time
- **Tune** 30+ hyperparameters with live feedback (300ms debounce)
- **Understand** algorithms via interactive Theory drawers with KaTeX equations
- **Compare** side-by-side visualizations (e.g., Gini vs Entropy trees, Uniform vs Distance-weighted KNN)

### 📊 Features

| Criterion | Status |
|-----------|--------|
| **Quality & Usability** | ✅ Dark-mode React UI + Shadcn components |
| **Adjustable Parameters** | ✅ 30+ sliders, dropdowns, toggles across 4 algorithms |
| **Graphical Representations** | ✅ Plotly charts, react-d3-tree, contour plots |
| **Enhancements** | ✅ Early stopping, Lasso zero-tracking, **Feature Importance**, Gini vs Entropy compare, GA ghost overlay |
| **Documentation** | ✅ Theory drawers, spec.md, API contracts |

---

## 📸 Screenshots

### Regression — Linear, Polynomial, Ridge, Lasso, Elastic Net

![Regression Page](https://github.com/idhawal/emergent/raw/main/screenshots/regression.png)

**Features:**
- Algorithm selector (5 variants)
- Learning rate (log-scale slider)
- Epochs & polynomial degree
- Early stopping with amber alert
- **Live coefficient bar chart** with Lasso zero-counter
- Cost vs iterations convergence plot

---

### K-Nearest Neighbors — Interactive Boundary Classification & Regression

![KNN Page](https://github.com/idhawal/emergent/raw/main/screenshots/knn.png)

**Features:**
- K slider (1–50)
- Distance metrics (Euclidean, Manhattan)
- **Compare mode:** Uniform vs Distance-weighted side-by-side
- Interactive test points (click to drop)
- 2D decision boundary with contours
- Real-time neighbor highlighting

---

### Decision Trees — CART with Gini / Entropy & Live Pruning

![Decision Trees Page](https://github.com/idhawal/emergent/raw/main/screenshots/decision-tree.png)

**Features:**
- Pan-and-zoom interactive tree visualization
- Max depth / min samples controls for pruning
- **NEW: Feature Importance Bar Chart** ⭐ (shows top 8 features by importance)
- **Compare mode:** Gini vs Entropy side-by-side
- Live node grayout on pruning
- Accuracy & tree depth metrics

---

### Genetic Algorithms — Real-Coded GA with SBX Crossover & Polynomial Mutation

![Genetic Algorithms Page](https://github.com/idhawal/emergent/raw/main/screenshots/genetic-algorithm.png)

**Features:**
- Benchmark function selector (Sphere, Rosenbrock, Rastrigin)
- Population size & mutation controls
- 2D contour plot with population overlay
- Fitness vs generations convergence chart
- Play / Step animation controls
- **Ghost overlay** for previous runs
- Best point & average fitness tracking

---

## 🏗 Architecture

### Frontend (React 19)
```
frontend/src/
├── App.js                    # Route definitions
├── components/
│   ├── regression/RegressionPage.jsx
│   ├── knn/KNNPage.jsx
│   ├── decision-tree/TreePage.jsx        # ← Feature importance chart here
│   ├── genetic/GAPage.jsx
│   ├── layout/
│   │   ├── Navbar.jsx
│   │   ├── Sidebar.jsx
│   │   ├── MetricsPanel.jsx
│   │   └── PageShell.jsx
│   └── shared/
│       ├── PlotlyChart.jsx
│       ├── SkeletonLoader.jsx
│       └── TheoryDrawer.jsx
├── store/store.js            # Zustand state (per-algorithm)
├── hooks/useDebounce.js      # 300ms debounce utility
└── lib/api.js                # Mock/real API layer
```

### Backend (FastAPI)
```
backend/
├── server.py                 # FastAPI app + CORS
├── requirements.txt          # Dependencies
└── tests/                    # pytest suite (auto-run via CI)
```

### Specification
```
spec.md                        # Single source of truth (SSoT)
```

---

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ & yarn
- Python 3.11+

### Installation & Running

**Frontend:**
```bash
cd frontend
yarn install
yarn start
# Opens http://localhost:3000
```

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python server.py
# Runs on http://localhost:8000
```

---

## 🎓 Core Algorithms

### 1. Regression (4.1 of spec)
- **Algorithms:** Linear GD, Polynomial, Ridge, Lasso, Elastic Net
- **Features:** Custom gradient descent, Lasso coefficient tracking, early stopping
- **Visualizations:** Scatter + fit, cost history, coefficient bars

### 2. K-Nearest Neighbors (4.2 of spec)
- **Metrics:** Euclidean, Manhattan
- **Weights:** Uniform, Distance-weighted
- **Visualization:** 2D decision boundary with test point interaction

### 3. Decision Trees (4.3 of spec)
- **Criterion:** Gini impurity, Entropy (info gain)
- **Pruning:** Max depth, min samples split/leaf
- **Visualization:** Interactive tree diagram + **Feature Importance chart** (NEW)

### 4. Genetic Algorithms (4.4 of spec)
- **Encoding:** Real-coded
- **Crossover:** Simulated Binary Crossover (SBX)
- **Mutation:** Polynomial
- **Visualization:** Contour + population overlay + fitness history

---

## 📋 Parameter Reference

| Algorithm | Adjustable Parameters |
|-----------|----------------------|
| **Regression** | algo, learning_rate, epochs, poly_degree, penalty, l1_ratio, noise, early_stopping |
| **KNN** | k, metric, weights, task, dataset |
| **Decision Trees** | task, criterion, max_depth, min_samples_split, min_samples_leaf, dataset, compare_mode |
| **Genetic Algorithms** | function, pop_size, mutation_rate, crossover_rate, generations, nm, nc |

---

## 🎯 Enhancements (Criterion 4)

✅ **Early Stopping** — Halts training if cost increases ≥5 iterations; displays amber alert  
✅ **Lasso Zero-Coefficient Tracker** — Live counter shows how many features are zeroed out  
✅ **KNN Boundary Compare** — Uniform vs Distance-weighted side-by-side  
✅ **Decision Tree Pruning** — Real-time node grayout as depth/samples change  
✅ **Gini vs Entropy Compare** — Side-by-side trees with switching  
✅ **GA Ghost Overlay** — Previous run curves fade behind current evolution  
✅ **Feature Importance Chart** — Decision Trees page shows top 8 features by importance (NEW) ⭐  

---

## ✨ Recent Enhancements

### Feature Importance Visualization (NEW)
A horizontal bar chart now appears on the **Decision Trees** page, displaying:
- Top 8 features ranked by importance
- Percentage contribution (0–100%)
- Sorted descending
- Works in both single and compare (A/B) modes
- Responsive design with truncation for long names

### GitHub Actions CI (NEW)
Automated testing on every commit:
- Runs pytest across Python 3.11 & 3.12
- Caches dependencies for speed
- Reports coverage metrics
- Blocks merge on test failure

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=backend

# CI automatically runs on every push (see .github/workflows/test.yml)
```

---

## 📖 Documentation

- **spec.md** — Master specification (single source of truth)
- **Theory Drawers** — KaTeX equations + parameter guides on every page
- **README** — This file

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 19, Tailwind CSS, Shadcn UI, Plotly.js, react-d3-tree, Zustand |
| **Backend** | FastAPI, scikit-learn, NumPy, Pydantic |
| **Testing** | pytest, pytest-asyncio, pytest-cov |
| **CI/CD** | GitHub Actions |

---

## 📝 License

This project is part of an academic ML visualization lab. See LICENSE for details.

---

## 👨‍💻 Author

Built by [@idhawal](https://github.com/idhawal) with specification-driven architecture.

---

## 💡 Notes

- **Specification-First:** All code directly implements `spec.md`; UI and backend teams work independently
- **Decoupled:** React ↔ FastAPI via JSON/REST; swappable mock/real API layers
- **Educational:** Designed for students to understand algorithm behavior through interactive tuning
- **Production-Ready:** Error handling, validation, responsive design, accessibility

---

**Made with Emergent** 🌱
