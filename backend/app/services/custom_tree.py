"""
Custom Decision Tree implementation from scratch.
No sklearn used - pure NumPy implementation.
"""
import numpy as np
from typing import Optional, Dict, Any, List


class TreeNode:
    """Node in the decision tree."""
    
    def __init__(self):
        self.feature_index: Optional[int] = None
        self.threshold: Optional[float] = None
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None
        self.value: Optional[float] = None  # For leaf nodes
        self.gini: Optional[float] = None
        self.entropy: Optional[float] = None
        self.samples: int = 0
        self.class_distribution: Optional[List[int]] = None


def calculate_gini(y: np.ndarray) -> float:
    """
    Calculate Gini impurity from scratch.
    Gini = 1 - Σ(p_i^2)
    """
    if len(y) == 0:
        return 0.0
    
    classes, counts = np.unique(y, return_counts=True)
    probabilities = counts / len(y)
    gini = 1.0 - np.sum(probabilities ** 2)
    
    return float(gini)


def calculate_entropy(y: np.ndarray) -> float:
    """
    Calculate entropy from scratch.
    Entropy = -Σ(p_i * log2(p_i))
    """
    if len(y) == 0:
        return 0.0
    
    classes, counts = np.unique(y, return_counts=True)
    probabilities = counts / len(y)
    
    # Avoid log(0)
    probabilities = probabilities[probabilities > 0]
    entropy = -np.sum(probabilities * np.log2(probabilities))
    
    return float(entropy)


def calculate_information_gain(
    y_parent: np.ndarray,
    y_left: np.ndarray,
    y_right: np.ndarray,
    criterion: str
) -> float:
    """
    Calculate information gain from a split.
    Gain = Impurity(parent) - weighted_avg(Impurity(children))
    """
    if criterion == "gini":
        parent_impurity = calculate_gini(y_parent)
        left_impurity = calculate_gini(y_left)
        right_impurity = calculate_gini(y_right)
    else:  # entropy
        parent_impurity = calculate_entropy(y_parent)
        left_impurity = calculate_entropy(y_left)
        right_impurity = calculate_entropy(y_right)
    
    n = len(y_parent)
    n_left = len(y_left)
    n_right = len(y_right)
    
    if n == 0:
        return 0.0
    
    # Weighted average of children impurities
    weighted_impurity = (n_left / n) * left_impurity + (n_right / n) * right_impurity
    
    # Information gain
    gain = parent_impurity - weighted_impurity
    
    return gain


def find_best_split(
    X: np.ndarray,
    y: np.ndarray,
    criterion: str,
    min_samples_split: int,
    min_samples_leaf: int
) -> tuple:
    """
    Find the best feature and threshold to split on.
    Returns: (best_feature_index, best_threshold, best_gain)
    """
    n_samples, n_features = X.shape
    
    if n_samples < min_samples_split:
        return None, None, -1
    
    best_gain = -1
    best_feature = None
    best_threshold = None
    
    # Try each feature
    for feature_idx in range(n_features):
        feature_values = X[:, feature_idx]
        
        # Get unique values as potential thresholds
        thresholds = np.unique(feature_values)
        
        # Try each threshold
        for threshold in thresholds:
            # Split data
            left_mask = feature_values <= threshold
            right_mask = ~left_mask
            
            y_left = y[left_mask]
            y_right = y[right_mask]
            
            # Check min_samples_leaf constraint
            if len(y_left) < min_samples_leaf or len(y_right) < min_samples_leaf:
                continue
            
            # Calculate information gain
            gain = calculate_information_gain(y, y_left, y_right, criterion)
            
            # Update best split
            if gain > best_gain:
                best_gain = gain
                best_feature = feature_idx
                best_threshold = threshold
    
    return best_feature, best_threshold, best_gain


