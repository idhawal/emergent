from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from typing_extensions import Annotated


# ========== REGRESSION MODELS ==========

class RegressionRequest(BaseModel):
    algo: Literal["linear_gd", "polynomial", "ridge", "lasso", "elastic_net"]
    learning_rate: Annotated[float, Field(gt=0, le=1.0)]
    epochs: Annotated[int, Field(ge=1, le=10000)]
    poly_degree: Annotated[int, Field(ge=1, le=4)]
    penalty: Annotated[float, Field(ge=0)]
    l1_ratio: Annotated[float, Field(ge=0.0, le=1.0)]
    noise: Annotated[float, Field(ge=0.0, le=1.0)]
    early_stopping: bool = False


class RegressionResponse(BaseModel):
    curve_x: List[float]
    curve_y: List[float]
    scatter_x: List[float]
    scatter_y: List[float]
    cost_history: List[float]
    coefficients: List[float]
    feature_names: List[str]
    stopped_at_epoch: Optional[int] = None


# ========== KNN MODELS ==========

class KNNRequest(BaseModel):
    k: Annotated[int, Field(ge=1, le=50)]
    metric: Literal["euclidean", "manhattan"]
    weights: Literal["uniform", "distance"]
    task: Literal["classification", "regression"]
    dataset: Literal["moons", "circles", "blobs", "sine"]
    test_point: Optional[List[float]] = None


class KNNResponse(BaseModel):
    train_points: List[List[float]]
    train_labels: List[float]
    mesh_xx: List[List[float]]
    mesh_yy: List[List[float]]
    mesh_zz: List[List[float]]
    neighbor_indices: List[int]
    test_prediction: float


# ========== DECISION TREE MODELS ==========

class DecisionTreeRequest(BaseModel):
    task: Literal["classifier", "regressor"]
    criterion: Literal["gini", "entropy"]
    max_depth: Optional[Annotated[int, Field(ge=1, le=10)]] = None
    min_samples_split: Annotated[int, Field(ge=2, le=20)]
    min_samples_leaf: Annotated[int, Field(ge=1, le=20)]
    dataset: Literal["iris", "breast_cancer", "blobs"]


class TreeNodeAttributes(BaseModel):
    gini: Optional[float] = None
    entropy: Optional[float] = None
    samples: int
    class_dist: List[int]


class TreeNode(BaseModel):
    name: str
    attributes: TreeNodeAttributes
    children: Optional[List["TreeNode"]] = None


# Resolve forward reference
TreeNode.model_rebuild()


class DecisionTreeResponse(BaseModel):
    tree_json: TreeNode
    accuracy: float
    depth: int
    n_leaves: int
    feature_importances: dict


# ========== GENETIC ALGORITHM MODELS ==========

class GARequest(BaseModel):
    function: Literal["sphere", "rosenbrock", "rastrigin"]
    pop_size: Annotated[int, Field(ge=10, le=200)]
    mutation_rate: Annotated[float, Field(ge=0.0, le=1.0)]
    crossover_rate: Annotated[float, Field(ge=0.0, le=1.0)]
    generations: Annotated[int, Field(ge=1, le=500)]
    eta_m: Annotated[float, Field(ge=1, le=50)]
    eta_c: Annotated[float, Field(ge=1, le=50)]


class GAHistoryEntry(BaseModel):
    generation: int
    points: List[List[float]]
    fitness_values: List[float]
    best_fitness: float
    avg_fitness: float
    best_point: List[float]


class GAResponse(BaseModel):
    contour_x: List[List[float]]
    contour_y: List[List[float]]
    contour_z: List[List[float]]
    history: List[GAHistoryEntry]
    converged_at_generation: Optional[int] = None
