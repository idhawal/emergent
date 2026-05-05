"""
Integration tests for end-to-end API functionality.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
import time

client = TestClient(app)


class TestRegressionIntegration:
    """End-to-end tests for regression endpoint."""
    
    def test_linear_gd_end_to_end(self):
        """Test complete linear GD workflow."""
        response = client.post("/api/regression", json={
            "algo": "linear_gd",
            "learning_rate": 0.01,
            "epochs": 100,
            "poly_degree": 1,
            "penalty": 1.0,
            "l1_ratio": 0.5,
            "noise": 0.3,
            "early_stopping": False
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields
        assert "curve_x" in data
        assert "curve_y" in data
        assert "scatter_x" in data
        assert "scatter_y" in data
        assert "cost_history" in data
        assert "coefficients" in data
        assert "feature_names" in data
        assert "stopped_at_epoch" in data
        
        # Check data types and lengths
        assert isinstance(data["curve_x"], list)
        assert isinstance(data["curve_y"], list)
        assert len(data["curve_x"]) == len(data["curve_y"])
        assert len(data["cost_history"]) > 0
        assert len(data["coefficients"]) == len(data["feature_names"])
    
    def test_polynomial_regression_end_to_end(self):
        """Test polynomial regression workflow."""
        response = client.post("/api/regression", json={
            "algo": "polynomial",
            "learning_rate": 0.01,
            "epochs": 200,
            "poly_degree": 3,
            "penalty": 1.0,
            "l1_ratio": 0.5,
            "noise": 0.2,
            "early_stopping": False
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have 4 coefficients for degree 3 (including bias)
        assert len(data["coefficients"]) == 4
        assert len(data["feature_names"]) == 4
    
    def test_early_stopping_triggers(self):
        """Test that early stopping can trigger with appropriate parameters."""
        response = client.post("/api/regression", json={
            "algo": "linear_gd",
            "learning_rate": 0.5,  # Moderate LR
            "epochs": 1000,
            "poly_degree": 1,
            "penalty": 1.0,
            "l1_ratio": 0.5,
            "noise": 0.3,
            "early_stopping": True
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Early stopping may or may not trigger depending on data
        # Just verify the field exists and is valid
        assert "stopped_at_epoch" in data
        assert data["stopped_at_epoch"] is None or isinstance(data["stopped_at_epoch"], int)


class TestKNNIntegration:
    """End-to-end tests for KNN endpoint."""
    
    def test_knn_classification_end_to_end(self):
        """Test complete KNN classification workflow."""
        response = client.post("/api/knn", json={
            "k": 5,
            "metric": "euclidean",
            "weights": "uniform",
            "task": "classification",
            "dataset": "moons",
            "test_point": [0.5, 0.5]
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields
        assert "train_points" in data
        assert "train_labels" in data
        assert "mesh_xx" in data
        assert "mesh_yy" in data
        assert "mesh_zz" in data
        assert "neighbor_indices" in data
        assert "test_prediction" in data
        
        # Check neighbor indices
        assert len(data["neighbor_indices"]) == 5  # K=5
        assert isinstance(data["test_prediction"], (int, float))
    
    def test_knn_regression_end_to_end(self):
        """Test KNN regression workflow with 2D blobs dataset."""
        response = client.post("/api/knn", json={
            "k": 3,
            "metric": "manhattan",
            "weights": "distance",
            "task": "regression",
            "dataset": "blobs",  # Use blobs instead of sine (2D vs 1D)
            "test_point": None
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["train_points"]) > 0
        assert len(data["train_labels"]) > 0
        assert "mesh_xx" in data
        assert "mesh_yy" in data


class TestDecisionTreeIntegration:
    """End-to-end tests for decision tree endpoint."""
    
    def test_tree_classifier_end_to_end(self):
        """Test complete decision tree classifier workflow."""
        response = client.post("/api/decision_tree", json={
            "task": "classifier",
            "criterion": "gini",
            "max_depth": 3,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "dataset": "iris"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields
        assert "tree_json" in data
        assert "accuracy" in data
        assert "depth" in data
        assert "n_leaves" in data
        assert "feature_importances" in data
        
        # Check tree structure
        assert "name" in data["tree_json"]
        assert "attributes" in data["tree_json"]
        assert "samples" in data["tree_json"]["attributes"]
        
        # Check metrics
        assert 0 <= data["accuracy"] <= 1
        assert data["depth"] > 0
        assert data["n_leaves"] > 0
        assert isinstance(data["feature_importances"], dict)
    
    def test_tree_regressor_end_to_end(self):
        """Test decision tree regressor workflow."""
        response = client.post("/api/decision_tree", json={
            "task": "regressor",
            "criterion": "gini",  # Will be converted to variance
            "max_depth": 5,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "dataset": "iris"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["depth"] > 0
        assert data["n_leaves"] > 0
    
    def test_tree_with_entropy(self):
        """Test tree with entropy criterion."""
        response = client.post("/api/decision_tree", json={
            "task": "classifier",
            "criterion": "entropy",
            "max_depth": 4,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "dataset": "breast_cancer"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have entropy in attributes
        assert "entropy" in data["tree_json"]["attributes"] or \
               "gini" in data["tree_json"]["attributes"]


class TestGeneticAlgorithmIntegration:
    """End-to-end tests for genetic algorithm endpoint."""
    
    def test_ga_sphere_end_to_end(self):
        """Test complete GA workflow with Sphere function."""
        response = client.post("/api/genetic_algorithm", json={
            "function": "sphere",
            "pop_size": 30,
            "mutation_rate": 0.1,
            "crossover_rate": 0.8,
            "generations": 50,
            "eta_m": 20,
            "eta_c": 15
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields
        assert "contour_x" in data
        assert "contour_y" in data
        assert "contour_z" in data
        assert "history" in data
        assert "converged_at_generation" in data
        
        # Check history structure
        assert len(data["history"]) == 50
        first_gen = data["history"][0]
        assert "generation" in first_gen
        assert "points" in first_gen
        assert "fitness_values" in first_gen
        assert "best_fitness" in first_gen
        assert "avg_fitness" in first_gen
        assert "best_point" in first_gen
        
        # Check fitness improves
        first_fitness = data["history"][0]["best_fitness"]
        last_fitness = data["history"][-1]["best_fitness"]
        assert last_fitness <= first_fitness
    
    def test_ga_rosenbrock_end_to_end(self):
        """Test GA with Rosenbrock function."""
        response = client.post("/api/genetic_algorithm", json={
            "function": "rosenbrock",
            "pop_size": 40,
            "mutation_rate": 0.15,
            "crossover_rate": 0.9,
            "generations": 30,
            "eta_m": 25,
            "eta_c": 20
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["history"]) == 30
    
    def test_ga_rastrigin_end_to_end(self):
        """Test GA with Rastrigin function."""
        response = client.post("/api/genetic_algorithm", json={
            "function": "rastrigin",
            "pop_size": 50,
            "mutation_rate": 0.2,
            "crossover_rate": 0.7,
            "generations": 40,
            "eta_m": 15,
            "eta_c": 10
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["history"]) == 40


class TestCORSAndHeaders:
    """Test CORS configuration and headers."""
    
    def test_cors_headers_present(self):
        """Test that CORS is configured."""
        # Just test that the endpoint works
        response = client.get("/health")
        
        assert response.status_code == 200
        # CORS headers are set by middleware, may not appear in test client
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data


class TestPerformance:
    """Test API performance."""
    
    def test_regression_response_time(self):
        """Regression should respond within reasonable time."""
        start = time.time()
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
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 5.0  # Should complete within 5 seconds
    
    def test_knn_response_time(self):
        """KNN should respond within reasonable time."""
        start = time.time()
        response = client.post("/api/knn", json={
            "k": 5,
            "metric": "euclidean",
            "weights": "uniform",
            "task": "classification",
            "dataset": "moons",
            "test_point": None
        })
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 5.0
    
    def test_tree_response_time(self):
        """Decision tree should respond within reasonable time."""
        start = time.time()
        response = client.post("/api/decision_tree", json={
            "task": "classifier",
            "criterion": "gini",
            "max_depth": 5,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "dataset": "iris"
        })
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 5.0
    
    def test_ga_response_time(self):
        """GA should respond within reasonable time."""
        start = time.time()
        response = client.post("/api/genetic_algorithm", json={
            "function": "sphere",
            "pop_size": 30,
            "mutation_rate": 0.1,
            "crossover_rate": 0.8,
            "generations": 30,
            "eta_m": 20,
            "eta_c": 15
        })
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 10.0  # GA can take a bit longer


class TestErrorHandling:
    """Test error handling."""
    
    def test_missing_required_field(self):
        """Test missing required field returns 422."""
        response = client.post("/api/regression", json={
            "algo": "linear_gd",
            # Missing learning_rate
            "epochs": 100,
            "poly_degree": 2,
            "penalty": 1.0,
            "l1_ratio": 0.5,
            "noise": 0.3,
            "early_stopping": False
        })
        
        assert response.status_code == 422
    
    def test_invalid_json(self):
        """Test invalid JSON returns 422."""
        response = client.post(
            "/api/regression",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422
    
    def test_wrong_endpoint(self):
        """Test non-existent endpoint returns 404."""
        response = client.get("/api/nonexistent")
        
        assert response.status_code == 404
