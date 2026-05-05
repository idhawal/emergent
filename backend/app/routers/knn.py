from fastapi import APIRouter
from app.models.schemas import KNNRequest, KNNResponse
from app.services.knn_service import run_knn

router = APIRouter()


@router.post("/knn", response_model=KNNResponse)
async def knn_endpoint(request: KNNRequest):
    """Run KNN algorithm with specified parameters."""
    result = run_knn(
        k=request.k,
        metric=request.metric,
        weights=request.weights,
        task=request.task,
        dataset=request.dataset,
        test_point=request.test_point,
        uploaded_data=request.uploaded_data,
    )
    return result