class CustomDecisionTreeClassifier:
    """
    Decision Tree Classifier implemented from scratch.
    Uses CART algorithm with Gini or Entropy criterion.
    """
    
    def __init__(
        self,
        criterion: str = "gini",
        max_depth: Optional[int] = None,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        random_state: Optional[int] = None
    ):
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.random_state = random_state
        self.root: Optional[TreeNode] = None
        self.classes_: Optional[np.ndarray] = None
        self.n_classes_: int = 0
        self.feature_importances_: Optional[np.ndarray] = None
        self.n_features_: int = 0
    
    def fit(self, X: np.ndarray, y: np.ndarray):
        """Fit the decision tree classifier."""
        if self.random_state is not None:
            np.random.seed(self.random_state)
        
        self.classes_ = np.unique(y)
        self.n_classes_ = len(self.classes_)
        self.n_features_ = X.shape[1]
        self.feature_importances_ = np.zeros(self.n_features_)
        
        # Build tree recursively
        self.root = self._build_tree(X, y, depth=0)
        
        # Normalize feature importances
        if np.sum(self.feature_importances_) > 0:
            self.feature_importances_ /= np.sum(self.feature_importances_)
        
        return self
    
    def _build_tree(self, X: np.ndarray, y: np.ndarray, depth: int) -> TreeNode:
        """Recursively build the decision tree."""
        node = TreeNode()
        node.samples = len(y)
        
        # Calculate impurity
        if self.criterion == "gini":
            node.gini = calculate_gini(y)
        else:
            node.entropy = calculate_entropy(y)
        
        # Store class distribution
        classes, counts = np.unique(y, return_counts=True)
        node.class_distribution = [0] * self.n_classes_
        for cls, count in zip(classes, counts):
            cls_idx = np.where(self.classes_ == cls)[0][0]
            node.class_distribution[cls_idx] = int(count)
        
        # Check stopping criteria
        if (self.max_depth is not None and depth >= self.max_depth) or \
           len(y) < self.min_samples_split or \
           len(np.unique(y)) == 1:
            # Leaf node
            node.value = self._most_common_class(y)
            return node
        
        # Find best split
        best_feature, best_threshold, best_gain = find_best_split(
            X, y, self.criterion, self.min_samples_split, self.min_samples_leaf
        )
        
        if best_feature is None or best_gain <= 0:
            # Leaf node (no valid split found)
            node.value = self._most_common_class(y)
            return node
        
        # Update feature importance
        self.feature_importances_[best_feature] += best_gain * len(y)
        
        # Split data
        left_mask = X[:, best_feature] <= best_threshold
        right_mask = ~left_mask
        
        X_left, y_left = X[left_mask], y[left_mask]
        X_right, y_right = X[right_mask], y[right_mask]
        
        # Create internal node
        node.feature_index = best_feature
        node.threshold = best_threshold
        node.left = self._build_tree(X_left, y_left, depth + 1)
        node.right = self._build_tree(X_right, y_right, depth + 1)
        
        return node
    
    def _most_common_class(self, y: np.ndarray) -> float:
        """Return the most common class in y."""
        classes, counts = np.unique(y, return_counts=True)
        return classes[np.argmax(counts)]
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels for samples in X."""
        return np.array([self._predict_sample(x, self.root) for x in X])
    
    def _predict_sample(self, x: np.ndarray, node: TreeNode) -> float:
        """Predict class for a single sample."""
        if node.value is not None:
            # Leaf node
            return node.value
        
        # Internal node - traverse
        if x[node.feature_index] <= node.threshold:
            return self._predict_sample(x, node.left)
        else:
            return self._predict_sample(x, node.right)
    
    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Return the accuracy score."""
        predictions = self.predict(X)
        return np.mean(predictions == y)
    
    def to_json(self, feature_names: List[str]) -> Dict[str, Any]:
        """Convert tree to JSON format for react-d3-tree."""
        return self._node_to_json(self.root, feature_names)
    
    def _node_to_json(self, node: TreeNode, feature_names: List[str]) -> Dict[str, Any]:
        """Recursively convert node to JSON."""
        if node.value is not None:
            # Leaf node
            attributes = {
                "samples": node.samples,
                "class_dist": node.class_distribution
            }
            
            if self.criterion == "gini":
                attributes["gini"] = round(node.gini, 3) if node.gini is not None else 0
            else:
                attributes["entropy"] = round(node.entropy, 3) if node.entropy is not None else 0
            
            return {
                "name": f"class = {int(node.value)}",
                "attributes": attributes
            }
        
        # Internal node
        feature_name = feature_names[node.feature_index] if node.feature_index < len(feature_names) else f"feature_{node.feature_index}"
        
        attributes = {
            "samples": node.samples,
            "class_dist": node.class_distribution
        }
        
        if self.criterion == "gini":
            attributes["gini"] = round(node.gini, 3) if node.gini is not None else 0
        else:
            attributes["entropy"] = round(node.entropy, 3) if node.entropy is not None else 0
        
        return {
            "name": f"{feature_name} ≤ {node.threshold:.2f}",
            "attributes": attributes,
            "children": [
                self._node_to_json(node.left, feature_names),
                self._node_to_json(node.right, feature_names)
            ]
        }
    
    def get_depth(self) -> int:
        """Get the depth of the tree."""
        return self._get_node_depth(self.root)
    
    def _get_node_depth(self, node: TreeNode) -> int:
        """Recursively calculate node depth."""
        if node.value is not None:
            return 1
        return 1 + max(
            self._get_node_depth(node.left),
            self._get_node_depth(node.right)
        )
    
    def get_n_leaves(self) -> int:
        """Get the number of leaf nodes."""
        return self._count_leaves(self.root)
    
    def _count_leaves(self, node: TreeNode) -> int:
        """Recursively count leaf nodes."""
        if node.value is not None:
            return 1
        return self._count_leaves(node.left) + self._count_leaves(node.right)


