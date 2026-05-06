# Architecture Documentation

## System Overview

**ML Visualizer** is a full-stack web application for interactive exploration and visualization of machine learning algorithms. The system enables real-time parameter tuning with instant visual feedback, educational algorithm understanding, and from-scratch implementations without relying on scikit-learn.

### Key Characteristics
- **Real-Time Interaction**: Parameter changes reflected in visualizations instantly
- **Educational Focus**: Theory drawer with mathematical equations for each algorithm
- **From-Scratch ML**: All algorithms implemented using NumPy only
- **Production Ready**: 122 comprehensive tests, global deployment, responsive design
- **Accessible**: WCAG AAA compliance with keyboard navigation and screen reader support

### System Properties
- Frontend-Backend separation with stateless API
- In-memory state management (no database)
- Responsive design: Mobile (320px) to 4K (2560px)
- Browser-based (no special client software needed)
- CORS-enabled for cross-origin requests

---

## High-Level Architecture

```
┌─────────────────────────────────────┐
│   Web Browser (React 19)            │
│  ┌──────────────────────────────┐   │
│  │ Algorithm Pages              │   │
│  │ - Regression                 │   │
│  │ - KNN                        │   │
│  │ - Decision Tree              │   │
│  │ - Genetic Algorithm          │   │
│  └──────────────────────────────┘   │
│              ↑ ↓                     │
│  ┌──────────────────────────────┐   │
│  │ Plotly / D3 Visualizations   │   │
│  └──────────────────────────────┘   │
│              ↑ ↓                     │
│  ┌──────────────────────────────┐   │
│  │ Zustand State Management     │   │
│  └──────────────────────────────┘   │
└────────────────┬────────────────────┘
                 │ HTTP API (REST)
      ┌──────────▼──────────┐
      │  FastAPI Backend    │
      ├─────────────────────┤
      │ API Routers         │
      │ - /api/regression   │
      │ - /api/knn          │
      │ - /api/decision_tree│
      │ - /api/genetic_algo │
      │ - /api/upload       │
      │ - /health           │
      ├─────────────────────┤
      │ ML Services (NumPy) │
      │ - Regression        │
      │ - KNN               │
      │ - Tree CART         │
      │ - GA (Real-coded)   │
      ├─────────────────────┤
      │ Dataset Management  │
      │ - Built-in datasets │
      │ - CSV uploads       │
      │ - Data normalization│
      └─────────────────────┘
```

---

## Frontend Architecture

### Directory Structure

```
frontend/src/
├── components/
│   ├── Home.jsx                    # Landing page
│   ├── ErrorBoundary.jsx           # Error handling wrapper
│   ├── regression/
│   │   ├── RegressionPage.jsx      # Main page
│   │   ├── RegressionControls.jsx  # Parameter controls
│   │   ├── RegressionChart.jsx     # Plotly visualization
│   │   └── costHistoryChart.jsx    # Cost tracking
│   ├── knn/
│   │   ├── KNNPage.jsx             # Main page
│   │   ├── KNNControls.jsx         # Parameter controls
│   │   ├── KNNPlot.jsx             # Decision boundary
│   │   └── KNNPlotTouchable.jsx    # Mobile interactions
│   ├── decision-tree/
│   │   ├── TreePage.jsx            # Main page
│   │   ├── TreeControls.jsx        # Parameter controls
│   │   ├── TreeVisualization.jsx   # D3 tree rendering
│   │   └── TreeNodeRenderer.jsx    # Custom node styling
│   ├── genetic/
│   │   ├── GAPage.jsx              # Main page
│   │   ├── GAControls.jsx          # Parameter controls
│   │   ├── GAChart.jsx             # Fitness evolution
│   │   └── GAScatterPlot.jsx       # Population visualization
│   ├── layout/
│   │   ├── Navbar.jsx              # Top navigation
│   │   ├── Sidebar.jsx             # Left sidebar with controls
│   │   ├── MetricsPanel.jsx        # Statistics display
│   │   └── PageShell.jsx           # Layout wrapper
│   ├── shared/
│   │   ├── PlotlyChart.jsx         # Plotly wrapper
│   │   ├── TheoryDrawer.jsx        # Equation reference
│   │   ├── SkeletonLoader.jsx      # Loading states
│   │   └── DatasetSelector.jsx     # Dataset management
│   └── ui/
│       ├── button.jsx              # Button component
│       ├── input.jsx               # Input component
│       ├── select.jsx              # Select dropdown
│       ├── slider.jsx              # Slider control
│       ├── checkbox.jsx            # Checkbox control
│       ├── switch.jsx              # Toggle switch
│       ├── skeleton.jsx            # Skeleton loading
│       └── sonner.js               # Toast notifications
├── store/
│   ├── store.js                    # UI store (theme, drawer)
│   ├── regressionStore.js          # Regression state
│   ├── knnStore.js                 # KNN state
│   ├── treeStore.js                # Decision tree state
│   └── gaStore.js                  # Genetic algorithm state
├── lib/
│   ├── api.js                      # Axios API client
│   └── utils.js                    # Helper functions
├── hooks/
│   ├── useRegressionStore.js       # Regression store hook
│   ├── useKNNStore.js              # KNN store hook
│   ├── useTreeStore.js             # Tree store hook
│   └── useGAStore.js               # GA store hook
├── App.js                          # Main app component
├── App.css                         # Global and component styles
├── index.css                       # Tailwind base styles
└── index.js                        # React entry point
```

