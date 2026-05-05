# ML Visualizer - Architecture Documentation

This document provides a comprehensive overview of the ML Visualizer architecture, design decisions, and component structure.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                         │
│  ├─ Components: Algorithm-specific pages                       │
│  ├─ State: Zustand store (per-algorithm state)                 │
│  ├─ Hooks: Custom hooks for debouncing, data management        │
│  ├─ Visualization: Plotly.js + react-d3-tree                  │
│  └─ Error Handling: React Error Boundary                       │
└─────────────────────────────────────────────────────────────────┘
                            ↓ HTTP API ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI Python)                      │
│  ├─ Routers: 6 algorithm endpoint groups                       │
│  ├─ Services: Custom ML implementations (no sklearn models)    │
│  ├─ Models: Pydantic schemas for validation                    │
│  ├─ Utils: Tree parsing, data loading                          │
│  └─ Logging: Structured logging with error tracking            │
└─────────────────────────────────────────────────────────────────┘
                            ↓ CORS ↓
                    (Vercel ↔ Render)
```

---

## Frontend Architecture

### Component Hierarchy

```
App.jsx (Root with Error Boundary)
├── ErrorBoundary (Error handling)
└── BrowserRouter
    └── Routes
        ├── Home → Home.jsx
        ├── /regression → RegressionPage.jsx
        ├── /knn → KNNPage.jsx
        ├── /decision-tree → TreePage.jsx
        └── /genetic-algorithm → GAPage.jsx

Each Algorithm Page Structure:
├── PageShell (Layout wrapper)
├── Sidebar (Parameter controls)
│   ├── Tabs (Task mode: Classifier/Regressor)
│   ├── Sliders (Hyperparameters)
│   ├── Selects (Dataset/Criterion)
│   └── Switches (Compare modes)
├── Main Content Area
│   ├── ChartCard/TreeCard (Visualization)
│   └── MetricsPanel (Key statistics)
└── TheoryDrawer (KaTeX equations)
```

### State Management (Zustand)

Each algorithm has a dedicated store with its state:

```javascript
// Decision Tree Store
useTreeStore: {
  task: "classifier" | "regressor",
  criterion: "gini" | "entropy",
  max_depth: number | null,
  min_samples_split: number,
  min_samples_leaf: number,
  dataset: string,
  uploadedDataset: object | null,
  compareMode: boolean,
  set: (patch) => void
}

// Global UI Store
useUIStore: {
  theoryOpen: boolean,
  setTheoryOpen: (value) => void
}
```

### Decision Tree Visualization (Key Improvement)

**Problem Solved:**
- Original: Poor node contrast, invisible connectors, fixed zoom/positioning
- Solution: Dynamic styling, responsive layout, improved colors

**Implementation:**
```javascript
// File: TreePage.jsx

// 1. Dynamic tree metrics based on depth
const treeMetrics = useMemo(() => {
  const depth = resp.depth || 3;
  const zoom = Math.max(0.5, 1.2 - (depth * 0.08));
  const yOffset = Math.max(60, 40 + depth * 15);
  return { zoom, translate: { x: 420, y: yOffset } };
}, [resp?.depth]);

// 2. Improved node rendering with better colors
const nodeConfig = isLeaf
  ? { fill: "#0f172a", stroke: "#0ea5e9", textColor: "#06b6d4" }
  : { fill: "#1e1b4b", stroke: "#a78bfa", textColor: "#e9d5ff" };

// 3. Connector line visibility (critical fix)
styles={{ links: { stroke: "#3b82f6", strokeWidth: 2.5 } }}

// 4. Text truncation and tooltips
const displayName = truncateText(nodeDatum.name, 28);
<title>{fullName}</title>  // Tooltip on hover
```

### Performance Optimizations

```javascript
// 1. Memoized expensive components
const FeatureImportanceChart = React.memo(function(...) { ... });
export default React.memo(TreePage);

// 2. Memoized calculations
const sorted = useMemo(() => 
  Object.entries(importances)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8),
  [importances]
);

// 3. Debounced API requests (300ms)
const debouncedReq = useDebounce({...params}, 300);
```

---

## Backend Architecture

### API Endpoints Structure

```
/api
├── /regression (POST)              → Regression algorithms
├── /knn (POST)                     → K-Nearest Neighbors
├── /decision_tree (POST)           → Decision Trees
├── /genetic_algorithm (POST)       → Genetic Algorithms
├── /datasets (GET)                 → Available datasets
├── /upload (POST)                  → CSV file upload
├── /health (GET)                   → Health check
└── /docs (GET)                     → OpenAPI documentation
```

### Request/Response Flow

```
User Action (e.g., adjust slider)
    ↓
