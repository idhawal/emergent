import numpy as np
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
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


def run_regression(
    algo: str,
    learning_rate: float,
    epochs: int,
    poly_degree: int,
    penalty: float,
    l1_ratio: float,
    noise: float,
    early_stopping: bool
) -> dict:
    """Run regression algorithm based on parameters."""
    
    # Generate synthetic data
    X, y = generate_synthetic_data(80, noise, poly_degree)
    
    # Prepare polynomial features if needed
    if poly_degree > 1 or algo in ["polynomial", "ridge", "lasso", "elastic_net"]:
        poly = PolynomialFeatures(degree=poly_degree, include_bias=True)
        X_poly = poly.fit_transform(X)
        feature_names = [f"x^{i}" if i > 0 else "bias" for i in range(X_poly.shape[1])]
    else:
        X_poly = np.c_[np.ones((X.shape[0], 1)), X]
        feature_names = ["bias", "x"]
    
    coefficients = []
    cost_history = []
    stopped_at_epoch = None
    
    if algo == "linear_gd":
        # Custom gradient descent
        theta, cost_history, stopped_at_epoch = custom_gradient_descent(
            X, y, learning_rate, epochs, early_stopping
        )
        coefficients = theta.tolist()
        
        # Generate curve for plotting
        curve_x = np.linspace(-3, 3, 200).reshape(-1, 1)
        curve_x_b = np.c_[np.ones((200, 1)), curve_x]
        curve_y = curve_x_b.dot(theta).tolist()
        
    elif algo == "polynomial":
        # Polynomial regression using sklearn
        model = LinearRegression()
        model.fit(X_poly, y)
        coefficients = model.coef_.tolist()
        cost_history = [np.mean((model.predict(X_poly) - y) ** 2) / 2] * epochs
        
        # Generate curve
        curve_x = np.linspace(-3, 3, 200).reshape(-1, 1)
        curve_x_poly = poly.transform(curve_x)
        curve_y = model.predict(curve_x_poly).tolist()
        
    elif algo == "ridge":
        # Ridge regression
        model = Ridge(alpha=penalty)
        model.fit(X_poly, y)
        coefficients = model.coef_.tolist()
        cost_history = [np.mean((model.predict(X_poly) - y) ** 2) / 2] * epochs
        
        curve_x = np.linspace(-3, 3, 200).reshape(-1, 1)
        curve_x_poly = poly.transform(curve_x)
        curve_y = model.predict(curve_x_poly).tolist()
        
    elif algo == "lasso":
        # Lasso regression
        model = Lasso(alpha=penalty, max_iter=epochs)
        model.fit(X_poly, y)
        coefficients = model.coef_.tolist()
        cost_history = [np.mean((model.predict(X_poly) - y) ** 2) / 2] * epochs
        
        curve_x = np.linspace(-3, 3, 200).reshape(-1, 1)
        curve_x_poly = poly.transform(curve_x)
        curve_y = model.predict(curve_x_poly).tolist()
        
    elif algo == "elastic_net":
        # Elastic Net
        model = ElasticNet(alpha=penalty, l1_ratio=l1_ratio, max_iter=epochs)
        model.fit(X_poly, y)
        coefficients = model.coef_.tolist()
        cost_history = [np.mean((model.predict(X_poly) - y) ** 2) / 2] * epochs
        
        curve_x = np.linspace(-3, 3, 200).reshape(-1, 1)
        curve_x_poly = poly.transform(curve_x)
        curve_y = model.predict(curve_x_poly).tolist()
    
    return {
        "curve_x": curve_x,
        "curve_y": curve_y,
        "scatter_x": X.flatten().tolist(),
        "scatter_y": y.tolist(),
        "cost_history": cost_history,
        "coefficients": coefficients,
        "feature_names": feature_names,
        "stopped_at_epoch": stopped_at_epoch
    }