### Component Hierarchy

```
App
├── ErrorBoundary
│   └── BrowserRouter
│       ├── Routes
│       │   ├── Home
│       │   ├── RegressionPage
│       │   │   ├── PageShell
│       │   │   ├── Navbar
│       │   │   ├── TheoryDrawer
│       │   │   ├── Sidebar (RegressionControls)
│       │   │   ├── RegressionChart
│       │   │   ├── costHistoryChart
│       │   │   └── MetricsPanel
│       │   ├── KNNPage (similar structure)
│       │   ├── TreePage (similar structure)
│       │   └── GAPage (similar structure)
```

### State Management with Zustand

#### Global UI Store (`store.js`)

```javascript
// UI state - theme, drawers, first-visit hints
{
  theoryOpen: boolean,              // Theory drawer visibility
  setTheoryOpen: (v) => void,
  hasSeenTheoryHint: boolean,       // First-visit hint tracking
  setHasSeenTheoryHint: (v) => void
}
```

Persistence enabled: Saved to localStorage as `ml-visualizer-ui`

#### Algorithm-Specific Stores

Each algorithm (regression, KNN, tree, GA) has its own Zustand store:

```javascript
// Example: Regression Store (regressionStore.js)
{
  // Task & Dataset
  task: 'regression' | 'classification',
  dataset: string,
  uploadedData: Array | null,
  
  // Model Parameters
  algo: string,                     // Linear, Polynomial, Ridge, etc.
  learningRate: number,
  maxIterations: number,
  regStrength: number,
  polyDegree: number,
  
  // Control Flags
  compareMode: boolean,
  
  // Setters
  setTask: (t) => void,
  setDataset: (d) => void,
  setUploadedData: (d) => void,
  setAlgo: (a) => void,
  setLearningRate: (lr) => void,
  // ... more setters
}
```

Persistence enabled: Saved to localStorage with prefix `regression-store-`

### Data Flow: Parameter Change to Visualization

```
1. User Interaction
   └─> Slider/Input component onChange
       └─> setState in Zustand store
           └─> Component re-renders with new props

2. API Call (Debounced 300ms)
   └─> useEffect detects store changes
       └─> Debounce prevents excessive API calls
           └─> POST /api/{algorithm}
               └─> Pydantic validates request

3. Backend Processing
   └─> Service load dataset
       └─> Service process with new parameters
           └─> Service generate visualization data
               └─> Return response (JSON)

4. Frontend Update
   └─> API response received
       └─> Zustand store updates with results
           └─> Components with useMemo detect changes
               └─> Chart re-renders
                   └─> Metrics panel updates
```

