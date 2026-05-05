import numpy as np
import pandas as pd
import logging
from sklearn.datasets import load_iris, load_breast_cancer, make_blobs
from sklearn.model_selection import train_test_split
from typing import Dict, Optional, List, Literal, Tuple
from app.services.custom_tree import CustomDecisionTreeClassifier, CustomDecisionTreeRegressor

# Configure logger for this module
logger = logging.getLogger(__name__)


def load_dataset(dataset_name: str) -> tuple:
    """
    Load dataset based on name.
    
    Args:
        dataset_name: Name of the dataset ("iris", "breast_cancer", or "blobs")
        
    Returns:
        Tuple of (X, y, feature_names) where X is features, y is target, feature_names are column names
        
    Raises:
        ValueError: If dataset_name is not recognized
    """
    logger.info(f"Loading dataset: {dataset_name}")
    
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
        logger.error(f"Unknown dataset requested: {dataset_name}")
        raise ValueError(f"Unknown dataset: {dataset_name}")
    
    logger.debug(f"Dataset loaded: {X.shape[0]} samples, {X.shape[1]} features")
    return X, y, feature_names


def run_decision_tree(
    task: Literal["classifier", "regressor"],
    criterion: Literal["gini", "entropy"],
    max_depth: Optional[int],
    min_samples_split: int,
    min_samples_leaf: int,
    dataset: str,
    uploaded_data: Optional[List[dict]] = None,
) -> dict:
    """
    Run decision tree algorithm with comprehensive error handling and validation.
    
    IMPLEMENTED FROM SCRATCH - NO SKLEARN TREE USED.
    
    Args:
        task: "classifier" or "regressor" - determines which tree model to use
        criterion: "gini" or "entropy" - splitting criterion (entropy only for classifier)
        max_depth: Maximum tree depth or None for unlimited
        min_samples_split: Minimum samples to split a node (≥ 2)
        min_samples_leaf: Minimum samples in leaf node (≥ 1)
        dataset: Built-in dataset name ("iris", "breast_cancer", "blobs")
        uploaded_data: Optional CSV data as list of dictionaries
        
    Returns:
        Dictionary with keys:
        - tree_json: Tree structure in JSON format
        - accuracy: Model accuracy on test set
        - depth: Tree depth
        - n_leaves: Number of leaf nodes
        - feature_importances: Dict of feature importance scores
        
    Raises:
        ValueError: If input validation fails or data issues occur
    """
    
    # Input validation
    if task not in ("classifier", "regressor"):
        logger.error(f"Invalid task: {task}")
        raise ValueError(f"task must be 'classifier' or 'regressor', got {task}")
    
    if task == "regressor" and criterion == "entropy":
        logger.error("entropy criterion not valid for regressor task")
        raise ValueError("entropy criterion is only valid for classifier task")
    
    if criterion not in ("gini", "entropy"):
        logger.error(f"Invalid criterion: {criterion}")
        raise ValueError(f"criterion must be 'gini' or 'entropy', got {criterion}")
    
    if min_samples_split < 2:
        raise ValueError(f"min_samples_split must be ≥ 2, got {min_samples_split}")
    
    if min_samples_leaf < 1:
        raise ValueError(f"min_samples_leaf must be ≥ 1, got {min_samples_leaf}")
    
    logger.info(f"Running decision tree: task={task}, criterion={criterion}, "
                f"max_depth={max_depth}, dataset={dataset}")
    
    try:
        # Load or validate data
        if uploaded_data:
            logger.info(f"Processing uploaded CSV with {len(uploaded_data)} rows")
            df = pd.DataFrame(uploaded_data)
            
            # Handle missing values
            if df.isnull().any().any():
                logger.warning("Uploaded data contains NaN values - filling with mean")
                numeric_cols = df.select_dtypes(include="number").columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            if len(numeric_cols) < 2:
                raise ValueError(
                    f"Uploaded CSV must have at least 2 numeric columns, found {len(numeric_cols)}"
                )
            
            feature_cols = numeric_cols[:-1]
            target_col = numeric_cols[-1]
            X = df[feature_cols].to_numpy(dtype=float)
            y = df[target_col].to_numpy(dtype=float)
            feature_names = feature_cols
            logger.info(f"Processed {X.shape[0]} samples with {X.shape[1]} features")
        else:
            X, y, feature_names = load_dataset(dataset)
        
        # Split data
        if len(X) < 10:
            logger.warning(f"Small dataset ({len(X)} samples) may produce unreliable results")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Create and fit model using CUSTOM implementation
        logger.debug(f"Creating {task} model with criterion={criterion}")
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
        logger.debug("Model training complete")
        
        # Calculate accuracy/score
        accuracy = model.score(X_test, y_test)
        logger.info(f"Model accuracy: {accuracy:.4f}")
        
        # Convert tree to JSON using custom method
        tree_json = model.to_json(feature_names)
        
        # Get tree metrics using custom methods
        depth = model.get_depth()
        n_leaves = model.get_n_leaves()
        logger.info(f"Tree metrics: depth={depth}, leaves={n_leaves}")
        
        # Get feature importances
        feature_importances = {}
        for name, importance in zip(feature_names, model.feature_importances_):
            feature_importances[name] = float(importance)
        
        result = {
            "tree_json": tree_json,
            "accuracy": float(accuracy),
            "depth": depth,
            "n_leaves": n_leaves,
            "feature_importances": feature_importances
        }
        
        logger.info("Decision tree execution completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in run_decision_tree: {str(e)}", exc_info=True)
        raise
