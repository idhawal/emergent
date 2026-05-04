import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.schemas import (
    RegressionRequest, KNNRequest, DecisionTreeRequest, GARequest
)

client = TestClient(app)


def test_pydantic_rejects_invalid_regression():
    """Each endpoint rejects out-of-range values with HTTP 422."""
    # Invalid learning rate (should be > 0 and <= 1.0)
    response = client.post("/api/regression", json={
        "algo": "linear_gd",
        "learning_rate": 2.0,  # Invalid: > 1.0
        "epochs": 100,
        "poly_degree": 1,
        "penalty": 1.0,
        "l1_ratio": 0.5,
        "noise": 0.3,
        "early_stopping": False
    })
    assert response.status_code == 422


def test_pydantic_rejects_invalid_knn():
    """KNN endpoint rejects invalid K value."""
    response = client.post("/api/knn", json={
        "k": 100,  # Invalid: > 50
        "metric": "euclidean",
        "weights": "uniform",
        "task": "classification",
        "dataset": "moons"
    })
    assert response.status_code == 422


def test_pydantic_rejects_invalid_tree():
    """Decision tree endpoint rejects invalid max_depth."""
    response = client.post("/api/decision_tree", json={
        "task": "classifier",
        "criterion": "gini",
        "max_depth": 20,  # Invalid: > 10
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "dataset": "iris"
    })
    assert response.status_code == 422


def test_pydantic_rejects_invalid_ga():
    """GA endpoint rejects invalid pop_size."""
    response = client.post("/api/genetic_algorithm", json={
        "function": "sphere",
        "pop_size": 5,  # Invalid: < 10
        "mutation_rate": 0.1,
        "crossover_rate": 0.8,
        "generations": 50,
        "eta_m": 20,
        "eta_c": 15
    })
    assert response.status_code == 422