### Key Hooks & Utilities

#### Custom Hooks
- `useDebounce(value, delay)`: Debounces API calls
- `useMemo`: Optimizes expensive calculations
- `useCallback`: Memoizes event handlers
- `useLocalStorage`: Persists UI preferences

#### Utility Functions
- `normalizeData()`: Standardizes numeric features
- `calculateMetrics()`: Computes accuracy, MSE, etc.
- `formatNumber()`: Number formatting with precision
- `parseCSV()`: CSV parsing and validation

---

## Backend Architecture

### FastAPI Application Structure

```
backend/
├── app/
│   ├── main.py                  # FastAPI app initialization
│   ├── config.py                # Environment configuration
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── regression.py        # POST /api/regression
│   │   ├── knn.py               # POST /api/knn
│   │   ├── decision_tree.py     # POST /api/decision_tree
│   │   ├── genetic_algorithm.py # POST /api/genetic_algorithm
│   │   └── utils.py             # Shared router utilities
│   ├── services/
│   │   ├── __init__.py
│   │   ├── regression_service.py    # Regression implementation
│   │   ├── knn_service.py           # KNN implementation
│   │   ├── tree_service.py          # Decision tree implementation
│   │   ├── ga_service.py            # Genetic algorithm implementation
│   │   ├── dataset_service.py       # Dataset loading & preprocessing
│   │   ├── tree_utils.py            # Tree-specific utilities
│   │   └── regression_utils.py      # Regression-specific utilities
│   ├── models/
│   │   ├── __init__.py
│   │   ├── request_models.py    # Pydantic request schemas
│   │   └── response_models.py   # Pydantic response schemas
│   └── utils/
│       ├── __init__.py
│       ├── errors.py            # Custom exceptions
│       ├── validators.py        # Input validators
│       └── formatters.py        # Response formatters
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # pytest fixtures
│   ├── test_regression.py       # Regression tests (25 tests)
│   ├── test_knn.py              # KNN tests (20 tests)
│   ├── test_decision_tree.py    # Tree tests (30 tests)
│   ├── test_genetic_algorithm.py# GA tests (25 tests)
│   ├── test_dataset_service.py  # Dataset tests (12 tests)
│   ├── test_sklearn_free.py     # Verify no sklearn
│   └── test_integration.py      # End-to-end tests (10 tests)
├── requirements.txt             # Python dependencies
└── server.py                    # Development server entry
```

### API Endpoints

#### 1. Regression
```
POST /api/regression
Request:
{
  "task": "regression" | "classification",
  "dataset": "linear" | "sine" | "quadratic" | custom,
  "algo": "linear" | "polynomial" | "ridge" | "lasso" | "elasticnet",
  "learning_rate": 0.001 - 1.0,
  "max_iterations": 1 - 10000,
  "poly_degree": 1 - 5,
  "reg_strength": 0.001 - 100,
  "train_test_ratio": 0.5 - 0.9,
  "uploaded_data": null | Array<{x, y}>,
  "compare_mode": false | true
}

Response:
{
  "coefficients": [float, ...],
  "intercept": float,
  "cost_history": [float, ...],
  "predictions_train": [float, ...],
  "predictions_test": [float, ...],
  "train_r2": float,
  "test_r2": float,
  "training_samples": int,
  "test_samples": int,
  "stopped_at_epoch": int,
  "mse_train": float,
  "mse_test": float
}
```

#### 2. K-Nearest Neighbors
```
POST /api/knn
Request:
{
  "task": "regression" | "classification",
  "k": 1 - 50,
  "metric": "euclidean" | "manhattan",
  "weights": "uniform" | "distance",
  "dataset": string,
  "test_point": [float, float] | null,
  "uploaded_data": null | Array
}

Response:
{
  "boundary_points": [[x, y, class], ...],
  "accuracies": {"train": float, "test": float},
  "test_prediction": float | int | null,
  "distances": [float, ...] | null,
  "neighbors_indices": [int, ...] | null,
  "training_samples": int,
  "test_samples": int
}
```

