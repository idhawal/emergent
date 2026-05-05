from fastapi import APIRouter, HTTPException
from app.models.schemas import DecisionTreeRequest, DecisionTreeResponse
from app.services.tree_service import run_decision_tree
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/decision_tree", response_model=DecisionTreeResponse)
async def decision_tree_endpoint(request: DecisionTreeRequest):
    """
    Run decision tree algorithm with specified parameters.
    
    Args:
        request: DecisionTreeRequest object with parameters
        
    Returns:
        DecisionTreeResponse with tree structure and metrics
        
    Raises:
        HTTPException: 400 for validation errors, 500 for internal errors
    """
    try:
        logger.debug(f"Decision tree request: task={request.task}, criterion={request.criterion}")
        result = run_decision_tree(
            task=request.task,
            criterion=request.criterion,
            max_depth=request.max_depth,
            min_samples_split=request.min_samples_split,
            min_samples_leaf=request.min_samples_leaf,
            dataset=request.dataset,
            uploaded_data=request.uploaded_data,
        )
        return result
    except ValueError as e:
        # Input validation errors - return 400 Bad Request
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(e)}"
        )
    except Exception as e:
        # Unexpected errors - return 500 Internal Server Error
        logger.error(f"Unexpected error in decision_tree_endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error processing decision tree"
        )
