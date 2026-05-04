import numpy as np
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.datasets import load_iris, load_breast_cancer, make_blobs
from sklearn.model_selection import train_test_split
from typing import Dict
from app.utils.tree_parser import tree_to_json, get_tree_depth, count_leaves


def load_dataset(dataset_name: str) -> tuple:
    """Load dataset based on name."""
    if dataset_name == "iris":
        data = load_iris()
        X, y = data.data, data.target
        feature_names = data.feature_names.tolist()
    elif dataset_name == "breast_cancer":
        data = load_breast_cancer()
        X, y = data.data, data.target
        feature_names = data.feature_names.tolist()
    elif dataset_name == "blobs":
        X, y = make_blobs(n_samples=300, centers=3, n_features=2, random_state=42)
        feature_names = ["x_0", "x_1"]
    else:
        raise ValueError(f"Unknown dataset: {dataset_name}")
    
    return X, y, feature_names


def run_decision_tree(
    task: str,
    criterion: str,
    max_depth: int,
    min_samples_split: int,
    min_samples_leaf: int,
    dataset: str
) -> dict:
    """Run decision tree algorithm."""
    
    # Load dataset
    X, y, feature_names = load_dataset(dataset)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Create and fit model
    if task == "classifier":
        model = DecisionTreeClassifier(
            criterion=criterion,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=42
        )
    else:
        model = DecisionTreeRegressor(
            criterion="squared_error" if criterion == "gini" else "absolute_error",
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=42
        )
    
    model.fit(X_train, y_train)
    
    # Calculate accuracy
    accuracy = model.score(X_test, y_test)
    
    # Convert tree to JSON
    tree_json = tree_to_json(model, feature_names, criterion)
    
    # Get tree metrics
    depth = get_tree_depth(tree_json)
    n_leaves = count_leaves(tree_json)
    
    # Get feature importances
    feature_importances = {}
    for name, importance in zip(feature_names, model.feature_importances_):
        feature_importances[name] = float(importance)
    
    return {
        "tree_json": tree_json,
        "accuracy": float(accuracy),
        "depth": depth,
        "n_leaves": n_leaves,
        "feature_importances": feature_importances
    }
