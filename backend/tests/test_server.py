"""Backend tests for Emergent ML Visualizer API."""
import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from server import app

client = TestClient(app)


def test_health_check():
    """Test root endpoint returns OK."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Emergent ML Visualizer API", "version": "1.0.0"}


def test_regression_endpoint():
    """Test regression API returns valid response."""
    payload = {
        "algo": "linear",
        "learning_rate": 0.1,
        "epochs": 100,
        "noise": 0.1
    }
    response = client.post("/api/regression", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "theta" in data
    assert "cost_history" in data
    assert "predictions" in data


def test_knn_endpoint():
    """Test KNN API returns valid response."""
    payload = {
        "k": 5,
        "metric": "euclidean",
        "weights": "uniform",
        "dataset": "moons"
    }
    response = client.post("/api/knn", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "boundary" in data or "predictions" in data


def test_decision_tree_endpoint():
    """Test Decision Tree API returns valid response."""
    payload = {
        "task": "classifier",
        "criterion": "gini",
        "max_depth": 3,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "dataset": "iris"
    }
    response = client.post("/api/decision_tree", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "tree_json" in data
    assert "accuracy" in data
    assert "feature_importances" in data


def test_genetic_algorithm_endpoint():
    """Test Genetic Algorithm API returns valid response."""
    payload = {
        "function": "sphere",
        "pop_size": 50,
        "mutation_rate": 0.1,
        "crossover_rate": 0.8,
        "generations": 80,
        "nm": 20,
        "nc": 15
    }
    response = client.post("/api/genetic_algorithm", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "population" in data or "fitness" in data
