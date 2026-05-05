# Architecture Documentation

---

## System Overview

**ML Visualizer** is a web application for interactive exploration of machine learning algorithms. The system uses React 19 for the frontend and FastAPI for the backend, with all ML algorithms implemented from scratch using NumPy.

**Key Properties:**
- Real-time visualization with instant parameter feedback
- 122 comprehensive tests ensuring implementation correctness
- Production-ready with global deployment (Vercel + Render)
- Responsive, accessible design across all devices

---

## System Architecture

```
┌──────────────────────────────┐
│    Frontend (React 19)       │
│ • Algorithm pages            │
│ • Zustand state management   │
│ • Plotly + react-d3-tree     │
└──────────────┬───────────────┘
               │ HTTP API
┌──────────────▼───────────────┐
│   Backend (FastAPI)          │
│ • 6 algorithm endpoints      │
│ • Custom ML services (NumPy) │
│ • Pydantic validation        │
└──────────────────────────────┘
```

---

## Frontend Architecture

### Component Hierarchy

```
App.jsx
├── ErrorBoundary
└── Routes
    ├── Home
    ├── /regression → RegressionPage
    ├── /knn → KNNPage
    ├── /decision-tree → TreePage
    └── /genetic-algorithm → GAPage

Algorithm Page Structure:
├── PageShell
├── Sidebar (parameter controls)
├── Main content (visualization)
├── MetricsPanel (statistics)
└── TheoryDrawer (equations)
```

### State Management

Each algorithm has a Zustand store containing:
- Task mode (classifier/regressor)
- Hyperparameters
- Dataset selection
- Compare mode flag
- Uploaded data (if applicable)

Global UI store manages theory drawer state.

### Key Features

**Decision Tree Visualization:**
- Dynamic positioning based on tree depth (zoom: 0.5–1.2, Y-offset: 60–600px)
- High-contrast nodes: leaf (#0f172a), decision (#1e1b4b)
- Visible connectors (blue #3b82f6, 2.5px)
- Text truncation with hover tooltips

**Performance:**
- Memoized components prevent unnecessary re-renders
- Debounced API calls (300ms) batch parameter changes
- useMemo optimizes expensive calculations

---

## Backend Architecture

### API Endpoints

```
POST /api/regression              → Linear/Polynomial/Ridge/Lasso/ElasticNet
POST /api/knn                     → K-Nearest Neighbors
POST /api/decision_tree           → Decision Tree
POST /api/genetic_algorithm       → Genetic Algorithm
GET  /api/datasets                → List available datasets
POST /api/upload                  → Upload CSV
GET  /api/health                  → Health check
GET  /docs                        → OpenAPI documentation
```

### Request/Response Flow

```
User action → State update → Debounce (300ms) → API call
                                                    ↓
Input validation (Pydantic) → Service processing → Response (200/400/500)
                                                    ↓
Frontend state update → Memoized re-render → Visualization update
```

### Service Layer

Each algorithm service handles:
1. Input validation with helpful error messages
2. Data loading (built-in or uploaded CSV)
3. Model training/processing
4. Result calculation and JSON serialization
5. Error handling with appropriate HTTP codes

**From-Scratch Implementation:**
- Decision Tree: CART with Gini/Entropy, feature importance
- KNN: Euclidean/Manhattan distance, uniform/weighted voting
- Regression: Gradient descent, Ridge/Lasso regularization
- Genetic Algorithm: Real-coded GA with SBX crossover

All verified to use only NumPy—no sklearn models.

### Error Handling

```
Validation errors (400)
├── Pydantic type/value errors
├── Business logic validation
└── Data requirement checks

Server errors (500)
├── Unexpected exceptions
└── Logged with full traceback
```

---

## Data Flow Examples

### Example 1: Parameter Adjustment
```
User adjusts max_depth slider to 5
  ↓ State update (useTreeStore)
  ↓ Debounce waits 300ms for more changes
  ↓ POST /api/decision_tree { max_depth: 5, ... }
  ↓ Backend trains tree with new depth limit
  ↓ Response: { tree_json, accuracy, depth, ... }
  ↓ Frontend updates state
  ↓ Memoized TreeCard component checks for changes
  ↓ treeMetrics recalculated based on new depth
  ↓ Visualization re-renders with updated positioning
```

### Example 2: CSV Upload Error
```
User uploads CSV with only 1 numeric column
  ↓ Frontend converts CSV to array of objects
  ↓ POST /api/decision_tree { uploaded_data: [...] }
  ↓ Backend validates: numeric_cols.length < 2
  ↓ Raises ValueError("Need at least 2 numeric columns")
  ↓ Router catches → HTTPException(400, detail=...)
  ↓ Frontend receives error response
  ↓ Error notification displayed to user
```

---

## Deployment Architecture

### Development
```
localhost:3000 (React dev server)
    ↓ axios
localhost:8000 (FastAPI dev server)
    ↓
In-memory data (no database)
```

### Production
```
Vercel CDN
├─ Build: yarn build → static files
├─ Deploy: Auto on main branch push
└─ Env: REACT_APP_BACKEND_URL

Render Backend
├─ Build: pip install -r requirements.txt
├─ Runtime: Gunicorn + Uvicorn
├─ Auto-scaling: CPU/memory based
└─ Env: FRONTEND_URL (CORS configuration)
```

### CORS Configuration
Allowed origins:
- `http://localhost:3000` (development)
- `https://*.vercel.app` (any Vercel deployment)
- Environment-configurable for custom deployments

---

## Testing Strategy

### Test Categories
- **Unit Tests**: Service functions, tree operations, utility functions
- **Integration Tests**: API endpoints with full request/response cycles
- **Algorithm Verification**: Mathematical correctness validation
- **Validation Tests**: Pydantic schemas, input edge cases
- **From-Scratch Verification**: Grep tests confirm no sklearn usage

### Running Tests
```bash
pytest tests/ -v                 # All tests
pytest tests/test_decision_tree.py  # Specific test file
pytest --cov=app                 # Coverage report
```

### Coverage
- 122 total tests
- Covers all algorithms and endpoints
- Edge cases and boundary conditions
- Error handling paths

---

## Performance Characteristics

### Frontend
- Tree rendering: O(n) where n = number of nodes
- Component updates: Memoized to prevent unnecessary re-renders
- Debouncing: 300ms batches parameter changes
- Memory: Efficient with useMemo for calculations

### Backend
- Tree training: O(n * m * log(n)) where n=samples, m=features
- Feature importance: O(m)
- KNN prediction: O(n * m) for each query point
- Typical response: 5–50 KB

---

## Security Considerations

**Input Validation:**
- Pydantic automatic type checking
- Service-level business logic validation
- Safe data type conversions
- Error messages don't expose internals

**Error Handling:**
- 400 errors shown to user with details
- 500 errors logged with full traceback
- Consistent error response format

**CORS:**
- Whitelist specific origins
- No wildcards except `*.vercel.app`
- Environment-configurable

---

## Future Improvements

1. **Caching**: Memoize identical algorithm requests
2. **WebSockets**: Real-time parameter updates
3. **Export**: Save trees/plots as image/PDF
4. **Persistence**: Save and compare multiple models
5. **Advanced Visualization**: 3D tree rendering
6. **Scaling**: Support larger datasets with batching

---

## References

- Backend services: `backend/app/services/`
- Frontend state: `frontend/src/store/store.js`
- API client: `frontend/src/lib/api.js`
- Tests: `backend/tests/`