Debounce (300ms)
    ↓
API Client (lib/api.js)
    ↓ JSON POST request
Backend Router (decision_tree.py)
    ↓ Error handling with try/catch
Service Layer (tree_service.py)
    ↓ Input validation
    ↓ Data loading/preprocessing
    ↓ Model training
    ↓ Result calculation
    ↓ JSON serialization
Backend Response (200 or 400/500)
    ↓ Frontend receives JSON
    ↓ Update state
    ↓ Memoized component re-render
    ↓ Visualization updated
```

### Error Handling Strategy

```python
# Backend: Multi-layer validation

@router.post("/decision_tree")
async def decision_tree_endpoint(request: DecisionTreeRequest):
    try:
        # 1. Pydantic auto-validation (happens first)
        # 2. Service-level validation
        run_decision_tree(
            task=request.task,           # Validated by Pydantic
            criterion=request.criterion,
            ...
        )
    except ValueError as e:
        # Input validation errors → 400
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Unexpected errors → 500
        logger.error(f"Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal error")
```

### Decision Tree Service (From-Scratch Implementation)

```python
# File: tree_service.py

def run_decision_tree(
    task: Literal["classifier", "regressor"],
    criterion: Literal["gini", "entropy"],
    max_depth: Optional[int],
    min_samples_split: int,
    min_samples_leaf: int,
    dataset: str,
    uploaded_data: Optional[List[dict]] = None,
) -> dict:
    """
    Key features:
    1. Comprehensive validation with helpful error messages
    2. Structured logging for debugging
    3. Support for built-in datasets AND CSV uploads
    4. Custom tree implementation (NO sklearn trees used)
    5. Tree-to-JSON conversion for visualization
    6. Feature importance calculation
    7. Depth/leaf counting utilities
    """
    # 1. Input validation
    if task not in ("classifier", "regressor"):
        raise ValueError(f"Invalid task: {task}")
    if task == "regressor" and criterion == "entropy":
        raise ValueError("entropy only for classifier")
    
    # 2. Data handling
    if uploaded_data:
        df = pd.DataFrame(uploaded_data)
        df = df.fillna(df.mean())  # Handle NaN
        X, y, feature_names = extract_numeric_cols(df)
    else:
        X, y, feature_names = load_dataset(dataset)
    
    # 3. Model training
    model = CustomDecisionTreeClassifier(...) or CustomDecisionTreeRegressor(...)
    model.fit(X_train, y_train)
    
    # 4. Results
    return {
        "tree_json": model.to_json(feature_names),
        "accuracy": model.score(X_test, y_test),
        "depth": model.get_depth(),
        "n_leaves": model.get_n_leaves(),
        "feature_importances": {...}
    }
```

### Logging Architecture

```python
# Configured in app/main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Each module:
logger = logging.getLogger(__name__)

# Usage:
logger.info(f"Processing dataset: {dataset}")
logger.warning("Small dataset may be unreliable")
logger.error("Unexpected error:", exc_info=True)
```

---

## Data Flow Examples

### Example 1: Adjusting Max Depth

```
User moves max_depth slider to 5
    ↓
State update: useTreeStore.set({ max_depth: 5 })
    ↓
Component re-render triggered
    ↓
useDebounce delays 300ms (waiting for more changes)
    ↓
300ms passes with no new input
    ↓
useEffect runs with new debouncedReq
    ↓
API call: POST /api/decision_tree { max_depth: 5, ... }
    ↓
Backend runs CustomDecisionTreeClassifier with max_depth=5
    ↓
Response: { tree_json, accuracy, depth, n_leaves, feature_importances }
    ↓
setRespA(data) updates state
    ↓
TreeCard memoized component checks if resp changed
    ↓
treeMetrics re-calculated based on new depth
    ↓
Tree component re-renders with new translate/zoom
    ↓
Visualization updates with improved positioning
```

### Example 2: Error Handling Flow

```
User uploads invalid CSV (only 1 numeric column)
    ↓
Frontend converts CSV to array of objects
    ↓
API call: POST /api/decision_tree { uploaded_data: [...] }
    ↓
Backend tree_service processes data:
    - load_dataset() returns data
    - Validate: numeric_cols = df.select_dtypes(include="number")
    - Check: len(numeric_cols) < 2
    - Raise: ValueError("Uploaded CSV must have at least 2 numeric columns")
    ↓