#### 3. Decision Tree
```
POST /api/decision_tree
Request:
{
  "task": "regression" | "classification",
  "max_depth": 1 - 20,
  "criterion": "gini" | "entropy" | "mse",
  "min_samples_split": 2 - 50,
  "dataset": string,
  "compare_mode": false | true,
  "compare_max_depth": 1 - 20 | null,
  "uploaded_data": null | Array
}

Response:
{
  "tree_json": {...},      # D3-compatible tree structure
  "accuracy": float,
  "depth": int,
  "n_leaves": int,
  "feature_importances": {"feature_0": float, ...},
  "training_samples": int,
  "test_samples": int,
  "test_accuracy": float
}
```

#### 4. Genetic Algorithm
```
POST /api/genetic_algorithm
Request:
{
  "function": "sphere" | "rastrigin" | "rosenbrock",
  "pop_size": 20 - 200,
  "generations": 10 - 1000,
  "mutation_rate": 0.01 - 0.5,
  "crossover_rate": 0.5 - 1.0,
  "eta_m": 5 - 50,
  "eta_c": 5 - 50,
  "dimension": 2 - 10
}

Response:
{
  "best_fitness": float,
  "best_solution": [float, ...],
  "fitness_history": [float, ...],
  "population_final": [[float, ...], ...],
  "generation": int,
  "function_evals": int,
  "convergence_generation": int
}
```

#### 5. Utilities
```
GET /api/health
Response: {"status": "ok", "timestamp": "2026-05-06T..."}

GET /api/datasets
Response: {
  "regression": ["linear", "sine", "quadratic"],
  "classification": ["iris", "breast_cancer", "moons", "circles", "blobs"]
}

POST /api/upload
Request: multipart/form-data with CSV file
Response: {"samples": int, "features": int, "data": [[...], ...]}
```

### ML Service Implementations

#### Regression Service (`regression_service.py`)

Implements gradient descent from scratch:
- **Linear Regression**: `y = w*x + b`
- **Polynomial Regression**: Adds polynomial features
- **Ridge Regression**: L2 regularization `loss + λ*||w||²`
- **Lasso Regression**: L1 regularization `loss + λ*||w||`
- **Elastic Net**: Combined L1 + L2 regularization

Key algorithms:
```python
def gradient_descent(X, y, learning_rate, iterations, reg_type, reg_strength):
    weights = np.zeros(X.shape[1])
    for epoch in range(iterations):
        # Compute predictions
        y_pred = np.dot(X, weights)
        
        # Compute loss
        mse = np.mean((y_pred - y) ** 2)
        
        # Add regularization
        reg_term = regularization_loss(weights, reg_type, reg_strength)
        loss = mse + reg_term
        
        # Compute gradients
        gradients = (2 / len(y)) * np.dot(X.T, (y_pred - y))
        
        # Add regularization gradient
        reg_gradient = reg_gradient_term(weights, reg_type, reg_strength)
        gradients += reg_gradient
        
        # Update weights
        weights -= learning_rate * gradients
        
        # Store metrics
        cost_history.append(loss)
    
    return weights, cost_history
```

#### KNN Service (`knn_service.py`)

Implements K-Nearest Neighbors classifier/regressor:
- **Distance Metrics**: Euclidean, Manhattan
- **Voting**: Uniform weights, distance weights
- **Decision Boundary**: Grid-based classification

