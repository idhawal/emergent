from fastapi import APIRouter
from app.models.schemas import DecisionTreeRequest, DecisionTreeResponse
from app.services.tree_service import run_decision_tree

router = APIRouter()


@router.post("/decision_tree", response_model=DecisionTreeResponse)
async def decision_tree_endpoint(request: DecisionTreeRequest):
    """Run decision tree algorithm with specified parameters."""
    result = run_decision_tree(
        task=request.task,
        criterion=request.criterion,
        max_depth=request.max_depth,
        min_samples_split=request.min_samples_split,
        min_samples_leaf=request.min_samples_leaf,
        dataset=request.dataset
    )
    return result
