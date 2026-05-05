"""
Test Pydantic validation - ensure invalid inputs are rejected with HTTP 422.
Spec requirement: Test that endpoints reject out-of-range values.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestRegressionValidation:
    """Test regression endpoint validation."""
    
    def test_reject_invalid_learning_rate_too_high(self):
        """Learning rate must be <= 1.0"""
        response = client.post("/api/regression", json={
            "algo": "linear_gd",
            "learning_rate": 2.0,  # Invalid: > 1.0
            "epochs": 100,
            "poly_degree": 2,
            "penalty": 1.0,
            "l1_ratio": 0.5,
            "noise": 0.3,
            "early_stopping": False
        })
        assert response.status_code == 422
    
    def test_reject_invalid_learning_rate_zero(self):
        """Learning rate must be > 0"""
        response = client.post("/api/regression", json={
            "algo": "linear_gd",
            "learning_rate": 0.0,  # Invalid: must be > 0
            "epochs": 100,
            "poly_degree": 2,
            "penalty": 1.0,
            "l1_ratio": 0.5,
            "noise": 0.3,
            "early_stopping": False
        })
        assert response.status_code == 422
    
    def test_reject_invalid_epochs_zero(self):
        """Epochs must be >= 1"""
        response = client.post("/api/regression", json={
            "algo": "linear_gd",
            "learning_rate": 0.01,
            "epochs": 0,  # Invalid: must be >= 1
            "poly_degree": 2,
            "penalty": 1.0,
            "l1_ratio": 0.5,
            "noise": 0.3,
            "early_stopping": False
        })
        assert response.status_code == 422
    
    def test_reject_invalid_epochs_too_high(self):
        """Epochs must be <= 10000"""
        response = client.post("/api/regression", json={
            "algo": "linear_gd",
            "learning_rate": 0.01,
            "epochs": 20000,  # Invalid: > 10000
            "poly_degree": 2,
            "penalty": 1.0,
            "l1_ratio": 0.5,
            "noise": 0.3,
            "early_stopping": False
        })
        assert response.status_code == 422
    
    def test_reject_invalid_poly_degree(self):
        """Poly degree must be 1-4"""
        response = client.post("/api/regression", json={
            "algo": "polynomial",
            "learning_rate": 0.01,
            "epochs": 100,
            "poly_degree": 10,  # Invalid: > 4
            "penalty": 1.0,
            "l1_ratio": 0.5,
            "noise": 0.3,
            "early_stopping": False
        })
        assert response.status_code == 422
    
    def test_reject_invalid_penalty_negative(self):
        """Penalty must be >= 0"""
        response = client.post("/api/regression", json={
            "algo": "ridge",
            "learning_rate": 0.01,
            "epochs": 100,
            "poly_degree": 2,
            "penalty": -1.0,  # Invalid: < 0
            "l1_ratio": 0.5,
            "noise": 0.3,
            "early_stopping": False
        })
        assert response.status_code == 422
    
    def test_reject_invalid_l1_ratio(self):
        """l1_ratio must be 0.0-1.0"""
        response = client.post("/api/regression", json={
            "algo": "elastic_net",
            "learning_rate": 0.01,
            "epochs": 100,
            "poly_degree": 2,
            "penalty": 1.0,
            "l1_ratio": 1.5,  # Invalid: > 1.0
            "noise": 0.3,
            "early_stopping": False
        })
        assert response.status_code == 422
    
    def test_reject_invalid_noise(self):
        """Noise must be 0.0-1.0"""
        response = client.post("/api/regression", json={
            "algo": "linear_gd",
            "learning_rate": 0.01,
            "epochs": 100,
            "poly_degree": 2,
            "penalty": 1.0,
            "l1_ratio": 0.5,
            "noise": 2.0,  # Invalid: > 1.0
            "early_stopping": False
        })
        assert response.status_code == 422
    
    def test_reject_invalid_algo(self):
        """Algorithm must be one of the valid options"""
        response = client.post("/api/regression", json={
            "algo": "invalid_algo",  # Invalid
            "learning_rate": 0.01,
            "epochs": 100,
            "poly_degree": 2,
            "penalty": 1.0,
            "l1_ratio": 0.5,
            "noise": 0.3,
            "early_stopping": False
        })
        assert response.status_code == 422
    
    def test_accept_valid_regression_request(self):
        """Valid request should return 200"""
        response = client.post("/api/regression", json={
            "algo": "linear_gd",
            "learning_rate": 0.01,
            "epochs": 100,
            "poly_degree": 2,
            "penalty": 1.0,
            "l1_ratio": 0.5,
            "noise": 0.3,
            "early_stopping": False
        })
        assert response.status_code == 200


class TestKNNValidation:
    """Test KNN endpoint validation."""
    
    def test_reject_invalid_k_zero(self):
        """K must be >= 1"""
        response = client.post("/api/knn", json={
            "k": 0,  # Invalid: must be >= 1
            "metric": "euclidean",
            "weights": "uniform",
            "task": "classification",
            "dataset": "moons",
            "test_point": None
        })
        assert response.status_code == 422
    
    def test_reject_invalid_k_too_high(self):
        """K must be <= 50"""
        response = client.post("/api/knn", json={
            "k": 100,  # Invalid: > 50
            "metric": "euclidean",
            "weights": "uniform",
            "task": "classification",
            "dataset": "moons",
            "test_point": None
        })
        assert response.status_code == 422
    
    def test_reject_invalid_metric(self):
        """Metric must be euclidean or manhattan"""
        response = client.post("/api/knn", json={
            "k": 5,
            "metric": "invalid_metric",  # Invalid
            "weights": "uniform",
            "task": "classification",
            "dataset": "moons",
            "test_point": None
        })
        assert response.status_code == 422
    
    def test_reject_invalid_weights(self):
        """Weights must be uniform or distance"""
        response = client.post("/api/knn", json={
            "k": 5,
            "metric": "euclidean",
            "weights": "invalid_weights",  # Invalid
            "task": "classification",
            "dataset": "moons",
            "test_point": None
        })
        assert response.status_code == 422
    
    def test_reject_invalid_task(self):
        """Task must be classification or regression"""
        response = client.post("/api/knn", json={
            "k": 5,
            "metric": "euclidean",
            "weights": "uniform",
            "task": "invalid_task",  # Invalid
            "dataset": "moons",
            "test_point": None
        })
        assert response.status_code == 422
    
    def test_reject_invalid_dataset(self):
        """Dataset must be one of the valid options"""
        response = client.post("/api/knn", json={
            "k": 5,
            "metric": "euclidean",
            "weights": "uniform",
            "task": "classification",
            "dataset": "invalid_dataset",  # Invalid
            "test_point": None
        })
        assert response.status_code == 422
    
    def test_accept_valid_knn_request(self):
        """Valid request should return 200"""
        response = client.post("/api/knn", json={
            "k": 5,
            "metric": "euclidean",
            "weights": "uniform",
            "task": "classification",
            "dataset": "moons",
            "test_point": None
        })
        assert response.status_code == 200


class TestDecisionTreeValidation:
    """Test decision tree endpoint validation."""
    
    def test_reject_invalid_task(self):
        """Task must be classifier or regressor"""
        response = client.post("/api/decision_tree", json={
            "task": "invalid_task",  # Invalid
            "criterion": "gini",
            "max_depth": 3,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "dataset": "iris"
        })
        assert response.status_code == 422
    
    def test_reject_invalid_criterion(self):
        """Criterion must be gini or entropy"""
        response = client.post("/api/decision_tree", json={
            "task": "classifier",
            "criterion": "invalid_criterion",  # Invalid
            "max_depth": 3,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "dataset": "iris"
        })
        assert response.status_code == 422
    
    def test_reject_invalid_max_depth_zero(self):
        """Max depth must be >= 1 or None"""
        response = client.post("/api/decision_tree", json={
            "task": "classifier",
            "criterion": "gini",
            "max_depth": 0,  # Invalid: must be >= 1 or None
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "dataset": "iris"
        })
        assert response.status_code == 422
    
    def test_reject_invalid_max_depth_too_high(self):
        """Max depth must be <= 10"""
        response = client.post("/api/decision_tree", json={
            "task": "classifier",
            "criterion": "gini",
            "max_depth": 20,  # Invalid: > 10
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "dataset": "iris"
        })
        assert response.status_code == 422
    
    def test_reject_invalid_min_samples_split(self):
        """Min samples split must be 2-20"""
        response = client.post("/api/decision_tree", json={
            "task": "classifier",
            "criterion": "gini",
            "max_depth": 3,
            "min_samples_split": 1,  # Invalid: must be >= 2
            "min_samples_leaf": 1,
            "dataset": "iris"
        })
        assert response.status_code == 422
    
    def test_reject_invalid_min_samples_leaf(self):
        """Min samples leaf must be 1-20"""
        response = client.post("/api/decision_tree", json={
            "task": "classifier",
            "criterion": "gini",
            "max_depth": 3,
            "min_samples_split": 2,
            "min_samples_leaf": 0,  # Invalid: must be >= 1
            "dataset": "iris"
        })
        assert response.status_code == 422
    
    def test_reject_invalid_dataset(self):
        """Dataset must be one of the valid options"""
        response = client.post("/api/decision_tree", json={
            "task": "classifier",
            "criterion": "gini",
            "max_depth": 3,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "dataset": "invalid_dataset"  # Invalid
        })
        assert response.status_code == 422
    
    def test_accept_valid_tree_request(self):
        """Valid request should return 200"""
        response = client.post("/api/decision_tree", json={
            "task": "classifier",
            "criterion": "gini",
            "max_depth": 3,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "dataset": "iris"
        })
        assert response.status_code == 200
    
    def test_accept_null_max_depth(self):
        """None/null max_depth should be accepted"""
        response = client.post("/api/decision_tree", json={
            "task": "classifier",
            "criterion": "gini",
            "max_depth": None,  # Valid: None is allowed
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "dataset": "iris"
        })
        assert response.status_code == 200


class TestGeneticAlgorithmValidation:
    """Test genetic algorithm endpoint validation."""
    
    def test_reject_invalid_function(self):
        """Function must be one of the valid options"""
        response = client.post("/api/genetic_algorithm", json={
            "function": "invalid_function",  # Invalid
            "pop_size": 50,
            "mutation_rate": 0.1,
            "crossover_rate": 0.8,
            "generations": 100,
            "eta_m": 20,
            "eta_c": 15
        })
        assert response.status_code == 422
    
    def test_reject_invalid_pop_size_too_small(self):
        """Pop size must be >= 10"""
        response = client.post("/api/genetic_algorithm", json={
            "function": "sphere",
            "pop_size": 5,  # Invalid: < 10
            "mutation_rate": 0.1,
            "crossover_rate": 0.8,
            "generations": 100,
            "eta_m": 20,
            "eta_c": 15
        })
        assert response.status_code == 422
    
    def test_reject_invalid_pop_size_too_large(self):
        """Pop size must be <= 200"""
        response = client.post("/api/genetic_algorithm", json={
            "function": "sphere",
            "pop_size": 300,  # Invalid: > 200
            "mutation_rate": 0.1,
            "crossover_rate": 0.8,
            "generations": 100,
            "eta_m": 20,
            "eta_c": 15
        })
        assert response.status_code == 422
    
    def test_reject_invalid_mutation_rate(self):
        """Mutation rate must be 0.0-1.0"""
        response = client.post("/api/genetic_algorithm", json={
            "function": "sphere",
            "pop_size": 50,
            "mutation_rate": 1.5,  # Invalid: > 1.0
            "crossover_rate": 0.8,
            "generations": 100,
            "eta_m": 20,
            "eta_c": 15
        })
        assert response.status_code == 422
    
    def test_reject_invalid_crossover_rate(self):
        """Crossover rate must be 0.0-1.0"""
        response = client.post("/api/genetic_algorithm", json={
            "function": "sphere",
            "pop_size": 50,
            "mutation_rate": 0.1,
            "crossover_rate": 1.5,  # Invalid: > 1.0
            "generations": 100,
            "eta_m": 20,
            "eta_c": 15
        })
        assert response.status_code == 422
    
    def test_reject_invalid_generations(self):
        """Generations must be 1-500"""
        response = client.post("/api/genetic_algorithm", json={
            "function": "sphere",
            "pop_size": 50,
            "mutation_rate": 0.1,
            "crossover_rate": 0.8,
            "generations": 1000,  # Invalid: > 500
            "eta_m": 20,
            "eta_c": 15
        })
        assert response.status_code == 422
    
    def test_reject_invalid_eta_m(self):
        """eta_m must be 1-50"""
        response = client.post("/api/genetic_algorithm", json={
            "function": "sphere",
            "pop_size": 50,
            "mutation_rate": 0.1,
            "crossover_rate": 0.8,
            "generations": 100,
            "eta_m": 100,  # Invalid: > 50
            "eta_c": 15
        })
        assert response.status_code == 422
    
    def test_reject_invalid_eta_c(self):
        """eta_c must be 1-50"""
        response = client.post("/api/genetic_algorithm", json={
            "function": "sphere",
            "pop_size": 50,
            "mutation_rate": 0.1,
            "crossover_rate": 0.8,
            "generations": 100,
            "eta_m": 20,
            "eta_c": 0  # Invalid: < 1
        })
        assert response.status_code == 422
    
    def test_accept_valid_ga_request(self):
        """Valid request should return 200"""
        response = client.post("/api/genetic_algorithm", json={
            "function": "sphere",
            "pop_size": 50,
            "mutation_rate": 0.1,
            "crossover_rate": 0.8,
            "generations": 100,
            "eta_m": 20,
            "eta_c": 15
        })
        assert response.status_code == 200
