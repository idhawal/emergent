# ML Visualizer GUI — Frontend

An interactive, academic-grade GUI for visualizing and tuning four families of Machine Learning algorithms: **Regression**, **K-Nearest Neighbors (KNN)**, **Decision Trees**, and **Genetic Algorithms**.

This repo contains the **frontend** implementation built strictly to the [master spec](./spec.md) — every adjustable parameter, chart, enhancement, and theory drawer described in the spec is wired up here.

---

## Highlights vs. spec

| Spec section | Implementation |
|---|---|
| §3 Global UI Layout | `Navbar` + `Sidebar` (Control Panel) + main visualization area + `MetricsPanel` |
| §4.1 Regression | Linear (GD), Polynomial, Ridge, Lasso, Elastic Net + log α slider, epoch input, λ select, l1_ratio, noise, early-stopping toggle. Live Scatter+Fit, Cost vs Iterations (log), Coefficient Bar Chart with red-zero highlighting and live `X of N features zeroed out` counter. Amber early-stop alert banner. |
| §4.2 KNN | Classification & regression, Euclidean / Manhattan, Uniform / Distance-weighted, Moons / Circles / Blobs / Sine. Decision boundary heatmap, click-to-place test point with neighbor-line overlay. **Compare Mode** — Uniform vs Distance side-by-side. |
| §4.3 Decision Trees | Classifier/Regressor, Gini/Entropy, max_depth (None or 1–10) with **live pruning**, min_samples_split/leaf, Iris/Breast Cancer/Blobs. `react-d3-tree` interactive node-link diagram with custom node card showing split rule + score + samples. **Compare Mode** — Gini vs Entropy side-by-side. |
| §4.4 Genetic Algorithms | Sphere / Rosenbrock / Rastrigin, all parameter sliders, 2D contour + population scatter, **Play / Pause / Step / scrub-slider**, Best vs Average fitness chart with **ghost overlay** for previous-function comparison. Convergence speed cards. |
| §5 API Contracts | Mocked in `src/lib/api.js` using the exact request/response shape from the spec. Swap with real FastAPI URLs by replacing function bodies. |
| §7 Theory Drawer | Right-side Shadcn `Sheet` per algorithm, with KaTeX-rendered equations (Entropy, Information Gain, Gini, GD update, Ridge/Lasso/Elastic Net, Euclidean/Manhattan, Sphere/Rosenbrock/Rastrigin), parameter guide tables, and usage instructions. |
| §8.2 Frontend checks | 300 ms `useDebounce` on every slider, Shadcn skeleton loaders on every API call, Plotly responsive (`useResizeHandler`). |

### Stack

- React 19 + Create React App (CRA) + Tailwind CSS + Shadcn UI
- Plotly.js via `react-plotly.js` for charts
- `react-d3-tree` for decision tree diagrams
- Zustand for per-algorithm state slices
- `katex` + `react-katex` for math typesetting

> **Note vs spec §2.1:** The spec recommends Vite + TypeScript. This project ships on the Emergent CRA template (React 19 + JS) for runtime stability — every other architectural decision (Shadcn, Plotly, react-d3-tree, Zustand, debounce, theory drawer) follows the spec exactly.

---

## Local Development

```bash
cd frontend
yarn install
yarn start   # http://localhost:3000
```

Set `REACT_APP_BACKEND_URL` in `frontend/.env` if you want to point at a real FastAPI backend later.

---

## Project Structure

```
frontend/src/
├── App.js                       # Routes for /regression, /knn, /decision-tree, /genetic-algorithm
├── components/
│   ├── Home.jsx                 # Landing page
│   ├── layout/
│   │   ├── Navbar.jsx           # Top nav + Theory button
│   │   ├── Sidebar.jsx          # Per-page Control Panel shell
│   │   ├── MetricsPanel.jsx     # Bottom metrics bar
│   │   └── PageShell.jsx
│   ├── shared/
│   │   ├── PlotlyChart.jsx      # Themed Plotly wrapper
│   │   ├── SkeletonLoader.jsx
│   │   └── TheoryDrawer.jsx     # Per-algorithm KaTeX-powered drawer
│   ├── regression/RegressionPage.jsx
│   ├── knn/KNNPage.jsx
│   ├── decision-tree/TreePage.jsx
│   └── genetic/GAPage.jsx
├── hooks/useDebounce.js         # 300 ms slider debounce (deep-equality safe)
├── store/store.js               # Zustand slices (UI + 4 algorithms)
└── lib/api.js                   # Mock implementations of every spec §5 endpoint
```

Every interactive element carries a `data-testid` attribute for automated UI tests.

---

## Replacing the mock with a real backend

In `src/lib/api.js`, each function (`runRegression`, `runKNN`, `runDecisionTree`, `runGA`) returns a `Promise` that mirrors the spec's response JSON exactly. To use the FastAPI backend, replace the body of each function with:

```js
import axios from "axios";
const API = process.env.REACT_APP_BACKEND_URL + "/api";

export async function runRegression(req) {
  const { data } = await axios.post(`${API}/regression`, req);
  return data;
}
// …same pattern for /knn, /decision_tree, /genetic_algorithm
```

No component changes are required — every page already consumes the spec-shaped response.

---

## License

MIT
