# SPEAR AI Backend - Phishing Detection API

This backend uses the `ealvaradob/bert-finetuned-phishing` BERT model from Hugging Face to detect phishing attempts in URLs, emails, and SMS messages.

## Project Structure

```
backend/
├── main.py              # FastAPI application and routes
├── schemas.py           # Pydantic request/response models
├── requirements.txt     # Python dependencies
├── start.py             # Startup script with dependency check
├── env.example          # Example environment variables
├── .env                 # Your API keys (create this)
└── models/
    ├── __init__.py
    ├── phishing_model.py    # BERT model wrapper class
    └── llm_analyzer.py      # LLM analysis using OpenRouter
```

## LLM Analysis Setup

The app uses [OpenRouter](https://openrouter.ai/) with DeepSeek V3.1 Nex N1 for detailed security analysis.

1. Get an API key from https://openrouter.ai/keys
2. Create a `.env` file in the backend folder:
   ```
   copy env.example .env
   ```
3. Add your API key to `.env`:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

The LLM acts as a cybersecurity analyst and provides:
- Threat assessment and red flags
- Attack technique identification
- Risk level evaluation
- Security recommendations

## Quick Start (Recommended)

From the project root, just run:

```bash
npm run dev
```

This will automatically:
1. Create a Python virtual environment (`backend/venv/`) if it doesn't exist
2. Install all dependencies in the venv
3. Start the backend server (port 8000)
4. Start the frontend dev server (port 5173)

## Manual Setup

### 1. Run the startup script

```bash
cd backend
python start.py
```

This will automatically create the venv and install dependencies.

### 2. Or set up manually

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## Available npm Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start both backend and frontend |
| `npm run backend` | Start only the backend server |
| `npm run frontend` | Start only the frontend dev server |
| `npm run build` | Build frontend for production |

## API Endpoints

### POST /analyze
Analyze content for phishing/social engineering threats using BERT model.

**Request Body:**
```json
{
  "content": "Your URL, email, or SMS content here",
  "content_type": "url" | "email" | "sms"
}
```

**Response:**
```json
{
  "threatLevel": "safe" | "suspicious" | "malicious",
  "confidenceScore": 95.5,
  "rawLabel": "phishing",
  "rawScore": 0.955,
  "llmAnalysis": {
    "success": true,
    "analysis": "**Threat Assessment**: This content shows signs of...",
    "model": "nex-agi/deepseek-v3.1-nex-n1:free",
    "error": null
  },
  "contentType": "URL" | "EMAIL" | "SMS",
  "timestamp": "2025-12-16 10:30:00",
  "processingTime": 150
}
```

### GET /health
Health check endpoint.

### GET /docs
Interactive API documentation (Swagger UI).

## Model Information

- **Model**: `ealvaradob/bert-finetuned-phishing`
- **Type**: BERT-based text classification
- **Task**: Binary classification (phishing vs legitimate)
- **Source**: [Hugging Face](https://huggingface.co/ealvaradob/bert-finetuned-phishing)

## Notes

- First startup will download the model (~440MB) from Hugging Face
- GPU will be used automatically if CUDA is available
- The API combines BERT model predictions with pattern-based analysis for more comprehensive detection