Key algorithm:
```python
def knn_predict(X_train, y_train, X_test, k, metric='euclidean', weights='uniform'):
    predictions = []
    
    for x_point in X_test:
        # Compute distances
        if metric == 'euclidean':
            distances = np.sqrt(np.sum((X_train - x_point) ** 2, axis=1))
        else:  # manhattan
            distances = np.sum(np.abs(X_train - x_point), axis=1)
        
        # Get k nearest indices
        k_nearest_indices = np.argsort(distances)[:k]
        k_nearest_labels = y_train[k_nearest_indices]
        k_nearest_distances = distances[k_nearest_indices]
        
        # Voting with weights
        if weights == 'uniform':
            prediction = mode(k_nearest_labels)
        else:  # distance weights
            weights_array = 1 / (k_nearest_distances + 1e-10)
            prediction = weighted_mode(k_nearest_labels, weights_array)
        
        predictions.append(prediction)
    
    return np.array(predictions)
```

#### Tree Service (`tree_service.py`)

Implements CART (Classification and Regression Trees):
- **Splitting Criteria**: Gini index, Entropy (classification); MSE (regression)
- **Pruning**: Max depth, min samples split
- **Feature Importance**: Calculated based on information gain

Key algorithm:
```python
def build_decision_tree(X, y, depth, max_depth, criterion):
    # Check stopping criteria
    if depth >= max_depth or len(np.unique(y)) == 1:
        return Leaf(value=mode(y))
    
    # Find best split
    best_split = find_best_split(X, y, criterion)
    if best_split is None:
        return Leaf(value=mode(y))
    
    # Recursively build left and right subtrees
    feature_idx, threshold = best_split
    left_mask = X[:, feature_idx] <= threshold
    right_mask = ~left_mask
    
    left_tree = build_decision_tree(
        X[left_mask], y[left_mask], 
        depth+1, max_depth, criterion
    )
    right_tree = build_decision_tree(
        X[right_mask], y[right_mask], 
        depth+1, max_depth, criterion
    )
    
    return Node(
        feature=feature_idx,
        threshold=threshold,
        left=left_tree,
        right=right_tree
    )
```

#### Genetic Algorithm Service (`ga_service.py`)

Implements real-coded genetic algorithm with SBX crossover:
- **Operators**: Real-coded crossover (SBX), polynomial mutation
- **Selection**: Tournament selection
- **Benchmark Functions**: Sphere, Rastrigin, Rosenbrock

Key algorithm:
```python
def genetic_algorithm(pop_size, generations, mutation_rate, crossover_rate, eta_m, eta_c):
    # Initialize population
    population = np.random.uniform(-5, 5, (pop_size, dimension))
    
    for gen in range(generations):
        # Evaluate fitness
        fitness = np.array([evaluate_function(ind) for ind in population])
        
        # Selection
        selected = tournament_selection(population, fitness, pop_size)
        
        # Crossover (SBX)
        offspring = []
        for i in range(0, pop_size, 2):
            child1, child2 = sbx_crossover(
                selected[i], selected[i+1], eta_c, crossover_rate
            )
            offspring.extend([child1, child2])
        
        # Mutation (Polynomial)
        for i in range(len(offspring)):
            offspring[i] = polynomial_mutation(
                offspring[i], mutation_rate, eta_m
            )
        
        # Environmental selection
        population = selection_best(
            population, offspring, fitness, pop_size
        )
        
        fitness_history.append(np.min(fitness))
    
    return best_solution, fitness_history
```

#### Dataset Service (`dataset_service.py`)

Loads and preprocesses datasets:
- **Built-in Datasets**: Linear, Sine, Iris, Cancer, etc.
- **CSV Upload**: Parsing, validation, normalization
- **Preprocessing**: Feature normalization, target encoding

### Error Handling

**Validation Errors (HTTP 400)**
```python
# Request validation happens automatically with Pydantic
# Invalid k value raises ValidationError → 400 response

# Business logic validation
if k > len(X_train):
    raise HTTPException(
        status_code=400,
        detail=f"k ({k}) cannot exceed training samples ({len(X_train)})"
    )
```

**Server Errors (HTTP 500)**
```python
try:
    # Process request
except Exception as e:
    logger.exception(f"Unexpected error: {str(e)}")
    raise HTTPException(
        status_code=500,
        detail="An unexpected error occurred. Please try again."
    )
```

---

## Data Flow Examples

