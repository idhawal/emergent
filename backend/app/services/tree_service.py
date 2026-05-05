import numpy as np
import pandas as pd
from sklearn.datasets import load_iris, load_breast_cancer, make_blobs
from sklearn.model_selection import train_test_split
from typing import Dict, Optional, List
from app.services.custom_tree import CustomDecisionTreeClassifier, CustomDecisionTreeRegressor


def load_dataset(dataset_name: str) -> tuple:
    """Load dataset based on name."""
    if dataset_name == "iris":
        data = load_iris()
        X, y = data.data, data.target
        feature_names = data.feature_names if isinstance(data.feature_names, list) else data.feature_names.tolist()
    elif dataset_name == "breast_cancer":
        data = load_breast_cancer()
        X, y = data.data, data.target
        feature_names = data.feature_names if isinstance(data.feature_names, list) else data.feature_names.tolist()
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
    dataset: str,
    uploaded_data: Optional[List[dict]] = None,
) -> dict:
    """
    Run decision tree algorithm.
    IMPLEMENTED FROM SCRATCH - NO SKLEARN TREE USED.
    """
    
    if uploaded_data:
        df = pd.DataFrame(uploaded_data)
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if len(numeric_cols) < 2:
            raise ValueError("Uploaded CSV for decision tree must include at least 2 numeric columns.")
        feature_cols = numeric_cols[:-1]
        target_col = numeric_cols[-1]
        X = df[feature_cols].to_numpy(dtype=float)
        y = df[target_col].to_numpy(dtype=float)
        feature_names = feature_cols
    else:
        X, y, feature_names = load_dataset(dataset)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Create and fit model using CUSTOM implementation
    if task == "classifier":
        model = CustomDecisionTreeClassifier(
            criterion=criterion,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=42
        )
    else:
        model = CustomDecisionTreeRegressor(
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=42
        )
    
    model.fit(X_train, y_train)
    
    # Calculate accuracy/score
    accuracy = model.score(X_test, y_test)
    
    # Convert tree to JSON using custom method
    tree_json = model.to_json(feature_names)
    
    # Get tree metrics using custom methods
    depth = model.get_depth()
    n_leaves = model.get_n_leaves()
    
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
