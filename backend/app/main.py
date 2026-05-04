from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import regression, knn, decision_tree, genetic_algorithm
import os

# Create FastAPI app
app = FastAPI(title="ML Visualizer API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(regression.router, prefix="/api")
app.include_router(knn.router, prefix="/api")
app.include_router(decision_tree.router, prefix="/api")
app.include_router(genetic_algorithm.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "ML Visualizer API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
