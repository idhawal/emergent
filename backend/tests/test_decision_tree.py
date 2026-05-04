import pytest
from app.services.tree_service import run_decision_tree
from app.utils.tree_parser import tree_to_json, get_tree_depth, count_leaves
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris


def test_tree_json_structure():
    """Validate tree_json has name, attributes, and children keys recursively."""
    data = load_iris()
    X, y = data.data, data.target
    feature_names = data.feature_names.tolist()
    
    clf = DecisionTreeClassifier(max_depth=3, random_state=42)
    clf.fit(X, y)
    
    tree_json = tree_to_json(clf, feature_names, "gini")
    
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
    feature_names = data.feature_names.tolist()
    
    clf = DecisionTreeClassifier(max_depth=3, random_state=42)
    clf.fit(X, y)
    
    tree_json = tree_to_json(clf, feature_names, "gini")
    
    depth = get_tree_depth(tree_json)
    leaves = count_leaves(tree_json)
    
    assert depth > 0, "Tree should have positive depth"
    assert leaves > 0, "Tree should have positive leaf count"
    assert depth <= 3, f"Tree depth should not exceed max_depth=3, got {depth}"


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
