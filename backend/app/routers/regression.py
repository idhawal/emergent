import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from app.models.schemas import RegressionRequest, RegressionResponse
from app.routers.datasets import DATASETS
from app.services.regression_service import run_regression

router = APIRouter()


def resolve_xy(request: RegressionRequest):
    if request.uploaded_data:
        df = pd.DataFrame(request.uploaded_data)
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if len(numeric_cols) < 2:
            raise HTTPException(status_code=422, detail="CSV must have at least 2 numeric columns.")
        x = df[numeric_cols[0]].values.astype(float)
        y = df[numeric_cols[-1]].values.astype(float)
        return x, y

    if request.dataset and request.dataset in DATASETS:
        df = DATASETS[request.dataset]()
        x = df.iloc[:, 0].values.astype(float)
        y = df.iloc[:, -1].values.astype(float)
        return x, y

    np.random.seed(0)
    x = np.linspace(0, 10, 100)
    y = 2 * x + 1 + np.random.randn(100) * request.noise * 5
    return x, y


@router.post("/regression", response_model=RegressionResponse)
async def regression_endpoint(request: RegressionRequest):
    """Run regression algorithm with specified parameters."""
    x_data, y_data = resolve_xy(request)
    result = run_regression(
        algo=request.algo,
        learning_rate=request.learning_rate,
        epochs=request.epochs,
        poly_degree=request.poly_degree,
        penalty=request.penalty,
        l1_ratio=request.l1_ratio,
        noise=request.noise,
        early_stopping=request.early_stopping,
        x_data=x_data,
        y_data=y_data,
    )
    return result
