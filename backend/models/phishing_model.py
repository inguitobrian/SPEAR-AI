"""
BERT-based Phishing Detection Model
Uses ealvaradob/bert-finetuned-phishing from Hugging Face
"""

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from dataclasses import dataclass


@dataclass
class PredictionResult:
    """Result from the phishing detection model"""
    raw_label: str
    raw_score: float
    is_phishing: bool
    confidence: float


class PhishingDetector:
    """
    BERT-based phishing detection model wrapper.
    Loads and manages the Hugging Face model for phishing classification.
    """
    
    MODEL_NAME = "ealvaradob/bert-finetuned-phishing"
    MAX_CONTENT_LENGTH = 2000  # Character limit for model input
    
    # Labels that indicate phishing content
    PHISHING_LABELS = ['phishing', 'spam', 'malicious', '1', 'label_1']
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.classifier = None
        self.is_loaded = False
        self.device = "GPU" if torch.cuda.is_available() else "CPU"
    
    def load(self) -> None:
        """Load the BERT model from Hugging Face"""
        print(f"Loading BERT phishing detection model: {self.MODEL_NAME}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_NAME)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.MODEL_NAME)
            self.classifier = pipeline(
                "text-classification",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if torch.cuda.is_available() else -1,
                truncation=True,  # Auto-truncate inputs longer than 512 tokens
                max_length=512
            )
            self.is_loaded = True
            print(f"Model loaded successfully! Using {self.device}")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise e
    
    def predict(self, content: str) -> PredictionResult:
        """
        Run phishing detection on the given content.
        
        Args:
            content: Text content to analyze (URL, email, or SMS)
            
        Returns:
            PredictionResult with classification details
            
        Raises:
            RuntimeError: If model is not loaded
            Exception: If inference fails
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load() first.")
        
        # Truncate content if too long for the model (max 512 tokens)
        truncated_content = content[:self.MAX_CONTENT_LENGTH]
        
        # Run inference
        result = self.classifier(truncated_content)[0]
        
        raw_label = result['label']
        raw_score = result['score']
        
        # Determine if content is phishing based on model output
        is_phishing = raw_label.lower() in self.PHISHING_LABELS
        confidence = raw_score * 100
        
        return PredictionResult(
            raw_label=raw_label,
            raw_score=raw_score,
            is_phishing=is_phishing,
            confidence=confidence
        )
    
    def is_gpu_available(self) -> bool:
        """Check if GPU is available for inference"""
        return torch.cuda.is_available()


# Singleton instance for the application
phishing_detector = PhishingDetector()

