import numpy as np
from typing import Tuple, Optional


def generate_synthetic_data(n_samples: int, noise: float, poly_degree: int = 4) -> Tuple[np.ndarray, np.ndarray]:
    """Generate synthetic 2D dataset with polynomial relationship."""
    np.random.seed(42)
    X = np.linspace(-3, 3, n_samples).reshape(-1, 1)
    
    # True polynomial coefficients
    true_coef = [1.5, -0.8, 0.4, -0.2]
    y = np.zeros(n_samples)
    for d in range(min(poly_degree + 1, len(true_coef))):
        y += true_coef[d] * (X ** d).flatten()
    
    # Add noise
    y += np.random.normal(0, noise, n_samples)
    
    return X, y


def create_polynomial_features(X: np.ndarray, degree: int) -> np.ndarray:
    """
    Create polynomial features from scratch.
    For X with shape (m, 1), creates [1, x, x^2, ..., x^degree]
    """
    m = X.shape[0]
    X_poly = np.ones((m, degree + 1))
    
    for d in range(1, degree + 1):
        X_poly[:, d] = (X[:, 0] ** d)
    
    return X_poly


def custom_gradient_descent(
    X: np.ndarray, 
    y: np.ndarray, 
    learning_rate: float, 
    epochs: int,
    early_stopping: bool = False
) -> Tuple[np.ndarray, list, Optional[int]]:
    """
    Custom gradient descent implementation from scratch using NumPy.
    Returns: coefficients, cost_history, stopped_at_epoch
    """
    m, n = X.shape
    theta = np.zeros(n)
    cost_history = []
    stopped_at_epoch = None
    
    # Add bias term
    X_b = np.c_[np.ones((m, 1)), X]
    theta = np.zeros(X_b.shape[1])
    
    consecutive_increases = 0
    
    for epoch in range(epochs):
        # Compute predictions
        predictions = X_b.dot(theta)
        
        # Compute cost (MSE)
        cost = (1 / (2 * m)) * np.sum((predictions - y) ** 2)
        cost_history.append(cost)
        
        # Early stopping check
        if early_stopping and epoch > 0:
            if cost > cost_history[-2]:
                consecutive_increases += 1
                if consecutive_increases >= 5:
                    stopped_at_epoch = epoch
                    break
            else:
                consecutive_increases = 0
        
        # Compute gradients
        gradients = (1 / m) * X_b.T.dot(predictions - y)
        
        # Update parameters
        theta = theta - learning_rate * gradients
    
    return theta, cost_history, stopped_at_epoch


def polynomial_gradient_descent(
    X: np.ndarray,
    y: np.ndarray,
    degree: int,
    learning_rate: float,
    epochs: int,
    early_stopping: bool = False
) -> Tuple[np.ndarray, list, Optional[int]]:
    """
    Polynomial regression using gradient descent from scratch.
    No sklearn used.
    """
    # Create polynomial features manually
    X_poly = create_polynomial_features(X, degree)
    
    m = X_poly.shape[0]
    theta = np.zeros(X_poly.shape[1])
    cost_history = []
    stopped_at_epoch = None
    consecutive_increases = 0
    
    for epoch in range(epochs):
        # Predictions
        predictions = X_poly.dot(theta)
        
        # Cost (MSE)
        cost = (1 / (2 * m)) * np.sum((predictions - y) ** 2)
        cost_history.append(cost)
        
        # Early stopping
        if early_stopping and epoch > 0:
            if cost > cost_history[-2]:
                consecutive_increases += 1
                if consecutive_increases >= 5:
                    stopped_at_epoch = epoch
                    break
            else:
                consecutive_increases = 0
        
        # Gradients
        gradients = (1 / m) * X_poly.T.dot(predictions - y)
        
        # Update
        theta = theta - learning_rate * gradients
    
    return theta, cost_history, stopped_at_epoch


def ridge_gradient_descent(
    X: np.ndarray,
    y: np.ndarray,
    degree: int,
    learning_rate: float,
    epochs: int,
    penalty: float,
    early_stopping: bool = False
) -> Tuple[np.ndarray, list, Optional[int]]:
    """
    Ridge regression (L2 regularization) using gradient descent from scratch.
    Cost: J(θ) = MSE + λ * Σ(θ_j^2)
    No sklearn used.
    """
    # Create polynomial features
    X_poly = create_polynomial_features(X, degree)
    
    m = X_poly.shape[0]
    theta = np.zeros(X_poly.shape[1])
    cost_history = []
    stopped_at_epoch = None
    consecutive_increases = 0
    
    for epoch in range(epochs):
        # Predictions
        predictions = X_poly.dot(theta)
        
        # Cost with L2 penalty (don't penalize bias term)
        mse = (1 / (2 * m)) * np.sum((predictions - y) ** 2)
        l2_penalty = (penalty / (2 * m)) * np.sum(theta[1:] ** 2)
        cost = mse + l2_penalty
        cost_history.append(cost)
        
        # Early stopping
        if early_stopping and epoch > 0:
            if cost > cost_history[-2]:
                consecutive_increases += 1
                if consecutive_increases >= 5:
                    stopped_at_epoch = epoch
                    break
            else:
                consecutive_increases = 0
        
        # Gradients with L2 penalty
        gradients = (1 / m) * X_poly.T.dot(predictions - y)
        # Add L2 penalty to gradients (except bias)
        gradients[1:] += (penalty / m) * theta[1:]
        
        # Update
        theta = theta - learning_rate * gradients
    
    return theta, cost_history, stopped_at_epoch


