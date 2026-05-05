import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import regression, knn, decision_tree, genetic_algorithm, datasets, upload

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app with detailed documentation
app = FastAPI(
    title="ML Visualizer API",
    version="1.0.0",
    description="Interactive machine learning algorithm visualizer with real-time parameter tuning.",
    docs_url="/docs",
    redoc_url="/redoc",
)

FRONTEND_URL = os.environ.get("FRONTEND_URL", "")

logger.info("Initializing ML Visualizer API")

# Configure CORS for local + Vercel deployments
cors_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://emergent-one.vercel.app",
]

if FRONTEND_URL:
    cors_origins.append(FRONTEND_URL)
    logger.info(f"Added FRONTEND_URL to CORS origins: {FRONTEND_URL}")

logger.info(f"Configuring CORS with origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=cors_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)

# Include routers with prefixes
app.include_router(regression.router, prefix="/api", tags=["regression"])
app.include_router(knn.router, prefix="/api", tags=["knn"])
app.include_router(decision_tree.router, prefix="/api", tags=["decision_tree"])
app.include_router(genetic_algorithm.router, prefix="/api", tags=["genetic_algorithm"])
app.include_router(datasets.router, prefix="/api", tags=["datasets"])
app.include_router(upload.router, prefix="/api", tags=["upload"])


@app.get("/")
async def root():
    """API root endpoint with version info."""
    return {
        "message": "ML Visualizer API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "ml-visualizer-api"}


@app.on_event("startup")
async def startup_event():
    logger.info("ML Visualizer API started successfully")
