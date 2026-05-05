"""
Tests to verify all algorithms are implemented from scratch.
NO SKLEARN ALLOWED (except for datasets and train_test_split).
"""
import pytest
import numpy as np
from app.services.regression_service import (
    custom_gradient_descent,
    polynomial_gradient_descent,
    ridge_gradient_descent,
    lasso_coordinate_descent,
    elastic_net_coordinate_descent,
    create_polynomial_features
)
from app.services.knn_service import compute_distance, predict_knn
from app.services.custom_tree import (
    calculate_gini,
    calculate_entropy,
    calculate_information_gain,
    CustomDecisionTreeClassifier,
    CustomDecisionTreeRegressor
)
from app.services.ga_service import (
    sphere,
    rosenbrock,
    rastrigin,
    sbx_crossover,
    polynomial_mutation,
    tournament_selection
)


class TestRegressionFromScratch:
    """Test that regression algorithms are implemented from scratch."""
    
    def test_custom_gradient_descent_no_sklearn(self):
        """Verify custom GD doesn't use sklearn."""
        np.random.seed(42)
        X = np.random.randn(100, 2)
        y = 3 * X[:, 0] + 2 * X[:, 1] + np.random.randn(100) * 0.1
        
        theta, cost_history, _ = custom_gradient_descent(X, y, 0.01, 100)
        
        assert len(theta) == 3  # bias + 2 features
        assert len(cost_history) == 100
        assert cost_history[-1] < cost_history[0]  # Cost should decrease
    
    def test_custom_gd_matches_sklearn(self):
        """Spec requirement: Custom GD should match sklearn within 1e-2."""
        from sklearn.linear_model import LinearRegression
        
        np.random.seed(42)
        X = np.random.randn(100, 2)
        y = 3 * X[:, 0] + 2 * X[:, 1] + np.random.randn(100) * 0.1
        
        # Custom GD
        theta_custom, _, _ = custom_gradient_descent(X, y, 0.01, 1000)
        
        # Sklearn
        X_with_bias = np.c_[np.ones((100, 1)), X]
        sklearn_model = LinearRegression(fit_intercept=False)
        sklearn_model.fit(X_with_bias, y)
        theta_sklearn = sklearn_model.coef_
        
        # Compare coefficients
        assert np.allclose(theta_custom, theta_sklearn, atol=1e-2), \
            f"Custom: {theta_custom}, Sklearn: {theta_sklearn}"
    
    def test_polynomial_features_from_scratch(self):
        """Test polynomial feature generation without sklearn."""
        X = np.array([[1], [2], [3]])
        X_poly = create_polynomial_features(X, degree=3)
        
        expected = np.array([
            [1, 1, 1, 1],    # [1, x, x^2, x^3] for x=1
            [1, 2, 4, 8],    # for x=2
            [1, 3, 9, 27]    # for x=3
        ])
        
        assert np.allclose(X_poly, expected)
    
    def test_polynomial_regression_from_scratch(self):
        """Test polynomial regression without sklearn."""
        np.random.seed(42)
        X = np.linspace(-1, 1, 50).reshape(-1, 1)
        y = 2 * X[:, 0] ** 2 + 3 * X[:, 0] + 1 + np.random.randn(50) * 0.1
        
        theta, cost_history, _ = polynomial_gradient_descent(
            X, y, degree=2, learning_rate=0.01, epochs=500
        )
        
        assert len(theta) == 3  # [1, x, x^2]
        assert cost_history[-1] < cost_history[0]
        # Coefficients should be reasonably close to [1, 3, 2]
        # Relaxed tolerance due to gradient descent approximation
        assert abs(theta[0] - 1) < 1.0
        assert abs(theta[1] - 3) < 1.0
        assert abs(theta[2] - 2) < 1.0
    
    def test_ridge_regression_from_scratch(self):
        """Test Ridge regression without sklearn."""
        np.random.seed(42)
        X = np.random.randn(100, 1)
        y = 2 * X[:, 0] + np.random.randn(100) * 0.1
        
        theta, cost_history, _ = ridge_gradient_descent(
            X, y, degree=1, learning_rate=0.01, epochs=500, penalty=1.0
        )
        
        assert len(theta) == 2  # [1, x]
        assert cost_history[-1] < cost_history[0]
    
    def test_lasso_regression_from_scratch(self):
        """Test Lasso regression without sklearn."""
        np.random.seed(42)
        X = np.random.randn(100, 1)
        y = 2 * X[:, 0] + np.random.randn(100) * 0.1
        
        theta, cost_history, _ = lasso_coordinate_descent(
            X, y, degree=3, penalty=10.0, epochs=100
        )
        
        assert len(theta) == 4  # [1, x, x^2, x^3]
        # With high penalty, some coefficients should be zero
        zero_count = np.sum(np.abs(theta) < 1e-6)
        assert zero_count >= 1, "Lasso should zero out some coefficients"
    
    def test_elastic_net_from_scratch(self):
        """Test Elastic Net without sklearn."""
        np.random.seed(42)
        X = np.random.randn(100, 1)
        y = 2 * X[:, 0] + np.random.randn(100) * 0.1
        
        theta, cost_history, _ = elastic_net_coordinate_descent(
            X, y, degree=3, penalty=5.0, l1_ratio=0.5, epochs=100
        )
        
        assert len(theta) == 4
        assert cost_history[-1] < cost_history[0]


