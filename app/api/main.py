import os
import sys
import logging
from datetime import datetime
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ensure package imports work when running this file directly (vs. `python -m app.api.main`).
if __package__ is None:
    # Add workspace root (two levels up from this file: app/api -> app -> workspace)
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if workspace_root not in sys.path:
        sys.path.insert(0, workspace_root)

from app.model.schema import FraudRequest
from app.model.predict import FraudPredictor

# Initialize FastAPI app
app = FastAPI(
    title="Insurance Fraud Detection API",
    version="1.0.0",
    description="Advanced ML-powered insurance fraud detection system",
    contact={
        "name": "Support",
        "email": "support@frauddetection.com"
    },
    license_info={
        "name": "MIT License"
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize predictor
try:
    predictor = FraudPredictor()
    logger.info("Fraud predictor initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize predictor: {str(e)}")
    predictor = None

# Response models
class PredictionResponse(BaseModel):
    fraud_prediction: int
    fraud_probability: float
    confidence: float
    timestamp: str
    processing_time_ms: float
    model_version: str = "1.0.0"

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    model_loaded: bool

class ErrorResponse(BaseModel):
    error: str
    detail: str
    timestamp: str
    request_id: str

class StatsResponse(BaseModel):
    total_predictions: int
    fraud_detections: int
    avg_processing_time_ms: float
    uptime_seconds: float

# Global stats
stats = {
    "total_predictions": 0,
    "fraud_detections": 0,
    "total_time": 0.0,
    "start_time": time.time()
}

# Middleware for request/response logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = f"{int(time.time() * 1000)}-{request.client.host}"
    request.state.request_id = request_id
    
    logger.info(f"[{request_id}] {request.method} {request.url.path}")
    
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    
    logger.info(f"[{request_id}] Status: {response.status_code}, Time: {process_time:.2f}ms")
    
    return response

# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check API health and model status"""
    return HealthResponse(
        status="healthy" if predictor else "degraded",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        model_loaded=predictor is not None
    )

@app.get("/", response_model=HealthResponse, tags=["Health"])
async def root():
    """Root endpoint - returns health status"""
    return HealthResponse(
        status="healthy" if predictor else "degraded",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        model_loaded=predictor is not None
    )

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
async def predict_fraud(request: FraudRequest):
    """
    Predict fraud probability for an insurance claim
    
    **Parameters:**
    - Month: Month of the accident
    - WeekOfMonth: Week number (1-4)
    - DayOfWeek: Day of the week
    - Make: Vehicle manufacturer
    - AccidentArea: Area type (Urban/Suburban/Rural)
    - Age: Driver age
    - Fault: Fault determination
    - PolicyType: Type of insurance policy
    - VehicleCategory: Vehicle type (Sedan/SUV/Truck/etc)
    - VehiclePrice: Vehicle price range
    - Deductible: Claim deductible amount
    - DriverRating: Driver safety rating (1-5)
    - Year: Vehicle year
    - BasePolicy: Base policy type
    
    **Returns:**
    - fraud_prediction: 0 (legitimate) or 1 (fraud)
    - fraud_probability: Probability of fraud (0-1)
    - confidence: Model confidence score
    - processing_time_ms: Time taken to process
    """
    
    if not predictor:
        logger.error("Predictor not initialized")
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Service unavailable."
        )
    
    try:
        start_time = time.time()
        
        # Make prediction
        result = predictor.predict(request.dict())
        
        processing_time = (time.time() - start_time) * 1000
        
        # Update stats
        stats["total_predictions"] += 1
        if result["fraud_prediction"] == 1:
            stats["fraud_detections"] += 1
        stats["total_time"] += processing_time
        
        # Calculate confidence
        fraud_prob = result["fraud_probability"]
        confidence = max(fraud_prob, 1 - fraud_prob)
        
        logger.info(
            f"Prediction: fraud={result['fraud_prediction']}, "
            f"prob={fraud_prob:.4f}, time={processing_time:.2f}ms"
        )
        
        return PredictionResponse(
            fraud_prediction=result["fraud_prediction"],
            fraud_probability=fraud_prob,
            confidence=confidence,
            timestamp=datetime.now().isoformat(),
            processing_time_ms=round(processing_time, 2),
            model_version="1.0.0"
        )
        
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=422,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# Batch prediction endpoint
@app.post("/predict_batch", tags=["Predictions"])
async def predict_batch(requests_list: List[FraudRequest]):
    """
    Predict fraud for multiple cases in batch
    
    Returns list of predictions with same format as /predict
    """
    
    if not predictor:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        results = []
        for idx, request in enumerate(requests_list):
            try:
                start_time = time.time()
                result = predictor.predict(request.dict())
                processing_time = (time.time() - start_time) * 1000
                
                fraud_prob = result["fraud_probability"]
                confidence = max(fraud_prob, 1 - fraud_prob)
                
                results.append(PredictionResponse(
                    fraud_prediction=result["fraud_prediction"],
                    fraud_probability=fraud_prob,
                    confidence=confidence,
                    timestamp=datetime.now().isoformat(),
                    processing_time_ms=round(processing_time, 2)
                ))
                
            except Exception as e:
                logger.error(f"Error processing batch item {idx}: {str(e)}")
                results.append({
                    "error": str(e),
                    "index": idx
                })
        
        return results
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Statistics endpoint
@app.get("/stats", response_model=StatsResponse, tags=["Monitoring"])
async def get_stats():
    """Get API statistics and performance metrics"""
    
    avg_time = (stats["total_time"] / stats["total_predictions"] 
                if stats["total_predictions"] > 0 else 0)
    
    uptime = time.time() - stats["start_time"]
    
    return StatsResponse(
        total_predictions=stats["total_predictions"],
        fraud_detections=stats["fraud_detections"],
        avg_processing_time_ms=round(avg_time, 2),
        uptime_seconds=round(uptime, 2)
    )

# Error handlers
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handle validation errors"""
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat(),
            "request_id": getattr(request.state, "request_id", "unknown")
        },
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat(),
            "request_id": getattr(request.state, "request_id", "unknown")
        },
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)