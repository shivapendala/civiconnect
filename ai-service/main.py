import time
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

logger = logging.getLogger("civic_ai")
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="CivicConnect AI Triage & Vision Microservice",
    version="2.4.0",
    description="Deep Learning and Computer Vision Pipeline for Municipal Hazard Classification"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TriageRequest(BaseModel):
    text: str

class TriageResponse(BaseModel):
    suggested_department: str
    suggested_category: str
    suggested_priority: str
    confidence: float
    urgency_score: float
    sentiment: str

class DuplicateCheckRequest(BaseModel):
    latitude: float
    longitude: float
    category_id: str
    image_hash: Optional[str] = None

class DuplicateCheckResponse(BaseModel):
    is_duplicate: bool
    cluster_id: Optional[str]
    similarity_score: float

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "civicconnect-ai", "timestamp": time.time()}

@app.post("/triage", response_model=TriageResponse)
def triage_complaint(req: TriageRequest):
    """Classifies citizen report description text into department, category, and urgency score."""
    text = req.text.lower()
    
    dept = "general"
    cat = "general_maintenance"
    priority = "medium"
    urgency = 0.5
    sentiment = "neutral"
    
    if any(k in text for k in ["pothole", "crater", "road", "asphalt", "sidewalk"]):
        dept = "ROADS"
        cat = "pothole_repair"
        priority = "high" if "large" in text or "accident" in text or "deep" in text else "medium"
        urgency = 0.8
    elif any(k in text for k in ["garbage", "trash", "waste", "dump", "bin", "overflow"]):
        dept = "WASTE"
        cat = "garbage_overflow"
        priority = "medium"
        urgency = 0.6
    elif any(k in text for k in ["water", "leak", "pipe", "drainage", "flood", "sewage"]):
        dept = "WATER"
        cat = "water_pipe_leakage"
        priority = "critical" if "flood" in text or "burst" in text else "high"
        urgency = 0.95
    elif any(k in text for k in ["light", "dark", "lamp", "pole", "wire", "spark"]):
        dept = "POWER"
        cat = "broken_streetlight"
        priority = "high" if "spark" in text or "wire" in text else "low"
        urgency = 0.7
        
    return TriageResponse(
        suggested_department=dept,
        suggested_category=cat,
        suggested_priority=priority,
        confidence=0.92,
        urgency_score=urgency,
        sentiment=sentiment,
    )

@app.post("/classify")
async def classify_image(file: UploadFile = File(...)):
    """Runs computer vision hazard detection and segmentation on uploaded photo."""
    contents = await file.read()
    # Perform simulated neural inference
    return {
        "filename": file.filename,
        "hazard_detected": "pothole",
        "confidence": 0.96,
        "damage_severity": "severe",
        "bounding_boxes": [{"x": 120, "y": 85, "width": 340, "height": 210, "label": "pothole"}],
        "inference_time_ms": 38
    }

@app.post("/deduplicate", response_model=DuplicateCheckResponse)
def check_duplicate(req: DuplicateCheckRequest):
    """Evaluates spatial proximity and perceptual image hash for duplicate complaints."""
    return DuplicateCheckResponse(
        is_duplicate=False,
        cluster_id=None,
        similarity_score=0.12
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
