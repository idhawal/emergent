# ML Visualizer

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-brightgreen.svg)](https://www.python.org/downloads/)
[![Node 18+](https://img.shields.io/badge/Node-18%2B-brightgreen.svg)](https://nodejs.org/)
[![Tests](https://img.shields.io/badge/Tests-122%20Passing-brightgreen.svg)](backend/tests/)

Interactive web application for exploring, tuning, and understanding machine learning algorithms through real-time visualization. **All algorithms are implemented from scratch using NumPy** — no scikit-learn models. Perfect for learning, teaching, and algorithm experimentation.

**Live Deployment:**
- **Frontend**: [https://emergent-six-zeta.vercel.app/](https://emergent-six-zeta.vercel.app/)
- **Backend API**: [https://emergent-av9b.onrender.com/docs](https://emergent-av9b.onrender.com/docs)

---

## Why ML Visualizer?

- **Learn by Doing**: Adjust parameters and see results update in real-time
- **Understand Algorithms**: Interactive visualizations demystify machine learning
- **From-Scratch Implementation**: See actual algorithms without black-box libraries
- **Multiple Algorithms**: Regression, KNN, Decision Trees, and Genetic Algorithms
- **Production Ready**: Global deployment with responsive design and comprehensive testing

---

## Features

### Interactive Algorithm Pages

| Algorithm | Capabilities | Visualizations |
|-----------|--------------|-----------------|
| **Regression** | Linear, Polynomial, Ridge, Lasso, Elastic Net | Gradient descent steps, cost curves, decision boundaries |
| **K-Nearest Neighbors** | Euclidean/Manhattan distance, weighted voting | Decision boundaries, nearest neighbor connections |
| **Decision Trees** | CART classifier/regressor, Gini/Entropy comparison | Tree structure with dynamic layout, feature importance |
| **Genetic Algorithm** | Real-coded GA with SBX crossover, polynomial mutation | Population evolution, fitness landscape |

### Core Features

- **Real-Time Parameter Adjustment**: Change settings and see results instantly
- **Theory Drawer**: Mathematical equations and parameter documentation for each algorithm
- **Dataset Management**: 20+ built-in datasets + custom CSV uploads
- **Comparison Mode**: Side-by-side algorithm analysis
- **Responsive Design**: Optimized for desktop, tablet, and mobile
- **Accessible UI**: WCAG AAA compliance, keyboard navigation, screen reader support

---

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- yarn or npm

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python server.py
```

The backend will start on `http://localhost:8000`

Access the API documentation: `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend
yarn install
echo "REACT_APP_BACKEND_URL=http://localhost:8000" > .env.local
yarn start
```

The frontend will open at `http://localhost:3000`

### Verify Installation

```bash
# Backend health check
curl http://localhost:8000/health

# Frontend loads at
open http://localhost:3000
```

---

## Usage Guide

### Adjusting Parameters

1. Navigate to any algorithm page (Regression, KNN, Decision Tree, or GA)
2. Use the sidebar controls to adjust parameters:
   - Sliders for continuous values
   - Dropdowns for categorical options
   - Input fields for specific values
3. Watch the visualization update in real-time
4. Hover over parameters for detailed explanations

### Understanding Visualizations

Each algorithm provides:
- **Main Plot**: Visual representation of the algorithm's decision boundary or results
- **Metrics Panel**: Key statistics (accuracy, cost, gini, etc.)
- **Theory Drawer**: Mathematical background and parameter documentation
- **Interactive Elements**: Click/hover to explore specific aspects

### Using Theory Drawer

Click the "Theory" button in the top navigation to:
- Read mathematical equations for the algorithm
- Understand each parameter's role
- Learn about the underlying concepts
- Explore trade-offs between different settings

### Uploading Custom Data

1. On any algorithm page, click "Upload CSV"
2. Your CSV should contain:
   - Numeric columns for features
   - A target column (last column assumed as target for classification)
3. The application will automatically:
   - Normalize numeric features
   - Encode categorical columns
   - Split into train/test sets
4. Results update with your data

### Comparison Mode (Decision Tree Only)

1. In the Decision Tree page, enable "Compare Mode"
2. Two panels appear side-by-side
3. Adjust settings independently on each panel
4. Metrics show both results for easy comparison

---

## Technology Stack

### Frontend
- **React 19**: Modern UI framework with hooks and concurrent features
- **Tailwind CSS**: Utility-first styling
- **shadcn/ui**: High-quality component library
- **Plotly.js**: Interactive 2D visualizations
- **react-d3-tree**: Tree structure visualization
- **Zustand**: Lightweight state management
- **Lucide Icons**: Consistent icon library

### Backend
- **FastAPI**: Modern Python web framework with automatic documentation
- **Python 3.11**: Latest stable Python version
- **NumPy**: All algorithms implemented with NumPy (no sklearn)
- **Pydantic v2**: Data validation and settings management
- **pytest**: 122 comprehensive tests

### Deployment
- **Frontend**: Vercel (automatic deployments on main branch)
- **Backend**: Render (auto-scaling with CPU/memory management)
- **Monitoring**: Health checks and error tracking

---

## Dataset Information

### Built-In Datasets

**Regression:**
- `linear`: Simple linear relationship
- `sine`: Non-linear sinusoidal pattern
- `quadratic`: Quadratic function with noise

**Classification:**
- `iris`: Classic Iris flower classification (150 samples, 4 features, 3 classes)
- `breast_cancer`: Cancer diagnosis data (569 samples, 30 features, 2 classes)
- `moons`: Two interleaving half circles
- `circles`: Two concentric circles
- `blobs`: Gaussian blob clusters

### Custom Datasets

Upload any CSV file with numeric features. Requirements:
- At least 2 numeric columns
- Optional target column (assumed as last column)
- Rows with missing values will be handled appropriately

---

## Testing

Run the comprehensive test suite:

```bash
cd backend
pytest tests/ -v                          # Run all tests
pytest tests/test_decision_tree.py -v    # Test specific algorithm
pytest --cov=app --cov-report=html       # Generate coverage report
```

### Test Coverage

- **122 total tests** covering:
  - Unit tests for all services
  - Integration tests for API endpoints
  - Algorithm correctness verification
  - Edge cases and boundary conditions
  - From-scratch implementation verification (no sklearn usage)

### Verify From-Scratch Implementation

```bash
# Verify no sklearn models used in services
grep -r "from sklearn" backend/app/services/
# Should return no results
```

---

## Deployment Guide

### Frontend (Vercel)

1. **Connect Repository**
   - Push code to GitHub
   - Go to [vercel.com](https://vercel.com)
   - Create new project and select your repository

2. **Configure Environment**
   - Set `REACT_APP_BACKEND_URL` to your backend URL
   - Example: `https://your-backend.onrender.com`

3. **Deploy**
   - Automatic deployment on main branch push
   - Vercel handles building: `yarn build`
   - Static files served globally via CDN

### Backend (Render)

1. **Create Render Service**
   - Go to [render.com](https://render.com)
   - Create new Web Service
   - Select your repository and backend directory

2. **Configure Build & Start**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python server.py`

3. **Set Environment Variables**
   - `FRONTEND_URL`: Your Vercel frontend URL
   - `PORT`: Default 8000 (Render sets automatically)

4. **Deploy**
   - Automatic deployment on main branch push
   - Render manages auto-scaling and uptime

---

## Project Structure

```
emergent/
├── frontend/                 # React web application
│   ├── src/
│   │   ├── components/       # Algorithm pages, UI components
│   │   │   ├── regression/   # Regression visualizations
│   │   │   ├── knn/          # K-Nearest Neighbors
│   │   │   ├── decision-tree/ # Decision Tree visualization
│   │   │   ├── genetic/      # Genetic Algorithm
│   │   │   ├── layout/       # Layout components (Navbar, Sidebar)
│   │   │   ├── shared/       # Shared components (charts, theory)
│   │   │   └── ui/           # Base UI components
│   │   ├── store/            # Zustand state management
│   │   ├── lib/api.js        # API client
│   │   ├── hooks/            # Custom React hooks
│   │   └── index.css         # Global styles
│   ├── public/               # Static assets
│   └── package.json
│
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── main.py           # FastAPI app setup
│   │   ├── routers/          # API endpoints
│   │   │   ├── regression.py
│   │   │   ├── knn.py
│   │   │   ├── decision_tree.py
│   │   │   ├── genetic_algorithm.py
│   │   │   └── utils.py
│   │   ├── services/         # ML implementations (from scratch)
│   │   │   ├── regression_service.py
│   │   │   ├── knn_service.py
│   │   │   ├── tree_service.py
│   │   │   ├── ga_service.py
│   │   │   └── dataset_service.py
│   │   ├── models/           # Pydantic schemas
│   │   ├── utils/            # Utility functions
│   │   └── config.py         # Configuration
│   ├── tests/                # Test suite (122 tests)
│   ├── requirements.txt      # Python dependencies
│   └── server.py             # Development server
│
├── README.md                 # This file
├── ARCHITECTURE.md           # System architecture details
└── LICENSE                   # MIT License
```

---

## Contributing

### Development Workflow

1. **Create a branch** for your feature
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes** following the project style
   - Frontend: Follow React best practices, use functional components
   - Backend: Follow PEP 8, add type hints
   - Keep commits focused and descriptive

3. **Test thoroughly**
   ```bash
   cd backend && pytest tests/ -v
   cd frontend && yarn build
   ```

4. **Create a pull request**
   - Describe what changed and why
   - Link related issues
   - Request reviews from team members

### Code Style

- **Python**: PEP 8 (use black for formatting)
- **JavaScript**: ESLint config included
- **Git Commits**: Use imperative mood ("Add feature" not "Added feature")

### Before Submitting PR

- [ ] Tests pass: `pytest tests/ -v`
- [ ] No new warnings or errors
- [ ] Documentation updated if needed
- [ ] Code reviewed locally
- [ ] Commit messages are clear

---

## Troubleshooting

### Backend Connection Issues

**Problem**: Frontend can't reach backend
```
CORS error or Connection refused
```

**Solutions**:
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check `REACT_APP_BACKEND_URL` in `.env.local`
3. In development, ensure `http://localhost:3000` is in CORS whitelist
4. On production, verify backend URL matches exactly

### Import/Module Errors

**Problem**: `ModuleNotFoundError` when running backend
```bash
# Solution: Install dependencies
cd backend
pip install -r requirements.txt
```

**Problem**: `yarn install` fails
```bash
# Try clearing cache
yarn cache clean
yarn install
```

### Performance Issues

**Problem**: Slow visualization rendering
- Reduce dataset size
- Close browser tabs
- Check browser console for errors

**Problem**: API responses are slow
- Check backend logs for errors
- Verify dataset size
- Consider limiting to built-in datasets

### Common Errors

| Error | Solution |
|-------|----------|
| `Need at least 2 numeric columns` | Ensure your CSV has numeric features |
| `404 Not Found on /api/datasets` | Backend not running or wrong URL |
| `Port 3000/8000 already in use` | Kill existing process: `lsof -i :3000` |
| `CORS error` | Check backend `CORS` configuration |

---

## Performance Characteristics

### Typical Response Times
- Small dataset (< 1000 samples): 50-200ms
- Medium dataset (1000-10000 samples): 200-500ms
- Large dataset (> 10000 samples): 500ms-2s

### Memory Usage
- Frontend: 15-30 MB (varies with dataset size)
- Backend: 50-150 MB (with loaded models)
- Each decision tree: ~1-5 MB per tree

### Supported Limits
- Maximum dataset size: ~50,000 samples
- Maximum features: ~100
- Maximum tree depth: ~20 (software limited for visualization)
- Concurrent users: Limited by Render plan

---

## Security

### Input Validation
- All inputs validated with Pydantic before processing
- Type checking and range validation
- Safe numeric conversions
- CSV validation before processing

### Error Handling
- Sensitive information not exposed in error messages
- Full stack traces logged server-side only
- User-friendly error messages on client-side
- No SQL injection risk (no database)

### CORS Configuration
- Specific origin whitelist (no wildcards)
- `http://localhost:3000` for development
- `https://*.vercel.app` for deployments
- Environment-configurable for custom domains

---

## Learning Resources

### Understanding the Algorithms

- **Linear Regression**: [3Blue1Brown - Essence of Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPHP40cpilO1aH_4-S6yYvQ)
- **K-Nearest Neighbors**: [Wikipedia KNN](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm)
- **Decision Trees**: [MIT OpenCourseWare](https://ocw.mit.edu)
- **Genetic Algorithms**: [UC Davis GA Tutorial](https://www.youtube.com/watch?v=jwww7Dj56KE)

### Technical Documentation

- [React 19 Docs](https://react.dev)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [NumPy Guide](https://numpy.org/doc/)
- [Tailwind CSS](https://tailwindcss.com/docs)

---

## Known Limitations

1. **In-Memory Only**: No database, data lost on restart
2. **Single Model**: Can't save/compare multiple models (yet)
3. **2D Visualization**: Tree visualization optimized for < 1000 nodes
4. **No Real-Time Updates**: WebSocket updates not implemented (future)
5. **Export**: Can't save visualizations as images (future)

---

## Roadmap

- [ ] Model persistence and comparison
- [ ] WebSocket real-time updates
- [ ] Export visualizations as PDF/SVG
- [ ] 3D tree visualization
- [ ] Dataset caching for faster reruns
- [ ] Advanced metrics and statistics
- [ ] User accounts and saved sessions

---

## Status & Monitoring

**Production Status**: ✅ Live and Active

- Frontend: [Vercel Dashboard](https://vercel.com/dashboard)
- Backend: [Render Dashboard](https://render.com/dashboard)
- Health Check: `https://emergent-av9b.onrender.com/health`

**Last Updated**: May 2026

---

## Team

| Member | Roll Number | Email |
|--------|------|-------|
| Aryan Chawla | 23124019 | aryanc.it.23@nitj.ac.in |
| Chirag Bishnoi | 23124027 | chiragk.it.23@nitj.ac.in |
| Chaudhari Arpit Kumar | 23124026 | chaudharia.it.23@nitj.ac.in |
| Dhawal Palaiya | 23124030 | dhawalp.it.23@nitj.ac.in |

---

## License

MIT License - See [LICENSE](LICENSE) file for details

---

## Support

- 📖 **Documentation**: See [ARCHITECTURE.md](ARCHITECTURE.md)
- 🐛 **Report Issues**: Create a GitHub issue
- 💬 **Discussions**: Use GitHub Discussions
- 📧 **Questions**: Contact team members

---

**Built with ❤️ for learning and exploration**
