import time
import logging
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sys

# Add src to python path
current_dir = Path(__file__).resolve().parent
src_dir = current_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))

from predict import CivicSensePredictor
from schemas import (
    ComplaintRequest, 
    BatchComplaintRequest, 
    RoutingResponse, 
    BatchRoutingResponse, 
    HealthCheckResponse
)

# Configure production logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("civicsense_api")

# Initialize FastAPI app (Must be named 'app' for uvicorn app:app)
app = FastAPI(
    title="CivicSense AI Routing API",
    description="Production-ready NLP routing engine for municipal citizen grievances.",
    version="1.0.0"
)

# Enable CORS for Frontend/Backend Integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Predictor Instance (Singleton)
predictor_instance = None

def get_predictor():
    global predictor_instance
    if predictor_instance is None:
        logger.info("Initializing CivicSense Predictor Singleton...")
        predictor_instance = CivicSensePredictor()
    return predictor_instance

@app.get("/health", response_model=HealthCheckResponse, tags=["System"])
def health_check(predictor: CivicSensePredictor = Depends(get_predictor)):
    return HealthCheckResponse(
        status="healthy",
        model_loaded=predictor.has_ml,
        model_version="baseline-tfidf-logreg-v1",
        total_categories_mapped=32
    )

@app.post("/api/v1/predict", response_model=RoutingResponse, tags=["Inference"])
def predict_single_complaint(
    payload: ComplaintRequest, 
    predictor: CivicSensePredictor = Depends(get_predictor)
):
    start_time = time.time()
    try:
        result = predictor.predict_complaint_text(payload.complaint_text)
        latency = round((time.time() - start_time) * 1000, 2)
        logger.info(f"Routed complaint in {latency}ms -> Dept: {result['department']}")

        return RoutingResponse(
            complaint_text=result["complaint_text"],
            predicted_category=result["predicted_category"],
            predicted_sub_category=result["predicted_sub_category"],
            department=result["department"],
            mapping_status=result["mapping_status"],
            confidence=result["confidence"],
            model_version=result["model_version"],
            manual_review_required=bool(result["confidence"] < 0.20)
        )
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Classification Engine Error: {str(e)}"
        )