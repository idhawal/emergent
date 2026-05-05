from fastapi import APIRouter, HTTPException
from sklearn.datasets import load_iris, load_breast_cancer, make_moons, make_circles, make_blobs
import pandas as pd
import numpy as np

router = APIRouter()

def get_iris_data():
    """Load Iris dataset"""
    data = load_iris(as_frame=True)
    df = data.frame
    return df

def get_breast_cancer_data():
    """Load Breast Cancer dataset"""
    data = load_breast_cancer(as_frame=True)
    df = data.frame
    return df

def get_moons_data():
    """Generate moons dataset"""
    X, y = make_moons(n_samples=200, noise=0.2, random_state=42)
    df = pd.DataFrame(X, columns=["x1", "x2"])
    df["label"] = y
    return df

def get_circles_data():
    """Generate circles dataset"""
    X, y = make_circles(n_samples=200, noise=0.1, factor=0.5, random_state=42)
    df = pd.DataFrame(X, columns=["x1", "x2"])
    df["label"] = y
    return df

def get_blobs_data():
    """Generate blobs dataset"""
    X, y = make_blobs(n_samples=200, centers=3, n_features=2, random_state=42)
    df = pd.DataFrame(X, columns=["x1", "x2"])
    df["label"] = y
    return df

def get_linear_data():
    """Generate linear regression dataset"""
    np.random.seed(42)
    X = np.linspace(0, 10, 100).reshape(-1, 1)
    y = 2 * X.flatten() + 1 + np.random.randn(100) * 2
    df = pd.DataFrame({"x": X.flatten(), "y": y})
    return df

def get_sine_data():
    """Generate sine wave dataset for regression"""
    np.random.seed(42)
    X = np.linspace(0, 4 * np.pi, 100).reshape(-1, 1)
    y = np.sin(X).flatten() + np.random.randn(100) * 0.1
    df = pd.DataFrame({"x": X.flatten(), "y": y})
    return df

DATASETS = {
    "iris": get_iris_data,
    "breast_cancer": get_breast_cancer_data,
    "moons": get_moons_data,
    "circles": get_circles_data,
    "blobs": get_blobs_data,
    "linear": get_linear_data,
    "sine": get_sine_data,
}

@router.get("/datasets")
async def list_datasets():
    """List all available datasets"""
    return {
        "datasets": list(DATASETS.keys()),
        "count": len(DATASETS)
    }

@router.get("/datasets/{name}")
async def get_dataset(name: str):
    """Get a specific dataset by name"""
    if name not in DATASETS:
        raise HTTPException(
            status_code=404,
            detail=f"Dataset '{name}' not found. Available datasets: {list(DATASETS.keys())}"
        )
    
    try:
        df = DATASETS[name]()
        return {
            "name": name,
            "columns": df.columns.tolist(),
            "rows": df.to_dict(orient="records"),
            "n_samples": len(df),
            "n_features": len(df.columns) - 1 if "label" in df.columns or "target" in df.columns else len(df.columns),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading dataset: {str(e)}")