### Example 1: Decision Tree Parameter Adjustment

```
1. Frontend State Update
   User adjusts max_depth slider → 7
   │
   └─> treeStore.setMaxDepth(7)
       └─> Zustand state changes
           └─> useEffect detects change
               └─> Debounce (300ms) waits for more changes

2. API Request
   After 300ms with no new changes:
   │
   └─> POST /api/decision_tree
       {
         "max_depth": 7,
         "task": "classification",
         "dataset": "iris",
         "criterion": "gini",
         ...
       }

3. Backend Processing
   │
   └─> Pydantic validates request
       └─> tree_service.build_tree()
           ├─> Load iris dataset
           ├─> Build tree with max_depth=7
           ├─> Calculate feature importances
           ├─> Generate tree JSON for D3
           └─> Calculate metrics (accuracy, depth, n_leaves)

4. Response Generation
   │
   └─> API returns:
       {
         "tree_json": {...},
         "accuracy": 0.96,
         "depth": 6,
         "n_leaves": 15,
         "feature_importances": {...}
       }

5. Frontend Update
   │
   └─> API response received
       └─> Zustand updates store with results
           └─> TreeVisualization component updates
               └─> MetricsPanel updates
                   └─> User sees new tree structure
```

### Example 2: CSV Upload Error Handling

```
1. User Selects File
   └─> CSV with only 1 numeric column selected
       └─> File uploaded via POST /api/upload

2. Backend Validation
   └─> CSV parsed successfully
       └─> Numeric columns checked
           └─> Only 1 numeric column found
               └─> ValidationError raised
                   └─> HTTPException(400) returned with detail

3. Frontend Error Display
   └─> API returns 400 with error message
       └─> Error notification displayed
           └─> User sees "Need at least 2 numeric columns"

4. User Corrected
   └─> User uploads correct CSV
       └─> Success: CSV processed and available
```

---

## Deployment Architecture

### Development Environment

```
localhost:3000 ←→ localhost:8000
├─ React dev server          ├─ FastAPI dev server
│  - Hot reload             │  - Auto reload
│  - Source maps            │  - OpenAPI docs
│  - DevTools                │  - debug=True
└─ .env.local               └─ .env (optional)
   REACT_APP_BACKEND_URL=    
   http://localhost:8000
```

### Production Environment (Vercel + Render)

```
User Browser
    │
    ├─→ Vercel CDN (Global Edge Network)
    │       │
    │       ├─ Static assets cached globally
    │       ├─ JavaScript bundles minified
    │       ├─ CSS preprocessed
    │       └─ Automatic GZIP compression
    │
    └─→ Render Backend (North America)
            │
            ├─ Gunicorn WSGI server
            ├─ Uvicorn ASGI worker
            ├─ Auto-scaling (CPU/Memory)
            └─ Health checks every 30s
```

### Environment Configuration

**Frontend Environment Variables**
```
REACT_APP_BACKEND_URL = https://emergent-av9b.onrender.com
REACT_APP_ENVIRONMENT = production
```

**Backend Environment Variables**
```
FRONTEND_URL = https://emergent-six-zeta.vercel.app
PORT = 8000 (managed by Render)
ENVIRONMENT = production
DEBUG = False
```

### CORS Configuration

```python
# Allowed origins for frontend requests
allowed_origins = [
    "http://localhost:3000",           # Development
    "https://emergent-six-zeta.vercel.app",  # Production
    "https://*.vercel.app",            # All Vercel previews
    # Environment-configurable for custom domains
]
```

---

## Performance Optimization

### Frontend Optimizations

**Memoization Strategy**
```javascript
// Prevent unnecessary re-renders
const MemoizedChart = React.memo(Chart, (prev, next) => {
  // Only re-render if these props change
  return prev.data === next.data && prev.layout === next.layout;
});
```

**Debouncing API Calls**
```javascript
// Batch parameter changes within 300ms
const debouncedFetch = useCallback(
  debounce((params) => {
    api.post('/api/decision_tree', params);
  }, 300),
  []
);
```