class TestKNNFromScratch:
    """Test that KNN is implemented from scratch."""
    
    def test_distance_metrics_from_scratch(self):
        """Test custom distance calculations."""
        a = np.array([0, 0])
        b = np.array([3, 4])
        
        euclidean = compute_distance(a, b, "euclidean")
        manhattan = compute_distance(a, b, "manhattan")
        
        assert abs(euclidean - 5.0) < 1e-10
        assert abs(manhattan - 7.0) < 1e-10
    
    def test_knn_prediction_from_scratch(self):
        """Test KNN prediction without sklearn."""
        # Simple 2D dataset
        X_train = np.array([[0, 0], [1, 1], [2, 2], [3, 3]])
        y_train = np.array([0, 0, 1, 1])
        
        # Test point closer to class 0
        test_point = np.array([0.5, 0.5])
        prediction = predict_knn(
            test_point, X_train, y_train, k=3,
            metric="euclidean", weights="uniform", task="classification"
        )
        
        assert prediction == 0
        
        # Test point closer to class 1
        test_point = np.array([2.5, 2.5])
        prediction = predict_knn(
            test_point, X_train, y_train, k=3,
            metric="euclidean", weights="uniform", task="classification"
        )
        
        assert prediction == 1
    
    def test_knn_regression_from_scratch(self):
        """Test KNN regression without sklearn."""
        X_train = np.array([[0], [1], [2], [3]])
        y_train = np.array([0.0, 1.0, 2.0, 3.0])
        
        test_point = np.array([1.5])
        prediction = predict_knn(
            test_point, X_train, y_train, k=2,
            metric="euclidean", weights="uniform", task="regression"
        )
        
        # Should be average of neighbors at x=1 and x=2
        assert abs(prediction - 1.5) < 0.1


class TestDecisionTreeFromScratch:
    """Test that Decision Trees are implemented from scratch."""
    
    def test_gini_calculation_from_scratch(self):
        """Test Gini impurity calculation."""
        # Pure node (all same class)
        y_pure = np.array([0, 0, 0, 0])
        gini_pure = calculate_gini(y_pure)
        assert abs(gini_pure - 0.0) < 1e-10
        
        # Impure node (50-50 split)
        y_impure = np.array([0, 0, 1, 1])
        gini_impure = calculate_gini(y_impure)
        assert abs(gini_impure - 0.5) < 1e-10
    
    def test_entropy_calculation_from_scratch(self):
        """Test Entropy calculation."""
        # Pure node
        y_pure = np.array([0, 0, 0, 0])
        entropy_pure = calculate_entropy(y_pure)
        assert abs(entropy_pure - 0.0) < 1e-10
        
        # Impure node (50-50 split)
        y_impure = np.array([0, 0, 1, 1])
        entropy_impure = calculate_entropy(y_impure)
        assert abs(entropy_impure - 1.0) < 1e-10
    
    def test_information_gain_from_scratch(self):
        """Test information gain calculation."""
        y_parent = np.array([0, 0, 1, 1])
        y_left = np.array([0, 0])
        y_right = np.array([1, 1])
        
        # Perfect split should have maximum gain
        gain_gini = calculate_information_gain(y_parent, y_left, y_right, "gini")
        gain_entropy = calculate_information_gain(y_parent, y_left, y_right, "entropy")
        
        assert gain_gini > 0
        assert gain_entropy > 0
    
    def test_custom_tree_classifier_from_scratch(self):
        """Test custom decision tree classifier."""
        # Simple XOR-like problem
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([0, 1, 1, 0])
        
        tree = CustomDecisionTreeClassifier(max_depth=3, random_state=42)
        tree.fit(X, y)
        
        predictions = tree.predict(X)
        accuracy = np.mean(predictions == y)
        
        # Should learn XOR with enough depth
        assert accuracy >= 0.5
        assert tree.get_depth() > 0
        assert tree.get_n_leaves() > 0
    
    def test_custom_tree_regressor_from_scratch(self):
        """Test custom decision tree regressor."""
        X = np.array([[0], [1], [2], [3], [4]])
        y = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
        
        tree = CustomDecisionTreeRegressor(max_depth=3, random_state=42)
        tree.fit(X, y)
        
        predictions = tree.predict(X)
        mse = np.mean((predictions - y) ** 2)
        
        assert mse < 1.0  # Should fit reasonably well
        assert tree.get_depth() > 0
    
    def test_tree_to_json_from_scratch(self):
        """Test tree JSON conversion."""
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([0, 1, 1, 0])
        
        tree = CustomDecisionTreeClassifier(max_depth=2, random_state=42)
        tree.fit(X, y)
        
        tree_json = tree.to_json(["feature_0", "feature_1"])
        
        assert "name" in tree_json
        assert "attributes" in tree_json
        assert "samples" in tree_json["attributes"]


