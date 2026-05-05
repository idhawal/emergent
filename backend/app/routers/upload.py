from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import io

router = APIRouter()

@router.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    """
    Upload a CSV file and parse it into a dataset.
    Returns column names, rows, and basic statistics.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported. Please upload a .csv file."
        )
    
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=422,
            detail="Could not decode CSV file. Please ensure it's UTF-8 encoded."
        )
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Could not parse CSV: {str(e)}"
        )
    
    if df.empty:
        raise HTTPException(
            status_code=422,
            detail="CSV file is empty. Please upload a file with data."
        )
    
    if len(df.columns) < 2:
        raise HTTPException(
            status_code=422,
            detail="CSV must have at least 2 columns (features and target)."
        )
    
    return {
        "filename": file.filename,
        "columns": df.columns.tolist(),
        "rows": df.to_dict(orient="records"),
        "n_samples": len(df),
        "n_features": len(df.columns),
        "preview": df.head(5).to_dict(orient="records"),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
    }