def soft_threshold(x: float, lambda_: float) -> float:
    """
    Soft thresholding operator for Lasso (proximal operator for L1 norm).
    """
    if x > lambda_:
        return x - lambda_
    elif x < -lambda_:
        return x + lambda_
    else:
        return 0.0


def lasso_coordinate_descent(
    X: np.ndarray,
    y: np.ndarray,
    degree: int,
    penalty: float,
    epochs: int,
    early_stopping: bool = False
) -> Tuple[np.ndarray, list, Optional[int]]:
    """
    Lasso regression (L1 regularization) using coordinate descent from scratch.
    Cost: J(θ) = MSE + λ * Σ|θ_j|
    No sklearn used.
    """
    # Create polynomial features
    X_poly = create_polynomial_features(X, degree)
    
    m, n = X_poly.shape
    theta = np.zeros(n)
    cost_history = []
    stopped_at_epoch = None
    consecutive_increases = 0
    
    # Precompute X^T X diagonal and X^T y
    XTX_diag = np.sum(X_poly ** 2, axis=0)
    XTy = X_poly.T.dot(y)
    
    for epoch in range(epochs):
        # Coordinate descent: update one coefficient at a time
        for j in range(n):
            # Compute residual without j-th feature
            residual = y - X_poly.dot(theta) + X_poly[:, j] * theta[j]
            
            # Compute rho_j = X_j^T * residual
            rho_j = X_poly[:, j].dot(residual)
            
            # Update theta_j using soft thresholding
            if j == 0:  # Don't penalize bias term
                theta[j] = rho_j / XTX_diag[j]
            else:
                theta[j] = soft_threshold(rho_j, penalty * m) / XTX_diag[j]
        
        # Compute cost
        predictions = X_poly.dot(theta)
        mse = (1 / (2 * m)) * np.sum((predictions - y) ** 2)
        l1_penalty = (penalty / m) * np.sum(np.abs(theta[1:]))
        cost = mse + l1_penalty
        cost_history.append(cost)
        
        # Early stopping
        if early_stopping and epoch > 0:
            if cost > cost_history[-2]:
                consecutive_increases += 1
                if consecutive_increases >= 5:
                    stopped_at_epoch = epoch
                    break
            else:
                consecutive_increases = 0
    
    return theta, cost_history, stopped_at_epoch


def elastic_net_coordinate_descent(
    X: np.ndarray,
    y: np.ndarray,
    degree: int,
    penalty: float,
    l1_ratio: float,
    epochs: int,
    early_stopping: bool = False
) -> Tuple[np.ndarray, list, Optional[int]]:
    """
    Elastic Net (L1 + L2 regularization) using coordinate descent from scratch.
    Cost: J(θ) = MSE + λ * [l1_ratio * Σ|θ_j| + (1-l1_ratio)/2 * Σ(θ_j^2)]
    No sklearn used.
    """
    # Create polynomial features
    X_poly = create_polynomial_features(X, degree)
    
    m, n = X_poly.shape
    theta = np.zeros(n)
    cost_history = []
    stopped_at_epoch = None
    consecutive_increases = 0
    
    # Precompute
    XTX_diag = np.sum(X_poly ** 2, axis=0)
    
    # Split penalty into L1 and L2 components
    lambda_1 = penalty * l1_ratio
    lambda_2 = penalty * (1 - l1_ratio)
    
    for epoch in range(epochs):
        # Coordinate descent
        for j in range(n):
            # Compute residual without j-th feature
            residual = y - X_poly.dot(theta) + X_poly[:, j] * theta[j]
            
            # Compute rho_j
            rho_j = X_poly[:, j].dot(residual)
            
            # Update with both L1 and L2 penalties
            if j == 0:  # Don't penalize bias
                theta[j] = rho_j / XTX_diag[j]
            else:
                # Soft thresholding with L2 adjustment
                denominator = XTX_diag[j] + lambda_2 * m
                theta[j] = soft_threshold(rho_j, lambda_1 * m) / denominator
        
        # Compute cost
        predictions = X_poly.dot(theta)
        mse = (1 / (2 * m)) * np.sum((predictions - y) ** 2)
        l1_penalty = (lambda_1 / m) * np.sum(np.abs(theta[1:]))
        l2_penalty = (lambda_2 / (2 * m)) * np.sum(theta[1:] ** 2)
        cost = mse + l1_penalty + l2_penalty
        cost_history.append(cost)
        
        # Early stopping
        if early_stopping and epoch > 0:
            if cost > cost_history[-2]:
                consecutive_increases += 1
                if consecutive_increases >= 5:
                    stopped_at_epoch = epoch
                    break
            else:
                consecutive_increases = 0
    
    return theta, cost_history, stopped_at_epoch