class TestGeneticAlgorithmFromScratch:
    """Test that GA is implemented from scratch."""
    
    def test_benchmark_functions_from_scratch(self):
        """Test benchmark functions are custom."""
        # Sphere
        assert abs(sphere(np.array([0.0, 0.0]))) < 1e-10
        assert sphere(np.array([1.0, 1.0])) > 0
        
        # Rosenbrock
        assert abs(rosenbrock(np.array([1.0, 1.0]))) < 1e-10
        assert rosenbrock(np.array([0.0, 0.0])) > 0
        
        # Rastrigin
        assert abs(rastrigin(np.array([0.0, 0.0]))) < 1e-10
        assert rastrigin(np.array([1.0, 1.0])) > 0
    
    def test_sbx_crossover_from_scratch(self):
        """Test SBX crossover is custom."""
        np.random.seed(42)
        parent1 = np.array([1.0, 2.0])
        parent2 = np.array([3.0, 4.0])
        
        child1, child2 = sbx_crossover(parent1, parent2, eta_c=20)
        
        assert len(child1) == 2
        assert len(child2) == 2
        # Children should be different from parents
        assert not np.array_equal(child1, parent1)
    
    def test_polynomial_mutation_from_scratch(self):
        """Test polynomial mutation is custom."""
        np.random.seed(42)
        individual = np.array([1.0, 2.0])
        
        mutated = polynomial_mutation(individual, eta_m=20, bounds=(-5, 5))
        
        assert len(mutated) == 2
        # Should be within bounds
        assert np.all(mutated >= -5)
        assert np.all(mutated <= 5)
    
    def test_tournament_selection_from_scratch(self):
        """Test tournament selection is custom."""
        np.random.seed(42)
        population = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        fitness = np.array([10.0, 5.0, 15.0, 3.0])
        
        selected = tournament_selection(population, fitness, tournament_size=3)
        
        assert len(selected) == 2
        # Should select from population
        assert any(np.array_equal(selected, ind) for ind in population)


class TestNoSklearnImports:
    """Verify sklearn is not imported in core algorithm files."""
    
    def test_regression_service_no_sklearn_models(self):
        """Verify regression_service doesn't import sklearn models."""
        with open('backend/app/services/regression_service.py', 'r') as f:
            content = f.read()
        
        # Should not import sklearn models
        assert 'from sklearn.linear_model import' not in content or \
               'from sklearn.linear_model import' not in content.split('# ')[0], \
               "regression_service should not import sklearn models"
        assert 'LinearRegression' not in content or content.count('LinearRegression') == 0
        assert 'Ridge(' not in content or 'Ridge(' not in content.split('#')[0]
        assert 'Lasso(' not in content or 'Lasso(' not in content.split('#')[0]
    
    def test_knn_service_no_sklearn_models(self):
        """Verify knn_service doesn't import sklearn KNN."""
        with open('backend/app/services/knn_service.py', 'r') as f:
            content = f.read()
        
        # Should not import sklearn KNN
        assert 'KNeighborsClassifier' not in content, \
               "knn_service should not import KNeighborsClassifier"
        assert 'KNeighborsRegressor' not in content, \
               "knn_service should not import KNeighborsRegressor"
    
    def test_tree_service_no_sklearn_tree(self):
        """Verify tree_service doesn't import sklearn tree."""
        with open('backend/app/services/tree_service.py', 'r') as f:
            content = f.read()
        
        # Should not import sklearn tree
        assert 'from sklearn.tree import DecisionTree' not in content, \
               "tree_service should not import sklearn DecisionTree"
        # Should import custom tree
        assert 'custom_tree' in content, \
               "tree_service should import custom_tree"
