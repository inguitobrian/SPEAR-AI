"""
LLM-based Cybersecurity Analysis
Dual LLM Support: DeepSeek V3.1 Nex N1 + Google Gemini 3
"""

import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from backend/.env
BACKEND_DIR = Path(__file__).parent.parent
ENV_PATH = BACKEND_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# OpenRouter configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Dual LLM Models
PRIMARY_MODEL = "nex-agi/deepseek-v3.1-nex-n1:free"  # DeepSeek
SECONDARY_MODEL = "google/gemma-3-12b-it:free"  # Gemini

# System prompt for the cybersecurity analyst
SYSTEM_PROMPT = """You are an expert cybersecurity analyst specializing in phishing detection and social engineering analysis. Your role is to comprehensively analyze potentially malicious content (URLs, emails, SMS messages) and provide detailed security assessments.

Your analysis must include ALL of the following sections in this exact format:

## Threat Assessment
[Brief 2-3 sentence summary of the overall threat]

## Red Flags Identified
[List each red flag as bullet points with explanations]
• [Flag 1]: [Explanation]
• [Flag 2]: [Explanation]

## Anomaly Detection
**Anomaly Score**: [0-100]
**Detected Anomalies**:
• [Anomaly 1]
• [Anomaly 2]
**Behavioral Patterns**: [list any suspicious patterns]

## Risk Classification
**Risk Level**: [CRITICAL / HIGH / MEDIUM / LOW]
**Risk Score**: [0-100]
**Risk Category**: [Credential Theft / Financial Fraud / Malware Delivery / Social Engineering / Data Harvesting / Impersonation / etc.]
**Risk Factors**:
• [Factor 1]
• [Factor 2]

## Attack Technique
[Detailed explanation of the attack methodology]

## Mitigation Recommendations

### Security Strategies
• [Action 1]: [Description]
• [Action 2]: [Description]

### Incident Response
• [Step 1]
• [Step 2]

### Policy Alignment
• NIST Cybersecurity Framework: [relevant controls]
• ISO/IEC 27001: [relevant controls]

Be thorough and provide actionable intelligence. All sections are mandatory."""


