# GenAI ADK Agent on Cloud Run

AI Learning Assistant built with Google Agent Development Kit (ADK), FastAPI, and Gemini. The service exposes a REST endpoint to chat with the agent and is deployable on Google Cloud Run.

## Project Structure

```text
genai-adk-agent/
│
├── agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── tools.py
│   └── config.py
│
├── app/
│   ├── __init__.py
│   └── main.py
│
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## Prerequisites

- Python 3.10+
- Docker
- Google Cloud CLI (`gcloud`)
- A valid Gemini API key in `GOOGLE_API_KEY`

## Local Setup

```bash
cd genai-adk-agent
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create your env file:

```bash
copy .env.example .env
```

Edit `.env` and set:

```bash
GOOGLE_API_KEY=YOUR_REAL_KEY
```

Run locally:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## API

### Health Check

```bash
curl http://localhost:8080/health
```

### Chat Endpoint

```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Teach me the basics of generative AI and suggest tools to practice."}'
```

Expected response shape:

```json
{
  "response": "..."
}
```

## Build Docker Image

```bash
docker build -t adk-agent:latest .
```

Run container locally:

```bash
docker run --rm -p 8080:8080 -e GOOGLE_API_KEY=YOUR_REAL_KEY adk-agent:latest
```

## Deploy to Cloud Run

Use these exact commands:

```bash
gcloud auth login
gcloud config set project PROJECT_ID
gcloud builds submit --tag gcr.io/PROJECT_ID/adk-agent
gcloud run deploy adk-agent \
--image gcr.io/PROJECT_ID/adk-agent \
--platform managed \
--region us-central1 \
--allow-unauthenticated
```

## Test Deployed API

Replace `SERVICE_URL` with your deployed Cloud Run URL.

```bash
curl -X POST SERVICE_URL/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain the difference between prompt engineering and fine-tuning."}'
```
