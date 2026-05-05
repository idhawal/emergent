# ML Visualizer

Interactive web application for exploring and tuning machine learning algorithms with real-time visualization. All algorithms are implemented from scratch using NumPy.

**Live Deployment:**
- **Frontend**: https://emergent-six-zeta.vercel.app/
- **Backend API**: https://emergent-av9b.onrender.com/docs

---

## Supported Algorithms

| Algorithm | Features |
|-----------|----------|
| **Regression** | Linear, Polynomial, Ridge, Lasso, Elastic Net with gradient descent visualization |
| **K-Nearest Neighbors** | Interactive 2D boundaries, Euclidean/Manhattan distance, weighted voting |
| **Decision Trees** | CART classifier/regressor, Gini/Entropy comparison, depth pruning, feature importance |
| **Genetic Algorithm** | Real-coded with SBX crossover, polynomial mutation, benchmark functions |

Each algorithm page includes a theory drawer with mathematical equations and parameter documentation.

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Frontend | React 19, Tailwind CSS, shadcn/ui |
| Visualization | Plotly.js, react-d3-tree |
| State | Zustand |
| Backend | FastAPI, Python 3.11 |
| ML Implementation | NumPy (no sklearn models) |
| Validation | Pydantic v2 |
| Testing | pytest (122 tests) |
| Deployment | Vercel (frontend), Render (backend) |

---

## Quick Start

**Requirements**: Python 3.11+, Node.js 18+, yarn

### Backend
```bash
cd backend
pip install -r requirements.txt
python server.py
```
Backend runs on `http://localhost:8000`

### Frontend
```bash
cd frontend
yarn install
echo "REACT_APP_BACKEND_URL=http://localhost:8000" > .env.local
yarn start
```
Frontend runs on `http://localhost:3000`

---

## Datasets

Built-in datasets: `linear`, `sine`, `quadratic` (regression); `iris`, `breast_cancer`, `moons`, `circles`, `blobs` (classification).

Custom CSV files can be uploaded from any algorithm page.

---

## Testing

```bash
cd backend
pytest tests/ -v
```

Verify from-scratch implementations:
```bash
rg "from sklearn.linear_model|from sklearn.neighbors|from sklearn.tree" backend/app/services/
# Should return no results
```

---

## Deployment

**Vercel (Frontend)**
1. Connect `frontend/` directory
2. Set `REACT_APP_BACKEND_URL=https://<your-backend>.onrender.com`

**Render (Backend)**
1. Connect `backend/` directory
2. Build: `pip install -r requirements.txt`
3. Start: `python server.py`
4. Optionally set `FRONTEND_URL` for CORS

---

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Algorithm pages and shared UI
│   ├── store/store.js    # Zustand state management
│   ├── lib/api.js        # API client
│   └── hooks/            # Custom hooks

backend/
├── app/
│   ├── routers/          # API endpoints
│   ├── services/         # ML implementations
│   ├── models/           # Pydantic schemas
│   └── main.py           # FastAPI app
└── tests/                # Test suite
```

---

## Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design, component structure, data flow, and testing strategy

---

## Status

- **Frontend**: Live at Vercel (auto-deploys on main push)
- **Backend**: Live at Render (auto-deploys on main push)  
- **Health Check**: `https://emergent-av9b.onrender.com/health`

---

## Team Members

- **Aryan Chawla,         Roll Number:23124019**
- **Chirag Bishnoi,       Roll Number:23124027**
- **Chaudari Arpit Kumar, Roll Number:23124026**
- **Dhawal Palaiya,       Roll Number:23124030**

---

## License

MIT
