import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import regression, knn, decision_tree, genetic_algorithm, datasets, upload

# Create FastAPI app
app = FastAPI(title="ML Visualizer API", version="1.0.0")

FRONTEND_URL = os.environ.get("FRONTEND_URL", "")

# Configure CORS for local + Vercel deployments.
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://emergent-one.vercel.app",
        *([FRONTEND_URL] if FRONTEND_URL else []),
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)

# Include routers
app.include_router(regression.router, prefix="/api")
app.include_router(knn.router, prefix="/api")
app.include_router(decision_tree.router, prefix="/api")
app.include_router(genetic_algorithm.router, prefix="/api")
app.include_router(datasets.router, prefix="/api")
app.include_router(upload.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "ML Visualizer API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
