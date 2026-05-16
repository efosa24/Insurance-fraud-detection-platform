import os
import sys

# Ensure package imports work when running this file directly (vs. `python -m app.api.main`).
if __package__ is None:
    # Add workspace root (two levels up from this file: app/api -> app -> workspace)
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if workspace_root not in sys.path:
        sys.path.insert(0, workspace_root)

from fastapi import FastAPI

from app.model.schema import FraudRequest
from app.model.predict import FraudPredictor

app = FastAPI(
    title="Insurance Fraud Detection API",
    version="1.0.0"
)

predictor = FraudPredictor()

@app.get("/")
def health_check():
    return {"status": "running"}

@app.post("/predict")
def predict_fraud(request: FraudRequest):

    result = predictor.predict(request.dict())

    return result