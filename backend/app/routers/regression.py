from fastapi import APIRouter
from app.models.schemas import RegressionRequest, RegressionResponse
from app.services.regression_service import run_regression

router = APIRouter()


@router.post("/regression", response_model=RegressionResponse)
async def regression_endpoint(request: RegressionRequest):
    """Run regression algorithm with specified parameters."""
    result = run_regression(
        algo=request.algo,
        learning_rate=request.learning_rate,
        epochs=request.epochs,
        poly_degree=request.poly_degree,
        penalty=request.penalty,
        l1_ratio=request.l1_ratio,
        noise=request.noise,
        early_stopping=request.early_stopping
    )
    return result
