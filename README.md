# ML Visualizer

An interactive web application for exploring and tuning four families of machine learning algorithms. Adjust parameters in real time, watch decision boundaries redraw, and inspect the math behind each model through built-in theory panels.

**Live demo ->** [YOUR_VERCEL_URL](https://YOUR_VERCEL_URL)

---

## Algorithms

| Module | What you can explore |
|---|---|
| **Regression** | Linear - Polynomial - Ridge - Lasso - Elastic Net with live gradient descent and early stopping |
| **K-Nearest Neighbors** | Interactive 2D decision boundaries - click to drop test points - Euclidean vs Manhattan distance - uniform vs distance-weighted voting |
| **Decision Trees** | CART classifier and regressor - Gini vs Entropy side-by-side - live depth pruning - feature importance chart |
| **Genetic Algorithms** | Real-coded GA with SBX crossover - polynomial mutation - Sphere / Rosenbrock / Rastrigin benchmark functions - play / step / ghost-overlay animation |

Every page includes a **Theory drawer** with KaTeX-rendered equations and parameter guides.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19, Tailwind CSS, shadcn/ui |
| Visualisation | Plotly.js, react-d3-tree |
| State | Zustand |
| Backend | FastAPI, Python 3.11 |
| ML / Math | NumPy (all algorithms implemented from scratch - no sklearn models) |
| Validation | Pydantic v2 |
| Tests | pytest (107 tests) |
| Deployment | Vercel (frontend) + Render (backend) |

---

## Screenshots

<table>
  <tr>
    <td><img src="screenshots/regression.png" alt="Regression" /></td>
    <td><img src="screenshots/knn.png" alt="KNN" /></td>
  </tr>
  <tr>
    <td><img src="screenshots/decision-tree.png" alt="Decision Trees" /></td>
    <td><img src="screenshots/genetic-algorithm.png" alt="Genetic Algorithms" /></td>
  </tr>
</table>

---

## Running Locally

**Requirements:** Python 3.11+, Node.js 18+, yarn

```bash
# Backend
cd backend
pip install -r requirements.txt
python server.py          # http://localhost:8000

# Frontend (new terminal)
cd frontend
yarn install
echo "REACT_APP_BACKEND_URL=http://localhost:8000" > .env.local
yarn start                # http://localhost:3000
```

**Backend health check:** `curl http://localhost:8000/health`

---

## Datasets

Built-in datasets are served by the backend:

| Name | Type | Source |
|---|---|---|
| `linear` | Regression | Synthetic (NumPy) |
| `sine` | Regression | Synthetic (NumPy) |
| `quadratic` | Regression | Synthetic (NumPy) |
| `iris` | Classification | sklearn |
| `breast_cancer` | Classification | sklearn |
| `moons` | Classification | sklearn |
| `circles` | Classification | sklearn |
| `blobs` | Classification/Regression | sklearn |

You can also upload your own `.csv` file from any algorithm page.

---

## Tests

```bash
cd backend
pytest tests/ -v
# 107 tests: unit - integration - from-scratch verification - Pydantic validation
```

To verify that no sklearn models are used in the algorithm implementations:

```bash
rg "from sklearn.linear_model import|from sklearn.neighbors import|from sklearn.tree import DecisionTree" backend/app/services/
# Should return no results
```

---

## Deployment

**Vercel (frontend)**
1. Connect the `frontend/` directory
2. Set environment variable: `REACT_APP_BACKEND_URL=https://<your-render-service>.onrender.com`

**Render (backend)**
1. Connect the `backend/` directory
2. Build command: `pip install -r requirements.txt`
3. Start command: `python server.py`
4. Optionally set: `FRONTEND_URL=https://<your-vercel-url>.vercel.app`

---

## Project Structure

```
├── frontend/
│   ├── src/
│   │   ├── components/       # React pages and shared UI
│   │   ├── store/store.js    # Zustand state
│   │   ├── lib/api.js        # Backend client with demo-data fallback
│   │   └── hooks/            # useDebounce
│   └── public/
└── backend/
    ├── app/
    │   ├── routers/          # FastAPI route handlers
    │   ├── services/         # From-scratch algorithm implementations
    │   ├── models/schemas.py # Pydantic request/response models
    │   └── main.py           # App factory + CORS
    └── tests/                # pytest suite
```

---

## License

MIT
