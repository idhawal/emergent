"""
Integration tests for API endpoints with error handling validation.
Tests ensure proper HTTP status codes and error messages are returned.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint():
    """Test root API endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "version" in response.json()


def test_decision_tree_valid_request():
    """Test valid decision tree request."""
    payload = {
        "task": "classifier",
        "criterion": "gini",
        "max_depth": 3,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "dataset": "iris",
        "uploaded_data": None
    }
    response = client.post("/api/decision_tree", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "tree_json" in data
    assert "accuracy" in data


def test_decision_tree_invalid_criterion_status():
    """Test that invalid criterion returns 400 status."""
    payload = {
        "task": "classifier",
        "criterion": "invalid",
        "max_depth": 3,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "dataset": "iris",
        "uploaded_data": None
    }
    response = client.post("/api/decision_tree", json=payload)
    assert response.status_code == 400
    assert "Invalid input" in response.json()["detail"]


def test_decision_tree_entropy_regressor_error():
    """Test that entropy with regressor returns 400 status."""
    payload = {
        "task": "regressor",
        "criterion": "entropy",
        "max_depth": 3,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "dataset": "iris",
        "uploaded_data": None
    }
    response = client.post("/api/decision_tree", json=payload)
    assert response.status_code == 400
    assert "entropy criterion is only valid" in response.json()["detail"]


def test_decision_tree_invalid_min_samples_split():
    """Test that invalid min_samples_split returns 400 status."""
    payload = {
        "task": "classifier",
        "criterion": "gini",
        "max_depth": 3,
        "min_samples_split": 1,  # Invalid: must be >= 2
        "min_samples_leaf": 1,
        "dataset": "iris",
        "uploaded_data": None
    }
    response = client.post("/api/decision_tree", json=payload)
    assert response.status_code == 400
    assert "min_samples_split" in response.json()["detail"]


def test_docs_endpoint_exists():
    """Test that OpenAPI documentation is available."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_endpoint_exists():
    """Test that ReDoc documentation is available."""
    response = client.get("/redoc")
    assert response.status_code == 200
