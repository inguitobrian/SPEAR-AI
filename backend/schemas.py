"""
Pydantic schemas for request/response models
"""

from pydantic import BaseModel
from typing import Optional, List


class AnalysisRequest(BaseModel):
    content: str
    content_type: str  # "url", "email", or "sms"


class RiskAssessment(BaseModel):
    """Risk assessment details"""
    level: str  # CRITICAL / HIGH / MEDIUM / LOW
    score: int  # 0-100
    factors: List[str]
    category: str  # e.g., "Credential Theft", "Financial Fraud"


class AnomalyDetection(BaseModel):
    """Anomaly detection results"""
    hasAnomalies: bool
    anomalies: List[str]
    anomalyScore: int  # 0-100
    patterns: List[str]


class MitigationRecommendations(BaseModel):
    """Security mitigation recommendations"""
    strategies: List[str]
    incidentResponse: List[str]
    policyAlignment: List[str]


class ParsedAnalysis(BaseModel):
    """Structured parsed analysis data"""
    riskAssessment: RiskAssessment
    anomalyDetection: AnomalyDetection
    mitigationRecommendations: MitigationRecommendations


class LLMAnalysis(BaseModel):
    success: bool
    analysis: str
    model: Optional[str] = None
    error: Optional[str] = None
    parsed: Optional[ParsedAnalysis] = None


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

