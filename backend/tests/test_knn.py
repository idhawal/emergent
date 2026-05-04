import pytest
from app.services.knn_service import run_knn, predict_knn, compute_distance
import numpy as np


def test_knn_response_structure():
    """Test that KNN response has all required fields."""
    result = run_knn(
        k=5,
        metric="euclidean",
        weights="uniform",
        task="classification",
        dataset="moons",
        test_point=None
    )
    
    required_fields = ["train_points", "train_labels", "mesh_xx", "mesh_yy", 
                      "mesh_zz", "neighbor_indices", "test_prediction"]
    for field in required_fields:
        assert field in result, f"Missing field: {field}"
    
    assert len(result["train_points"]) > 0
    assert len(result["train_labels"]) > 0
    assert len(result["mesh_xx"]) > 0
    assert len(result["mesh_yy"]) > 0
    assert len(result["mesh_zz"]) > 0


def test_distance_metrics():
    """Test Euclidean and Manhattan distance calculations."""
    a = np.array([0, 0])
    b = np.array([3, 4])
    
    euclidean = compute_distance(a, b, "euclidean")
    manhattan = compute_distance(a, b, "manhattan")
    
    assert abs(euclidean - 5.0) < 1e-10, "Euclidean distance should be 5"
    assert abs(manhattan - 7.0) < 1e-10, "Manhattan distance should be 7"


def test_knn_with_test_point():
    """Test KNN prediction with a test point."""
    result = run_knn(
        k=5,
        metric="euclidean",
        weights="uniform",
        task="classification",
        dataset="moons",
        test_point=[0.5, 0.5]
    )
    
    # Should have neighbor indices
    assert len(result["neighbor_indices"]) == 5, "Should return 5 neighbor indices"
    # Should have a prediction
    assert result["test_prediction"] is not None, "Should have a test prediction"


def test_knn_regression_mode():
    """Test KNN in regression mode."""
    result = run_knn(
        k=5,
        metric="euclidean",
        weights="uniform",
        task="regression",
        dataset="sine",
        test_point=[0.0]
    )
    
    assert result["test_prediction"] is not None
    # Regression prediction should be a float
    assert isinstance(result["test_prediction"], (int, float))
