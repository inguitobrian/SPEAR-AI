"""
SPEAR AI Backend - Phishing Detection API
Uses BERT model fine-tuned for phishing detection + LLM analysis
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import time

from dotenv import load_dotenv
# Load environment variables from backend/.env
ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

from schemas import AnalysisRequest, AnalysisResponse, LLMAnalysis, DetectionResponse, LLMRequest
from models import PhishingDetector, llm_analyzer

app = FastAPI(
    title="SPEAR AI Phishing Detection API",
    description="AI-powered phishing and social engineering detection",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the phishing detector
detector = PhishingDetector()


@app.on_event("startup")
async def startup_event():
    """Load the BERT model and check LLM on startup"""
    detector.load()
    
    # Check LLM status
    if llm_analyzer.is_available():
        print("[OK] LLM Analyzer configured - OpenRouter API ready")
    else:
        print("[!] LLM Analyzer NOT configured - Add OPENROUTER_API_KEY to backend/.env")


def get_threat_level(is_phishing: bool, confidence: float) -> str:
    """Determine threat level based on model prediction"""
    if is_phishing:
        if confidence >= 80:
            return "malicious"
        else:
            return "suspicious"
    else:
        if confidence >= 80:
            return "safe"
        else:
            return "suspicious"


@app.post("/detect", response_model=DetectionResponse)
async def detect_content(request: AnalysisRequest):
    """
    Fast BERT-based threat detection only.
    Returns immediately with threat level and confidence.
    """
    if not detector.is_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded yet")
    
    start_time = time.time()
    
    content = request.content.strip()
    content_type = request.content_type.lower()
    
    if not content:
        raise HTTPException(status_code=400, detail="Content cannot be empty")
    
    if content_type not in ["url", "email", "sms"]:
        raise HTTPException(status_code=400, detail="Invalid content type")
    
    # Run BERT model classification
    try:
        prediction = detector.predict(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model inference error: {str(e)}")
    
    # Determine threat level from model output
    threat_level = get_threat_level(prediction.is_phishing, prediction.confidence)
    
    # Calculate processing time
    processing_time = int((time.time() - start_time) * 1000)
    
    return DetectionResponse(
        threatLevel=threat_level,
        confidenceScore=round(prediction.confidence, 2),
        rawLabel=prediction.raw_label,
        rawScore=round(prediction.raw_score, 4),
        contentType=content_type.upper(),
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
        processingTime=processing_time
    )


@app.post("/analyze-llm", response_model=LLMAnalysis)
async def analyze_with_llm(request: LLMRequest):
    """
    LLM-based detailed security analysis with anomaly detection,
    risk assessment, and mitigation recommendations.
    Call this after /detect to get expert analysis.
    """
    content = request.content.strip()
    content_type = request.content_type.lower()
    
    if not content:
        raise HTTPException(status_code=400, detail="Content cannot be empty")
    
    # Run LLM analysis
    llm_result = llm_analyzer.analyze(
        content=content,
        content_type=content_type,
        bert_threat_level=request.threat_level,
        bert_confidence=request.confidence
    )
    
    return LLMAnalysis(
        success=llm_result["success"],
        analysis=llm_result["analysis"],
        model=llm_result.get("model"),
        error=llm_result.get("error"),
        parsed=llm_result.get("parsed")
    )


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_content(request: AnalysisRequest):
    """
    Full analysis - BERT detection + LLM analysis combined.
    For backwards compatibility.
    """
    if not detector.is_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded yet")
    
    start_time = time.time()
    
    content = request.content.strip()
    content_type = request.content_type.lower()
    
    if not content:
        raise HTTPException(status_code=400, detail="Content cannot be empty")
    
    if content_type not in ["url", "email", "sms"]:
        raise HTTPException(status_code=400, detail="Invalid content type")
    
    # Step 1: Run BERT model classification
    try:
        prediction = detector.predict(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model inference error: {str(e)}")
    
    # Determine threat level from model output
    threat_level = get_threat_level(prediction.is_phishing, prediction.confidence)
    
    # Step 2: Run LLM analysis (cybersecurity expert analysis)
    llm_result = llm_analyzer.analyze(
        content=content,
        content_type=content_type,
        bert_threat_level=threat_level,
        bert_confidence=prediction.confidence
    )
    
    # Calculate processing time
    processing_time = int((time.time() - start_time) * 1000)
    
    return AnalysisResponse(
        threatLevel=threat_level,
        confidenceScore=round(prediction.confidence, 2),
        rawLabel=prediction.raw_label,
        rawScore=round(prediction.raw_score, 4),
        llmAnalysis=LLMAnalysis(
            success=llm_result["success"],
            analysis=llm_result["analysis"],
            model=llm_result.get("model"),
            error=llm_result.get("error"),
            parsed=llm_result.get("parsed")
        ),
        contentType=content_type.upper(),
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
        processingTime=processing_time
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "bert_model_loaded": detector.is_loaded,
        "llm_configured": llm_analyzer.is_available(),
        "gpu_available": detector.is_gpu_available()
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SPEAR AI Phishing Detection API",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