Router catches ValueError
    ↓
Raise HTTPException(status_code=400, detail="Invalid input: ...")
    ↓
Frontend receives error response (400)
    ↓
Error notification displayed to user
```

---

## Testing Architecture

### Test Layers

```
1. Unit Tests (app/services/custom_tree.py)
   ├── Tree structure validation
   ├── Depth/leaf counting
   └── Feature importance calculation

2. Service Tests (app/services/tree_service.py)
   ├── Input validation
   ├── Error handling
   ├── CSV processing
   ├── Different datasets
   └── Classifier vs Regressor

3. Endpoint Tests (routers/decision_tree.py)
   ├── Valid requests → 200
   ├── Invalid inputs → 400
   ├── Error messages
   └── Response structure

4. Integration Tests
   ├── End-to-end workflows
   ├── State management
   └── Visualization rendering

5. E2E Tests (frontend)
   ├── User interactions
   ├── Tree visualization
   └── Error boundaries
```

### Test Statistics

```
Total Tests: 107+
├── Decision Tree: 20+
├── KNN: 15+
├── Regression: 15+
├── Genetic Algorithm: 15+
├── API Endpoints: 12+
├── Validation: 10+
└── Server/Integration: 5+
```

---

## Deployment Architecture

### Development Environment

```
localhost:3000 (Frontend - React Dev Server)
    ↓ axios
localhost:8000 (Backend - FastAPI Dev Server)
    ↓
In-memory data (no database)
```

### Production Environment (Vercel + Render)

```
Frontend Deployment (Vercel CDN)
├─ Build: yarn build → static files
├─ Deployment: Auto on main branch push
├─ Environment: REACT_APP_BACKEND_URL=https://api.render.com
└─ Performance: Global edge caching

Backend Deployment (Render)
├─ Build: pip install -r requirements.txt
├─ Runtime: Gunicorn + Uvicorn workers
├─ Environment: FRONTEND_URL=https://frontend.vercel.app
└─ Scaling: Auto-scaling based on CPU/memory
```

### CORS Configuration

```python
# Allowed origins:
- http://localhost:3000        # Local development
- http://localhost:3001        # Alternative local
- https://*.vercel.app         # Any Vercel deployment
- https://emergent-one.vercel.app  # Production
- Custom FRONTEND_URL env var  # Flexible deployment
```

---

## Security Considerations

### Input Validation

```python
# All user inputs validated at multiple layers:
1. Pydantic schemas (automatic type checking)
2. Service-level validation (business logic)
3. Data preprocessing (safe conversions)
4. Error messages (don't expose internals)
```

### Error Handling

```python
# Errors categorized:
- 400 Bad Request: User input errors (shown to user)
- 500 Internal Error: Server errors (generic message to user, detailed logs for dev)
```

### CORS Protection

```python
# Strict CORS configuration:
- Whitelist specific origins
- No wildcard origins except for vercel.app
- Environment-configurable for deployments
```

---

## Performance Characteristics

### Frontend

- **Tree Rendering**: O(n) where n = number of nodes
- **Component Re-renders**: Memoized to prevent unnecessary updates
- **API Debouncing**: 300ms to batch requests
- **Memory**: Efficient with useMemo for expensive calculations

### Backend

- **Algorithm Complexity**:
  - Tree Training: O(n * m * log(n)) where n=samples, m=features
  - Feature Importance: O(m)
  - Tree Serialization: O(nodes)

### Data Transfer

- **Typical Response Size**: 5-50 KB (tree JSON + metrics)
- **Compression**: Enabled by default in production

---

## Future Improvements

1. **Caching**: Memoize identical tree requests
2. **Real-time Updates**: WebSocket for live parameter tuning
3. **Export Features**: Download tree as image/PDF
4. **More Datasets**: User dataset management
5. **Model Comparison**: Save and compare multiple models
6. **Advanced Visualization**: 3D trees for deeper exploration
7. **Model Persistence**: Save/load trained models
8. **Distributed Training**: Scale to larger datasets

---

## References

- [Decision Tree Implementation](../backend/app/services/custom_tree.py)
- [Tree Service](../backend/app/services/tree_service.py)
- [Frontend State](../frontend/src/store/store.js)
- [API Client](../frontend/src/lib/api.js)
- [TreePage Component](../frontend/src/components/decision-tree/TreePage.jsx)
