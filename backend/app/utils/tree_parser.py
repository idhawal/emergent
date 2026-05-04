import numpy as np
from sklearn.tree import _tree
from typing import Dict, Any


def tree_to_json(clf, feature_names: list, criterion: str) -> Dict[str, Any]:
    """
    Convert sklearn tree to JSON format compatible with react-d3-tree.
    
    Args:
        clf: Fitted sklearn DecisionTreeClassifier or DecisionTreeRegressor
        feature_names: List of feature names
        criterion: 'gini' or 'entropy'
    
    Returns:
        Nested dictionary representing the tree structure
    """
    tree_ = clf.tree_
    
    def recurse(node: int) -> Dict[str, Any]:
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            # Internal node
            name = f"{feature_names[tree_.feature[node]]} ≤ {tree_.threshold[node]:.2f}"
            
            # Calculate impurity
            if criterion == "gini":
                impurity = tree_.impurity[node]
                attributes = {"gini": impurity, "samples": tree_.n_node_samples[node]}
            else:
                impurity = tree_.impurity[node]
                attributes = {"entropy": impurity, "samples": tree_.n_node_samples[node]}
            
            # For classification, add class distribution
            if hasattr(clf, 'classes_'):
                class_dist = tree_.value[node][0].astype(int).tolist()
                attributes["class_dist"] = class_dist
            
            return {
                "name": name,
                "attributes": attributes,
                "children": [
                    recurse(tree_.children_left[node]),
                    recurse(tree_.children_right[node])
                ]
            }
        else:
            # Leaf node
            if criterion == "gini":
                impurity = tree_.impurity[node]
                attributes = {"gini": impurity, "samples": tree_.n_node_samples[node]}
            else:
                impurity = tree_.impurity[node]
                attributes = {"entropy": impurity, "samples": tree_.n_node_samples[node]}
            
            # For classification, show the class
            if hasattr(clf, 'classes_'):
                class_idx = np.argmax(tree_.value[node][0])
                class_label = clf.classes_[class_idx]
                name = f"class = {class_label}"
                class_dist = tree_.value[node][0].astype(int).tolist()
                attributes["class_dist"] = class_dist
            else:
                # For regression, show the predicted value
                value = tree_.value[node][0][0]
                name = f"value = {value:.2f}"
            
            return {
                "name": name,
                "attributes": attributes
            }
    
    return recurse(0)


def get_tree_depth(tree_json: Dict[str, Any]) -> int:
    """Calculate the depth of the tree from JSON structure."""
    if "children" not in tree_json or not tree_json["children"]:
        return 1
    return 1 + max(get_tree_depth(child) for child in tree_json["children"])


def count_leaves(tree_json: Dict[str, Any]) -> int:
    """Count the number of leaf nodes in the tree."""
    if "children" not in tree_json or not tree_json["children"]:
        return 1
    return sum(count_leaves(child) for child in tree_json["children"])
