"""
LLM-based Cybersecurity Analysis
Uses OpenRouter API with DeepSeek V3.1 Nex N1 model
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
MODEL_NAME = "nex-agi/deepseek-v3.1-nex-n1:free"

# System prompt for the cybersecurity analyst
SYSTEM_PROMPT = """You are an expert cybersecurity analyst specializing in phishing detection and social engineering analysis. Your role is to analyze potentially malicious content (URLs, emails, SMS messages) and provide detailed security assessments.

When analyzing content, you should:
1. Identify specific threat indicators and red flags
2. Explain the potential attack vector or technique being used
3. Assess the sophistication level of the threat
4. Provide actionable security recommendations
5. Rate the overall risk level

Be concise but thorough. Focus on practical, actionable insights. If the content appears legitimate, explain why.

Format your response in clear sections:
- **Threat Assessment**: Brief summary of what you found
- **Red Flags Identified**: List specific suspicious elements
- **Attack Technique**: What type of attack this might be (if applicable)
- **Risk Level**: LOW / MEDIUM / HIGH / CRITICAL
- **Recommendations**: What the user should do"""


class LLMAnalyzer:
    """
    LLM-based security analyzer using OpenRouter API.
    Provides detailed cybersecurity analysis of content.
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
            print(f"[OK] LLM Analyzer configured with model: {MODEL_NAME}")
        else:
            print("[!] LLM Analyzer not configured - OPENROUTER_API_KEY not set")
            self.is_configured = False
    
    def analyze(self, content: str, content_type: str, bert_threat_level: str, bert_confidence: float) -> dict:
        """
        Perform LLM-based security analysis on the content.
        
        Args:
            content: The content to analyze (URL, email, or SMS)
            content_type: Type of content ("url", "email", "sms")
            bert_threat_level: Threat level from BERT model
            bert_confidence: Confidence score from BERT model
            
        Returns:
            dict with 'analysis' text and 'success' boolean
        """
        if not self.is_configured:
            return {
                "success": False,
                "analysis": "LLM analysis unavailable - API key not configured",
                "error": "OPENROUTER_API_KEY not set in .env file"
            }
        
        # Build the user prompt with context
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
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000,
                temperature=0.3,  # Lower temperature for more focused analysis
                extra_headers={
                    "HTTP-Referer": "https://spear-ai.local",
                    "X-Title": "SPEAR AI Security Analyzer"
                }
            )
            
            analysis_text = response.choices[0].message.content
            
            return {
                "success": True,
                "analysis": analysis_text,
                "model": MODEL_NAME,
                "tokens_used": response.usage.total_tokens if response.usage else None
            }
            
        except Exception as e:
            return {
                "success": False,
                "analysis": f"LLM analysis failed: {str(e)}",
                "error": str(e)
            }
    
    def is_available(self) -> bool:
        """Check if LLM analyzer is available"""
        return self.is_configured


# Singleton instance
llm_analyzer = LLMAnalyzer()

