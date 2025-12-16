"""
Pydantic schemas for request/response models
"""

from pydantic import BaseModel
from typing import Optional


class AnalysisRequest(BaseModel):
    content: str
    content_type: str  # "url", "email", or "sms"


class LLMAnalysis(BaseModel):
    success: bool
    analysis: str
    model: Optional[str] = None
    error: Optional[str] = None


class AnalysisResponse(BaseModel):
    threatLevel: str  # "safe", "suspicious", "malicious"
    confidenceScore: float  # 0-100 percentage
    rawLabel: str  # Raw model output label
    rawScore: float  # Raw model output score
    llmAnalysis: LLMAnalysis  # LLM cybersecurity analysis
    contentType: str
    timestamp: str
    processingTime: int


# Separate endpoints for progressive loading
class DetectionResponse(BaseModel):
    """Fast BERT detection result"""
    threatLevel: str
    confidenceScore: float
    rawLabel: str
    rawScore: float
    contentType: str
    timestamp: str
    processingTime: int


class LLMRequest(BaseModel):
    """Request for LLM analysis"""
    content: str
    content_type: str
    threat_level: str
    confidence: float