def run_regression(
    algo: str,
    learning_rate: float,
    epochs: int,
    poly_degree: int,
    penalty: float,
    l1_ratio: float,
    noise: float,
    early_stopping: bool,
    x_data: Optional[np.ndarray] = None,
    y_data: Optional[np.ndarray] = None,
) -> dict:
    """
    Run regression algorithm based on parameters.
    ALL ALGORITHMS IMPLEMENTED FROM SCRATCH - NO SKLEARN.
    """
    
    # Resolve dataset (uploaded/preset) if provided, otherwise synthetic fallback.
    if x_data is not None and y_data is not None:
        X = np.asarray(x_data, dtype=float).reshape(-1, 1)
        y = np.asarray(y_data, dtype=float)
    else:
        X, y = generate_synthetic_data(80, noise, poly_degree)
    
    coefficients = []
    cost_history = []
    stopped_at_epoch = None
    
    if algo == "linear_gd":
        # Linear regression with gradient descent
        theta, cost_history, stopped_at_epoch = custom_gradient_descent(
            X, y, learning_rate, epochs, early_stopping
        )
        coefficients = theta.tolist()
        feature_names = ["bias", "x"]
        
        # Generate curve for plotting
        curve_x = np.linspace(-3, 3, 200).reshape(-1, 1)
        curve_x_b = np.c_[np.ones((200, 1)), curve_x]
        curve_y = curve_x_b.dot(theta).tolist()
        
    elif algo == "polynomial":
        # Polynomial regression from scratch
        theta, cost_history, stopped_at_epoch = polynomial_gradient_descent(
            X, y, poly_degree, learning_rate, epochs, early_stopping
        )
        coefficients = theta.tolist()
        feature_names = [f"x^{i}" for i in range(poly_degree + 1)]
        
        # Generate curve
        curve_x = np.linspace(-3, 3, 200).reshape(-1, 1)
        curve_x_poly = create_polynomial_features(curve_x, poly_degree)
        curve_y = curve_x_poly.dot(theta).tolist()
        
    elif algo == "ridge":
        # Ridge regression from scratch
        theta, cost_history, stopped_at_epoch = ridge_gradient_descent(
            X, y, poly_degree, learning_rate, epochs, penalty, early_stopping
        )
        coefficients = theta.tolist()
        feature_names = [f"x^{i}" for i in range(poly_degree + 1)]
        
        # Generate curve
        curve_x = np.linspace(-3, 3, 200).reshape(-1, 1)
        curve_x_poly = create_polynomial_features(curve_x, poly_degree)
        curve_y = curve_x_poly.dot(theta).tolist()
        
    elif algo == "lasso":
        # Lasso regression from scratch
        theta, cost_history, stopped_at_epoch = lasso_coordinate_descent(
            X, y, poly_degree, penalty, epochs, early_stopping
        )
        coefficients = theta.tolist()
        feature_names = [f"x^{i}" for i in range(poly_degree + 1)]
        
        # Generate curve
        curve_x = np.linspace(-3, 3, 200).reshape(-1, 1)
        curve_x_poly = create_polynomial_features(curve_x, poly_degree)
        curve_y = curve_x_poly.dot(theta).tolist()
        
    elif algo == "elastic_net":
        # Elastic Net from scratch
        theta, cost_history, stopped_at_epoch = elastic_net_coordinate_descent(
            X, y, poly_degree, penalty, l1_ratio, epochs, early_stopping
        )
        coefficients = theta.tolist()
        feature_names = [f"x^{i}" for i in range(poly_degree + 1)]
        
        # Generate curve
        curve_x = np.linspace(-3, 3, 200).reshape(-1, 1)
        curve_x_poly = create_polynomial_features(curve_x, poly_degree)
        curve_y = curve_x_poly.dot(theta).tolist()
    
    return {
        "curve_x": curve_x.flatten().tolist() if hasattr(curve_x, 'flatten') else curve_x,
        "curve_y": curve_y,
        "scatter_x": X.flatten().tolist(),
        "scatter_y": y.tolist(),
        "cost_history": cost_history,
        "coefficients": coefficients,
        "feature_names": feature_names,
        "stopped_at_epoch": stopped_at_epoch
    }
