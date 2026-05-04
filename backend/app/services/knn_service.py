import numpy as np
from sklearn.datasets import make_moons, make_circles, make_blobs
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from typing import Tuple, List, Optional


def generate_dataset(dataset_name: str, n_samples: int = 200) -> Tuple[np.ndarray, np.ndarray]:
    """Generate synthetic dataset based on name."""
    np.random.seed(42)
    
    if dataset_name == "moons":
        X, y = make_moons(n_samples=n_samples, noise=0.15, random_state=42)
    elif dataset_name == "circles":
        X, y = make_circles(n_samples=n_samples, noise=0.08, factor=0.5, random_state=42)
    elif dataset_name == "blobs":
        X, y = make_blobs(n_samples=n_samples, centers=3, random_state=42)
    elif dataset_name == "sine":
        X = np.linspace(-3, 3, n_samples).reshape(-1, 1)
        y = np.sin(X.flatten()) + np.random.normal(0, 0.2, n_samples)
    else:
        raise ValueError(f"Unknown dataset: {dataset_name}")
    
    return X, y


def compute_distance(a: np.ndarray, b: np.ndarray, metric: str) -> float:
    """Compute distance between two points."""
    if metric == "manhattan":
        return np.sum(np.abs(a - b))
    else:  # euclidean
        return np.sqrt(np.sum((a - b) ** 2))


def predict_knn(
    point: np.ndarray,
    X_train: np.ndarray,
    y_train: np.ndarray,
    k: int,
    metric: str,
    weights: str,
    task: str
) -> float:
    """Predict using KNN algorithm."""
    # Compute distances
    distances = []
    for i, x in enumerate(X_train):
        d = compute_distance(point, x, metric)
        distances.append((d, i, y_train[i]))
    
    # Sort by distance and get k nearest
    distances.sort(key=lambda x: x[0])
    k_nearest = distances[:k]
    
    if task == "classification":
        # Weighted voting
        if weights == "distance":
            votes = {}
            for d, idx, label in k_nearest:
                weight = 1.0 / (d + 1e-6)
                votes[label] = votes.get(label, 0) + weight
            return max(votes.items(), key=lambda x: x[1])[0]
        else:
            # Uniform voting
            labels = [label for _, _, label in k_nearest]
            return max(set(labels), key=labels.count)
    else:
        # Regression
        if weights == "distance":
            num = 0.0
            den = 0.0
            for d, idx, value in k_nearest:
                weight = 1.0 / (d + 1e-6)
                num += weight * value
                den += weight
            return num / den
        else:
            values = [value for _, _, value in k_nearest]
            return np.mean(values)


def generate_meshgrid(
    X_train: np.ndarray,
    y_train: np.ndarray,
    k: int,
    metric: str,
    weights: str,
    task: str,
    grid_size: int = 60
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate decision boundary meshgrid."""
    x_min, x_max = X_train[:, 0].min() - 0.6, X_train[:, 0].max() + 0.6
    y_min, y_max = X_train[:, 1].min() - 0.6, X_train[:, 1].max() + 0.6
    
    xx = np.linspace(x_min, x_max, grid_size)
    yy = np.linspace(y_min, y_max, grid_size)
    mesh_xx, mesh_yy = np.meshgrid(xx, yy)
    
    mesh_zz = np.zeros_like(mesh_xx)
    for i in range(grid_size):
        for j in range(grid_size):
            point = np.array([mesh_xx[i, j], mesh_yy[i, j]])
            mesh_zz[i, j] = predict_knn(point, X_train, y_train, k, metric, weights, task)
    
    return mesh_xx, mesh_yy, mesh_zz


def run_knn(
    k: int,
    metric: str,
    weights: str,
    task: str,
    dataset: str,
    test_point: Optional[List[float]] = None
) -> dict:
    """Run KNN algorithm."""
    
    # Generate dataset
    X_train, y_train = generate_dataset(dataset, n_samples=200)
    
    # Generate meshgrid for decision boundary
    mesh_xx, mesh_yy, mesh_zz = generate_meshgrid(
        X_train, y_train, k, metric, weights, task
    )
    
    # Handle test point
    neighbor_indices = []
    test_prediction = None
    
    if test_point is not None:
        test_point_arr = np.array(test_point)
        
        # Find k nearest neighbors
        distances = []
        for i, x in enumerate(X_train):
            d = compute_distance(test_point_arr, x, metric)
            distances.append((d, i))
        
        distances.sort(key=lambda x: x[0])
        neighbor_indices = [idx for _, idx in distances[:k]]
        
        # Make prediction
        test_prediction = predict_knn(
            test_point_arr, X_train, y_train, k, metric, weights, task
        )
    
    return {
        "train_points": X_train.tolist(),
        "train_labels": y_train.tolist(),
        "mesh_xx": mesh_xx.tolist(),
        "mesh_yy": mesh_yy.tolist(),
        "mesh_zz": mesh_zz.tolist(),
        "neighbor_indices": neighbor_indices,
        "test_prediction": test_prediction if test_prediction is not None else 0.0
    }
