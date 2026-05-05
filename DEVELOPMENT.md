# ML Visualizer - Setup & Development Guide

This document provides comprehensive setup, development, and deployment instructions for the ML Visualizer project.

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Environment Configuration](#environment-configuration)
3. [Running the Application](#running-the-application)
4. [Testing](#testing)
5. [Deployment](#deployment)
6. [Troubleshooting](#troubleshooting)
7. [Architecture Overview](#architecture-overview)

---

## Local Development Setup

### Prerequisites

- **Python 3.11+** - Backend runtime
- **Node.js 18+** - Frontend runtime
- **Yarn 1.22+** - Frontend package manager
- **Git** - Version control

### Quick Start

#### 1. Clone Repository

```bash
git clone <repository-url>
cd emergent
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start development server
python server.py
```

Backend will be available at `http://localhost:8000`

#### 3. Frontend Setup (in a new terminal)

```bash
cd frontend

# Install dependencies
yarn install

# Create environment file
echo "REACT_APP_BACKEND_URL=http://localhost:8000" > .env.local

# Start development server
yarn start
```

Frontend will be available at `http://localhost:3000`

---

## Environment Configuration

### Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# FastAPI Configuration
PORT=8000                              # Server port (default: 8000)
FRONTEND_URL=http://localhost:3000     # Frontend URL for CORS

# Logging (optional)
LOG_LEVEL=INFO                         # Logging level (DEBUG/INFO/WARNING/ERROR)
```

### Frontend Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```bash
# API Configuration
REACT_APP_BACKEND_URL=http://localhost:8000    # Backend API URL
```

For production deployments, use `.env.production`:

```bash
REACT_APP_BACKEND_URL=https://api.example.com
```

---

## Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python server.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
yarn start
```

Access the application at `http://localhost:3000`

### Production Build

**Frontend Build:**
```bash
cd frontend
yarn build
# Output: frontend/build/ directory ready for deployment
```

**Backend for Production:**
```bash
cd backend
gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

---

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_decision_tree.py -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=html
```

Test files included:
- `test_basic.py` - Core functionality tests
- `test_decision_tree.py` - Decision tree algorithm tests (20+ tests)
- `test_api_endpoints.py` - API endpoint validation and error handling
- `test_ga.py` - Genetic algorithm tests
- `test_integration.py` - End-to-end integration tests
- `test_knn.py` - K-Nearest Neighbors tests
- `test_pydantic_validation.py` - Input validation tests
- `test_regression.py` - Regression algorithm tests
- `test_server.py` - Server configuration tests

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

### Test Results

Currently **107+ tests** covering:
- ✅ Decision tree classifier/regressor
- ✅ KNN classification and regression
- ✅ Regression algorithms (Linear, Ridge, Lasso, Elastic Net)
- ✅ Genetic algorithms
- ✅ Input validation and error handling
- ✅ API endpoint error responses
- ✅ Pydantic data validation

---

## Deployment

### Frontend Deployment (Vercel)

1. **Connect GitHub Repository**
   ```bash
   # Push code to GitHub
   git push origin main
   ```

2. **Configure Vercel**
   - Go to https://vercel.com
   - Import project from GitHub
   - Set Build Settings:
     - Build Command: `cd frontend && yarn build`
     - Output Directory: `frontend/build`
   - Set Environment Variables:
     ```
     REACT_APP_BACKEND_URL=https://your-backend-api.com
     ```

3. **Deploy**
   - Vercel automatically deploys on push to main

### Backend Deployment (Render)

1. **Create Render Web Service**
   - Go to https://render.com
   - New → Web Service
   - Connect GitHub repository

2. **Configure Service**
   - Environment: Python 3.11
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker app.main:app`
   - Set Environment Variables:
     ```
     FRONTEND_URL=https://your-frontend.vercel.app
     LOG_LEVEL=INFO
     ```

3. **Deploy**
   - Render automatically deploys on push

### Docker Deployment (Optional)

**Backend Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
CMD ["python", "server.py"]
```

**Build and Run:**
```bash
docker build -t ml-visualizer-backend -f Dockerfile.backend .
docker run -p 8000:8000 ml-visualizer-backend
```

---

## Troubleshooting

### Backend Issues

**Issue: "Backend unreachable" in frontend**
- Ensure backend is running: `http://localhost:8000/health`
- Check `REACT_APP_BACKEND_URL` environment variable
- Verify CORS settings in `backend/app/main.py`
- Check for port conflicts: `lsof -i :8000`

**Issue: Import errors in backend**
```bash
cd backend
pip install --upgrade -r requirements.txt
```

**Issue: Database/Dataset loading errors**
```bash
cd backend
python -c "from sklearn.datasets import load_iris; load_iris()"
```

### Frontend Issues

**Issue: "Cannot find module" errors**
```bash
cd frontend
rm -rf node_modules
yarn install
yarn start
```

**Issue: Port 3000 already in use**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :3000
kill -9 <PID>
```

### CORS Errors

**Issue: "CORS policy: Response to preflight request"**

Check `backend/app/main.py`:
```python
FRONTEND_URL=http://localhost:3000  # for development
FRONTEND_URL=https://yoursite.vercel.app  # for production
```

### Test Failures

```bash
# Verbose output
pytest tests/ -vv

# Stop on first failure
pytest tests/ -x

# Show print statements
pytest tests/ -s
```

---

## Architecture Overview

### Directory Structure

```
emergent/
├── backend/                    # FastAPI server
│   ├── app/
│   │   ├── main.py            # FastAPI app, CORS config, routes
│   │   ├── routers/           # API endpoints for each algorithm
│   │   ├── services/          # Algorithm implementations (from scratch)
│   │   ├── models/            # Pydantic schemas & validation
│   │   └── utils/             # Utility functions
│   ├── tests/                 # 107+ pytest test cases
│   ├── requirements.txt       # Python dependencies
│   └── server.py              # Entry point
│
└── frontend/                  # React app
    ├── src/
    │   ├── components/        # React components by algorithm
    │   ├── lib/              # API client, utilities
    │   ├── store/            # Zustand state management
    │   ├── hooks/            # Custom React hooks
    │   └── App.js            # Root with error boundary
    ├── package.json
    └── README.md
```

### Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend | React | 19.0.0 |
| Frontend UI | Tailwind + shadcn/ui | Latest |
| Visualization | Plotly.js + react-d3-tree | Latest |
| State | Zustand | 5.0.12 |
| Backend | FastAPI | 0.110.1 |
| Deployment | Vercel + Render | Latest |

### Data Flow

```
User Interface (React)
    ↓
API Client (lib/api.js)
    ↓
FastAPI Backend (app/routers)
    ↓
Algorithm Services (app/services)
    ↓
Custom ML Implementations
    ↓
Response → Tree JSON/Metrics
    ↓
Visualization (Plotly/react-d3-tree)
```

---

## Key Features

### Decision Tree Visualization
- ✅ Improved node contrast and visibility
- ✅ Automatic zoom/translate based on tree depth
- ✅ Gini vs Entropy side-by-side comparison
- ✅ Feature importance bar chart
- ✅ Responsive design

### Error Handling
- ✅ React Error Boundary for graceful failures
- ✅ Backend validation with helpful error messages
- ✅ API error status codes (400, 500)
- ✅ Structured logging for debugging

### Performance
- ✅ Memoized components to reduce re-renders
- ✅ Debounced API requests
- ✅ Lazy loading of datasets
- ✅ Efficient tree rendering

### Accessibility
- ✅ ARIA labels on interactive elements
- ✅ High contrast color scheme
- ✅ Keyboard navigation support
- ✅ Screen reader friendly

---

## Contributing

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes and commit: `git commit -am 'Add feature'`
3. Run tests: `pytest tests/ -v`
4. Push and create pull request

---

## Support

For issues and questions:
- Check the [Troubleshooting](#troubleshooting) section
- Review test files for usage examples
- Check API docs at `http://localhost:8000/docs`
