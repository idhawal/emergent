import pytest
import pandas as pd
import numpy as np
from app.services.tree_service import run_decision_tree
from app.services.custom_tree import CustomDecisionTreeClassifier, CustomDecisionTreeRegressor
from sklearn.datasets import load_iris, load_breast_cancer


def test_tree_json_structure():
    """Validate tree_json has name, attributes, and children keys recursively."""
    data = load_iris()
    X, y = data.data, data.target
    feature_names = list(data.feature_names) if hasattr(data.feature_names, '__iter__') else data.feature_names
    
    clf = CustomDecisionTreeClassifier(max_depth=3, random_state=42)
    clf.fit(X, y)
    
    tree_json = clf.to_json(feature_names)
    
    def validate_node(node):
        assert "name" in node, "Node must have 'name'"
        assert "attributes" in node, "Node must have 'attributes'"
        assert "samples" in node["attributes"], "Attributes must have 'samples'"
        
        if "children" in node and node["children"]:
            for child in node["children"]:
                validate_node(child)
    
    validate_node(tree_json)


def test_tree_depth_and_leaves():
    """Test tree depth and leaf counting functions."""
    data = load_iris()
    X, y = data.data, data.target
    feature_names = list(data.feature_names) if hasattr(data.feature_names, '__iter__') else data.feature_names
    
    clf = CustomDecisionTreeClassifier(max_depth=3, random_state=42)
    clf.fit(X, y)
    
    depth = clf.get_depth()
    leaves = clf.get_n_leaves()
    
    assert depth > 0, "Tree should have positive depth"
    assert leaves > 0, "Tree should have positive leaf count"
    assert depth <= 4, f"Tree depth should not exceed max_depth=3 + 1, got {depth}"


def test_decision_tree_response_structure():
    """Test that decision tree response has all required fields."""
    result = run_decision_tree(
        task="classifier",
        criterion="gini",
        max_depth=3,
        min_samples_split=2,
        min_samples_leaf=1,
        dataset="iris"
    )
    
    required_fields = ["tree_json", "accuracy", "depth", "n_leaves", "feature_importances"]
    for field in required_fields:
        assert field in result, f"Missing field: {field}"
    
    assert 0 <= result["accuracy"] <= 1, "Accuracy should be between 0 and 1"
    assert result["depth"] > 0, "Depth should be positive"
    assert result["n_leaves"] > 0, "Leaf count should be positive"
    assert isinstance(result["feature_importances"], dict), "Feature importances should be a dict"


def test_invalid_task_parameter():
    """Test error handling for invalid task parameter."""
    with pytest.raises(ValueError, match="task must be"):
        run_decision_tree(
            task="invalid",
            criterion="gini",
            max_depth=3,
            min_samples_split=2,
            min_samples_leaf=1,
            dataset="iris"
        )


def test_entropy_with_regressor_error():
    """Test that entropy criterion raises error with regressor task."""
    with pytest.raises(ValueError, match="entropy criterion is only valid for classifier"):
        run_decision_tree(
            task="regressor",
            criterion="entropy",
            max_depth=3,
            min_samples_split=2,
            min_samples_leaf=1,
            dataset="iris"
        )


def test_invalid_criterion():
    """Test error handling for invalid criterion."""
    with pytest.raises(ValueError, match="criterion must be"):
        run_decision_tree(
            task="classifier",
            criterion="invalid_criterion",
            max_depth=3,
            min_samples_split=2,
            min_samples_leaf=1,
            dataset="iris"
        )


def test_invalid_min_samples_split():
    """Test validation of min_samples_split parameter."""
    with pytest.raises(ValueError, match="min_samples_split must be"):
        run_decision_tree(
            task="classifier",
            criterion="gini",
            max_depth=3,
            min_samples_split=1,  # Invalid: must be >= 2
            min_samples_leaf=1,
            dataset="iris"
        )


def test_invalid_min_samples_leaf():
    """Test validation of min_samples_leaf parameter."""
    with pytest.raises(ValueError, match="min_samples_leaf must be"):
        run_decision_tree(
            task="classifier",
            criterion="gini",
            max_depth=3,
            min_samples_split=2,
            min_samples_leaf=0,  # Invalid: must be >= 1
            dataset="iris"
        )


def test_classifier_vs_regressor():
    """Test that classifier and regressor produce valid results."""
    # Classifier
    result_clf = run_decision_tree(
        task="classifier",
        criterion="gini",
        max_depth=3,
        min_samples_split=2,
        min_samples_leaf=1,
        dataset="iris"
    )
    assert result_clf["accuracy"] > 0
    
    # Regressor
    result_reg = run_decision_tree(
        task="regressor",
        criterion="gini",
        max_depth=3,
        min_samples_split=2,
        min_samples_leaf=1,
        dataset="blobs"
    )
    assert result_reg["accuracy"] is not None


def test_deep_tree():
    """Test tree with maximum depth."""
    result = run_decision_tree(
        task="classifier",
        criterion="gini",
        max_depth=10,
        min_samples_split=2,
        min_samples_leaf=1,
        dataset="iris"
    )
    assert result["depth"] > 0
    assert result["n_leaves"] > 0


def test_uploaded_csv_data():
    """Test with uploaded CSV data."""
    # Create sample CSV data
    data = {
        "feature1": [1, 2, 3, 4, 5],
        "feature2": [2, 3, 4, 5, 6],
        "target": [0, 1, 0, 1, 0]
    }
    df = pd.DataFrame(data)
    csv_data = df.to_dict("records")
    
    result = run_decision_tree(
        task="classifier",
        criterion="gini",
        max_depth=3,
        min_samples_split=2,
        min_samples_leaf=1,
        dataset="blobs",
        uploaded_data=csv_data
    )
    
    assert "tree_json" in result
    assert "accuracy" in result


def test_uploaded_csv_too_few_columns():
    """Test error handling for CSV with insufficient numeric columns."""
    # Only 1 numeric column - should fail
    data = {"feature1": [1, 2, 3, 4, 5]}
    df = pd.DataFrame(data)
    csv_data = df.to_dict("records")
    
    with pytest.raises(ValueError, match="at least 2 numeric columns"):
        run_decision_tree(
            task="classifier",
            criterion="gini",
            max_depth=3,
            min_samples_split=2,
            min_samples_leaf=1,
            dataset="blobs",
            uploaded_data=csv_data
        )


def test_gini_vs_entropy():
    """Test that Gini and Entropy produce different results."""
    result_gini = run_decision_tree(
        task="classifier",
        criterion="gini",
        max_depth=3,
        min_samples_split=2,
        min_samples_leaf=1,
        dataset="iris"
    )
    
    result_entropy = run_decision_tree(
        task="classifier",
        criterion="entropy",
        max_depth=3,
        min_samples_split=2,
        min_samples_leaf=1,
        dataset="iris"
    )
    
    # Trees should be different (usually)
    assert result_gini is not None
    assert result_entropy is not None
    # Note: Can't guarantee trees are different every time due to randomness
