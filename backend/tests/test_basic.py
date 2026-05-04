"""Basic backend tests for Emergent ML Visualizer."""
import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_python_version():
    """Verify Python version is 3.11+."""
    import sys
    assert sys.version_info >= (3, 11), "Python 3.11+ required"


def test_numpy_import():
    """Test numpy is available."""
    import numpy as np
    arr = np.array([1, 2, 3])
    assert arr.sum() == 6


def test_pandas_import():
    """Test pandas is available."""
    import pandas as pd
    df = pd.DataFrame({'a': [1, 2, 3]})
    assert len(df) == 3


def test_sklearn_import():
    """Test scikit-learn is available."""
    from sklearn.tree import DecisionTreeClassifier
    clf = DecisionTreeClassifier()
    assert clf is not None


def test_fastapi_import():
    """Test FastAPI is available."""
    from fastapi import FastAPI
    app = FastAPI()
    assert app is not None


def test_pydantic_import():
    """Test Pydantic is available."""
    from pydantic import BaseModel
    
    class TestModel(BaseModel):
        name: str
        value: int
    
    obj = TestModel(name="test", value=42)
    assert obj.name == "test"
    assert obj.value == 42