class LLMAnalyzer:
    """
    Dual LLM-based security analyzer using OpenRouter API.
    Supports both DeepSeek and Gemini models for comprehensive analysis.
    """
    
    def __init__(self):
        self.client = None
        self.is_configured = False
        self._initialize()
    
    def _initialize(self):
        """Initialize the OpenAI client for OpenRouter"""
        if OPENROUTER_API_KEY and OPENROUTER_API_KEY.strip():
            self.client = OpenAI(
                base_url=OPENROUTER_BASE_URL,
                api_key=OPENROUTER_API_KEY,
            )
            self.is_configured = True
            print(f"[OK] Dual LLM Analyzer configured:")
            print(f"    - Primary: {PRIMARY_MODEL}")
            print(f"    - Secondary: {SECONDARY_MODEL}")
        else:
            print("[!] LLM Analyzer not configured - OPENROUTER_API_KEY not set")
            self.is_configured = False
    
    def analyze(self, content: str, content_type: str, bert_threat_level: str, bert_confidence: float) -> dict:
        """
        Perform comprehensive LLM-based security analysis including anomaly detection,
        risk classification, and mitigation recommendations.
        
        Args:
            content: The content to analyze (URL, email, or SMS)
            content_type: Type of content ("url", "email", "sms")
            bert_threat_level: Threat level from BERT model
            bert_confidence: Confidence score from BERT model
            
        Returns:
            dict with comprehensive analysis including anomalies, risk, and mitigations
        """
        if not self.is_configured:
            return self._get_fallback_analysis(content, content_type, bert_threat_level, bert_confidence)
        
        # Build the user prompt with context
        user_prompt = f"""Analyze the following {content_type.upper()} for potential phishing or social engineering threats.

**Content to analyze:**
```
{content[:3000]}  
```

**BERT Model Pre-analysis:**
- Threat Level: {bert_threat_level.upper()}
- Confidence: {bert_confidence}%

Provide a COMPLETE analysis following ALL sections in the system prompt. Be specific and thorough."""

        try:
            response = self.client.chat.completions.create(
                model=PRIMARY_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=2000,
                temperature=0.4,
                extra_headers={
                    "HTTP-Referer": "https://spear-ai.local",
                    "X-Title": "SPEAR AI Security Analyzer"
                }
            )
            
            analysis_text = response.choices[0].message.content
            
            # Parse the LLM response to extract structured data
            parsed_data = self._parse_llm_analysis(analysis_text)
            
            return {
                "success": True,
                "analysis": analysis_text,
                "model": PRIMARY_MODEL,
                "tokens_used": response.usage.total_tokens if response.usage else None,
                "parsed": parsed_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "analysis": f"LLM analysis failed: {str(e)}",
                "error": str(e),
                "model": PRIMARY_MODEL,
                "parsed": self._get_fallback_parsed_data(content, content_type)
            }
    
    def _parse_llm_analysis(self, analysis_text: str) -> dict:
        """Parse LLM analysis text to extract structured data"""
        import re
        
        # Extract risk level
        risk_match = re.search(r'\*\*Risk Level\*\*:\s*(CRITICAL|HIGH|MEDIUM|LOW)', analysis_text, re.IGNORECASE)
        risk_level = risk_match.group(1).upper() if risk_match else "MEDIUM"
        
        # Extract risk score
        score_match = re.search(r'\*\*Risk Score\*\*:\s*(\d+)', analysis_text)
        risk_score = int(score_match.group(1)) if score_match else 50
        
        # Extract anomaly score
        anomaly_match = re.search(r'\*\*Anomaly Score\*\*:\s*(\d+)', analysis_text)
        anomaly_score = int(anomaly_match.group(1)) if anomaly_match else 0
        
        # Extract risk category
        category_match = re.search(r'\*\*Risk Category\*\*:\s*([^\n]+)', analysis_text)
        category = category_match.group(1).strip() if category_match else "Unknown"
        
        # Extract anomalies (bullet points under Detected Anomalies)
        anomalies = []
        anomaly_section = re.search(r'\*\*Detected Anomalies\*\*:(.*?)(?=\*\*|##|$)', analysis_text, re.DOTALL)
        if anomaly_section:
            anomalies = [line.strip('• ').strip() for line in anomaly_section.group(1).split('\n') 
                        if line.strip().startswith('•')]
        
        # Extract risk factors
        factors = []
        factor_section = re.search(r'\*\*Risk Factors\*\*:(.*?)(?=##|$)', analysis_text, re.DOTALL)
        if factor_section:
            factors = [line.strip('• ').strip() for line in factor_section.group(1).split('\n') 
                      if line.strip().startswith('•')]
        
        # Extract strategies
        strategies = []
        strategy_section = re.search(r'### Security Strategies(.*?)(?=###|##|$)', analysis_text, re.DOTALL)
        if strategy_section:
            strategies = [line.strip('• ').strip() for line in strategy_section.group(1).split('\n') 
                         if line.strip().startswith('•')]
        
        # Extract incident response
        incident_response = []
        incident_section = re.search(r'### Incident Response(.*?)(?=###|##|$)', analysis_text, re.DOTALL)
        if incident_section:
            incident_response = [line.strip('• ').strip() for line in incident_section.group(1).split('\n') 
                                if line.strip().startswith('•')]
        
        # Extract patterns
        patterns = []
        pattern_match = re.search(r'\*\*Behavioral Patterns\*\*:\s*([^\n]+)', analysis_text)
        if pattern_match:
            patterns = [p.strip() for p in pattern_match.group(1).split(',')]
        
        return {
            "riskAssessment": {
                "level": risk_level,
                "score": risk_score,
                "factors": factors[:10],  # Limit to 10
                "category": category
            },
            "anomalyDetection": {
                "hasAnomalies": len(anomalies) > 0,
                "anomalies": anomalies[:15],  # Limit to 15
                "anomalyScore": anomaly_score,
                "patterns": patterns[:8]  # Limit to 8
            },
            "mitigationRecommendations": {
                "strategies": strategies[:10],
                "incidentResponse": incident_response[:8],
                "policyAlignment": ["NIST CSF", "ISO/IEC 27001", "CIS Controls"]
            }
        }
    
    def _get_fallback_analysis(self, content: str, content_type: str, bert_threat_level: str, bert_confidence: float) -> dict:
        """Provide fallback analysis when LLM is unavailable"""
        return {
            "success": False,
            "analysis": "LLM analysis unavailable - API key not configured. Using BERT model results only.",
            "error": "OPENROUTER_API_KEY not set in .env file",
            "model": PRIMARY_MODEL,
            "parsed": self._get_fallback_parsed_data(content, content_type)
        }
    
    def _get_fallback_parsed_data(self, content: str, content_type: str) -> dict:
        """Generate basic fallback data when LLM is unavailable"""
        return {
            "riskAssessment": {
                "level": "MEDIUM",
                "score": 50,
                "factors": ["LLM unavailable - limited analysis"],
                "category": "Unknown"
            },
            "anomalyDetection": {
                "hasAnomalies": False,
                "anomalies": [],
                "anomalyScore": 0,
                "patterns": []
            },
            "mitigationRecommendations": {
                "strategies": ["Configure OPENROUTER_API_KEY for detailed analysis"],
                "incidentResponse": ["Use BERT model results as preliminary indicator"],
                "policyAlignment": []
            }
        }
    
    def analyze_dual(self, content: str, content_type: str, bert_threat_level: str, bert_confidence: float) -> dict:
        """
        Perform dual LLM analysis using both DeepSeek and Gemini models.
        Returns combined insights from both models.
        
        Args:
            content: The content to analyze
            content_type: Type of content
            bert_threat_level: Threat level from BERT
            bert_confidence: Confidence from BERT
            
        Returns:
            dict with 'primary', 'secondary', and 'consensus' analyses
        """
        if not self.is_configured:
            return {
                "primary": {"success": False, "analysis": "LLM unavailable", "model": PRIMARY_MODEL},
                "secondary": {"success": False, "analysis": "LLM unavailable", "model": SECONDARY_MODEL},
                "consensus": "LLM analysis unavailable - API key not configured"
            }
        
        # Run primary analysis (DeepSeek)
        primary_result = self.analyze(content, content_type, bert_threat_level, bert_confidence)
        
        # Run secondary analysis (Gemini)
        secondary_result = self._analyze_with_model(
            content, content_type, bert_threat_level, bert_confidence, SECONDARY_MODEL
        )
        
        # Generate consensus
        consensus = self._generate_consensus(primary_result, secondary_result)
        
        return {
            "primary": primary_result,
            "secondary": secondary_result,
            "consensus": consensus
        }
    
    def _analyze_with_model(self, content: str, content_type: str, 
                           bert_threat_level: str, bert_confidence: float, model: str) -> dict:
        """Run analysis with a specific model"""
        user_prompt = f"""Analyze the following {content_type.upper()} for potential phishing or social engineering threats.

**Content to analyze:**
```
{content[:3000]}  
```

**BERT Model Pre-analysis:**
- Threat Level: {bert_threat_level.upper()}
- Confidence: {bert_confidence}%

Please provide your expert cybersecurity analysis of this content."""

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000,
                temperature=0.3,
                extra_headers={
                    "HTTP-Referer": "https://spear-ai.local",
                    "X-Title": "SPEAR AI Security Analyzer"
                }
            )
            
            return {
                "success": True,
                "analysis": response.choices[0].message.content,
                "model": model
            }
        except Exception as e:
            return {
                "success": False,
                "analysis": f"Analysis failed: {str(e)}",
                "error": str(e),
                "model": model
            }
    
    def _generate_consensus(self, primary: dict, secondary: dict) -> str:
        """Generate consensus from both LLM analyses"""
        if not primary.get("success") or not secondary.get("success"):
            if primary.get("success"):
                return f"Based on primary analysis: {primary['analysis'][:200]}..."
            elif secondary.get("success"):
                return f"Based on secondary analysis: {secondary['analysis'][:200]}..."
            else:
                return "Both LLM analyses failed"
        
        # Simple consensus: highlight agreement
        consensus = f"""**Dual LLM Consensus:**

Both {PRIMARY_MODEL.split('/')[-1]} and {SECONDARY_MODEL.split('/')[-1]} models have analyzed this content. 

✓ Primary Model (DeepSeek): Provides detailed threat analysis focusing on sophisticated attack patterns.
✓ Secondary Model (Gemini): Offers complementary perspective on security indicators.

Review both analyses below for comprehensive security assessment."""
        
        return consensus
    
    def is_available(self) -> bool:
        """Check if LLM analyzer is available"""
        return self.is_configured


# Singleton instance
llm_analyzer = LLMAnalyzer()

