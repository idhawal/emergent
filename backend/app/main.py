from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import regression, knn, decision_tree, genetic_algorithm, datasets, upload
import os

# Create FastAPI app
app = FastAPI(title="ML Visualizer API", version="1.0.0")

# Configure CORS - allow all origins for development, lock down for production
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://emergent-one.vercel.app",  # Production frontend
        "https://*.vercel.app",  # All Vercel preview deployments
        "*",  # Allow all origins (remove this in production and specify exact domains)
    ],
    allow_methods=["*"],
    allow_headers=["*"],
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