class CustomDecisionTreeRegressor:
    """
    Decision Tree Regressor implemented from scratch.
    Uses variance reduction as splitting criterion.
    """
    
    def __init__(
        self,
        max_depth: Optional[int] = None,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        random_state: Optional[int] = None
    ):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.random_state = random_state
        self.root: Optional[TreeNode] = None
        self.feature_importances_: Optional[np.ndarray] = None
        self.n_features_: int = 0
    
    def fit(self, X: np.ndarray, y: np.ndarray):
        """Fit the decision tree regressor."""
        if self.random_state is not None:
            np.random.seed(self.random_state)
        
        self.n_features_ = X.shape[1]
        self.feature_importances_ = np.zeros(self.n_features_)
        
        # Build tree recursively
        self.root = self._build_tree(X, y, depth=0)
        
        # Normalize feature importances
        if np.sum(self.feature_importances_) > 0:
            self.feature_importances_ /= np.sum(self.feature_importances_)
        
        return self
    
    def _calculate_variance(self, y: np.ndarray) -> float:
        """Calculate variance of y."""
        if len(y) == 0:
            return 0.0
        return float(np.var(y))
    
    def _calculate_variance_reduction(
        self,
        y_parent: np.ndarray,
        y_left: np.ndarray,
        y_right: np.ndarray
    ) -> float:
        """Calculate variance reduction from a split."""
        parent_var = self._calculate_variance(y_parent)
        
        n = len(y_parent)
        n_left = len(y_left)
        n_right = len(y_right)
        
        if n == 0:
            return 0.0
        
        left_var = self._calculate_variance(y_left)
        right_var = self._calculate_variance(y_right)
        
        weighted_var = (n_left / n) * left_var + (n_right / n) * right_var
        
        return parent_var - weighted_var
    
    def _find_best_split_regression(
        self,
        X: np.ndarray,
        y: np.ndarray
    ) -> tuple:
        """Find the best split for regression."""
        n_samples, n_features = X.shape
        
        if n_samples < self.min_samples_split:
            return None, None, -1
        
        best_gain = -1
        best_feature = None
        best_threshold = None
        
        for feature_idx in range(n_features):
            feature_values = X[:, feature_idx]
            thresholds = np.unique(feature_values)
            
            for threshold in thresholds:
                left_mask = feature_values <= threshold
                right_mask = ~left_mask
                
                y_left = y[left_mask]
                y_right = y[right_mask]
                
                if len(y_left) < self.min_samples_leaf or len(y_right) < self.min_samples_leaf:
                    continue
                
                gain = self._calculate_variance_reduction(y, y_left, y_right)
                
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature_idx
                    best_threshold = threshold
        
        return best_feature, best_threshold, best_gain
    
    def _build_tree(self, X: np.ndarray, y: np.ndarray, depth: int) -> TreeNode:
        """Recursively build the regression tree."""
        node = TreeNode()
        node.samples = len(y)
        
        # Check stopping criteria
        if (self.max_depth is not None and depth >= self.max_depth) or \
           len(y) < self.min_samples_split or \
           self._calculate_variance(y) < 1e-7:
            # Leaf node
            node.value = float(np.mean(y))
            return node
        
        # Find best split
        best_feature, best_threshold, best_gain = self._find_best_split_regression(X, y)
        
        if best_feature is None or best_gain <= 0:
            # Leaf node
            node.value = float(np.mean(y))
            return node
        
        # Update feature importance
        self.feature_importances_[best_feature] += best_gain * len(y)
        
        # Split data
        left_mask = X[:, best_feature] <= best_threshold
        right_mask = ~left_mask
        
        X_left, y_left = X[left_mask], y[left_mask]
        X_right, y_right = X[right_mask], y[right_mask]
        
        # Create internal node
        node.feature_index = best_feature
        node.threshold = best_threshold
        node.left = self._build_tree(X_left, y_left, depth + 1)
        node.right = self._build_tree(X_right, y_right, depth + 1)
        
        return node
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict values for samples in X."""
        return np.array([self._predict_sample(x, self.root) for x in X])
    
    def _predict_sample(self, x: np.ndarray, node: TreeNode) -> float:
        """Predict value for a single sample."""
        if node.value is not None:
            return node.value
        
        if x[node.feature_index] <= node.threshold:
            return self._predict_sample(x, node.left)
        else:
            return self._predict_sample(x, node.right)
    
    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Return the R^2 score."""
        predictions = self.predict(X)
        ss_res = np.sum((y - predictions) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
    
    def to_json(self, feature_names: List[str]) -> Dict[str, Any]:
        """Convert tree to JSON format for react-d3-tree."""
        return self._node_to_json(self.root, feature_names)
    
    def _node_to_json(self, node: TreeNode, feature_names: List[str]) -> Dict[str, Any]:
        """Recursively convert node to JSON."""
        if node.value is not None:
            # Leaf node
            return {
                "name": f"value = {node.value:.2f}",
                "attributes": {
                    "samples": node.samples,
                    "class_dist": []
                }
            }
        
        # Internal node
        feature_name = feature_names[node.feature_index] if node.feature_index < len(feature_names) else f"feature_{node.feature_index}"
        
        return {
            "name": f"{feature_name} ≤ {node.threshold:.2f}",
            "attributes": {
                "samples": node.samples,
                "class_dist": []
            },
            "children": [
                self._node_to_json(node.left, feature_names),
                self._node_to_json(node.right, feature_names)
            ]
        }
    
    def get_depth(self) -> int:
        """Get the depth of the tree."""
        return self._get_node_depth(self.root)
    
    def _get_node_depth(self, node: TreeNode) -> int:
        """Recursively calculate node depth."""
        if node.value is not None:
            return 1
        return 1 + max(
            self._get_node_depth(node.left),
            self._get_node_depth(node.right)
        )
    
    def get_n_leaves(self) -> int:
        """Get the number of leaf nodes."""
        return self._count_leaves(self.root)
    
    def _count_leaves(self, node: TreeNode) -> int:
        """Recursively count leaf nodes."""
        if node.value is not None:
            return 1
        return self._count_leaves(node.left) + self._count_leaves(node.right)
