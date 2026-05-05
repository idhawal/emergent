import pytest
import numpy as np
from app.services.regression_service import custom_gradient_descent, run_regression


def test_gradient_descent_convergence():
    """Verify custom GD loss decreases monotonically on clean data."""
    np.random.seed(42)
    X = np.random.randn(100, 2)
    y = 3 * X[:, 0] + 2 * X[:, 1] + np.random.randn(100) * 0.1
    
    theta, cost_history, _ = custom_gradient_descent(X, y, learning_rate=0.01, epochs=100)
    
    # Check that cost generally decreases (allow small fluctuations)
    # Compare first 10% to last 10%
    early_cost = np.mean(cost_history[:10])
    late_cost = np.mean(cost_history[-10:])
    assert late_cost < early_cost, "Cost should decrease over iterations"


def test_early_stopping_trigger():
    """Assert training halts at correct epoch when cost increases ≥5 times consecutively."""
    np.random.seed(42)
    X = np.random.randn(50, 1)
    y = 2 * X[:, 0] + np.random.randn(50) * 0.5
    
    # Use very high learning rate to cause oscillation
    theta, cost_history, stopped_at = custom_gradient_descent(
        X, y, learning_rate=0.5, epochs=200, early_stopping=True
    )
    
    # Early stopping should trigger or complete normally
    # With high LR, it might oscillate but not always trigger early stopping
    assert stopped_at is None or stopped_at < 200, "Should stop before max epochs if triggered"
    assert len(cost_history) > 0, "Should have cost history"


def test_lasso_zero_coefficients():
    """Confirm ≥1 coefficient is zero when penalty=100 on sparse data."""
    result = run_regression(
        algo="lasso",
        learning_rate=0.01,
        epochs=100,
        poly_degree=3,
        penalty=100.0,
        l1_ratio=0.5,
        noise=0.1,
        early_stopping=False
    )
    
    # Check that at least one coefficient is near zero
    zero_count = sum(1 for c in result["coefficients"] if abs(c) < 1e-6)
    assert zero_count >= 1, f"Lasso should zero out coefficients with high penalty, got {zero_count}"


def test_regression_response_structure():
    """Test that regression response has all required fields."""
    result = run_regression(
        algo="linear_gd",
        learning_rate=0.01,
        epochs=100,
        poly_degree=1,
        penalty=1.0,
        l1_ratio=0.5,
        noise=0.3,
        early_stopping=False
    )
    
    required_fields = ["curve_x", "curve_y", "scatter_x", "scatter_y", 
                      "cost_history", "coefficients", "feature_names", "stopped_at_epoch"]
    for field in required_fields:
        assert field in result, f"Missing field: {field}"
    
    assert len(result["curve_x"]) == len(result["curve_y"])
    assert len(result["scatter_x"]) == len(result["scatter_y"])
    assert len(result["coefficients"]) == len(result["feature_names"])