**Code Splitting**
```javascript
// Load algorithm pages only when needed
const RegressionPage = lazy(() => import('./components/regression/RegressionPage'));
```

### Backend Optimizations

**Algorithm Efficiency**
- Decision Tree: O(n * m * log(n)) training time
- KNN: O(n * m) prediction time (no training)
- Regression: O(m³) for coefficient computation
- GA: O(pop_size * generations * dimension)

**Response Optimization**
- Typical JSON response: 5-50 KB
- Gzipped response: 2-15 KB
- Response time: 50ms-2s depending on dataset

---

## Testing Strategy

### Test Coverage (122 tests)

**Unit Tests**
- Service functions: Gradient descent, splitting criteria
- Utility functions: Distance metrics, feature scaling
- Data processing: CSV parsing, normalization

**Integration Tests**
- Complete API request/response cycles
- State management integration
- Database (CSV) interactions

**Algorithm Tests**
- Mathematical correctness verification
- Boundary condition handling
- Edge case validation

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_decision_tree.py -v

# With coverage
pytest --cov=app --cov-report=html
```

### From-Scratch Verification

```bash
# Verify no sklearn usage
grep -r "from sklearn" backend/app/services/
# Should return no results - all implemented from scratch
```

---

## Security Considerations

### Input Validation

**Type Checking**
- Pydantic automatic validation on all inputs
- Type hints on all function parameters
- Safe conversions for numeric types

**Business Logic Validation**
```python
# Example: KNN k value validation
if not 1 <= k <= len(X_train):
    raise ValueError(f"k must be between 1 and {len(X_train)}")
```

**Data Sanitization**
- No dynamic SQL (no database)
- CSV validation before processing
- Safe numeric conversions

### Error Handling

**User-Facing Errors**
- 400 errors include helpful details
- No internal exception messages exposed
- Actionable guidance provided

**Server Errors**
- 500 errors logged with full traceback
- Generic message shown to user
- Traceback never exposed to client

### CORS Security

- Specific origin whitelist (no wildcards)
- Credentials support only for same-origin
- Preflight requests properly handled

---

## Monitoring & Logging

### Health Checks

**Frontend**
- TypeScript compilation errors
- JavaScript runtime errors
- Component rendering failures

**Backend**
```python
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
```

### Logging

**Backend Logging**
```python
import logging

logger = logging.getLogger(__name__)
logger.info("Request received: /api/decision_tree")
logger.error("Error processing tree", exc_info=True)
```

---

## Known Limitations

1. **In-Memory Only**: No persistence between server restarts
2. **Single Model**: Can't save/load multiple models
3. **Tree Visualization**: Limited to ~1000 nodes for performance
4. **No Real-Time**: WebSocket updates not implemented
5. **Export**: Can't save visualizations as images

---

## Future Improvements

1. **Model Persistence**: Save and load trained models
2. **Database Integration**: Store user models and preferences
3. **WebSocket Real-Time**: Live parameter updates
4. **Export Functionality**: Save visualizations as SVG/PDF
5. **Advanced Metrics**: More detailed statistics and comparisons
6. **Distributed Training**: GPU acceleration for large datasets
7. **Mobile App**: Native mobile applications
8. **Collaborative**: Real-time collaboration features

---

## References & Resources

- **Frontend Code**: `frontend/src/`
- **Backend Code**: `backend/app/`
- **Tests**: `backend/tests/`
- **README**: `README.md`
- **Deployment**: Vercel (frontend), Render (backend)

---

## Contributors

| Contributor | Roll Number | Email |
|--------|------|-------|
| Aryan Chawla | 23124019 | aryanc.it.23@nitj.ac.in |
| Chirag Bishnoi | 23124027 | chiragk.it.23@nitj.ac.in |
| Chaudhari Arpit Kumar | 23124026 | chaudharia.it.23@nitj.ac.in |
| Dhawal Palaiya | 23124030 | dhawalp.it.23@nitj.ac.in |

---
