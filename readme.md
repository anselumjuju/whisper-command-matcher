# Whisper Command Matcher

This is a **FastAPI backend** that handles **voice commands** for the Lurmis project.

It converts short audio commands (Basque, Spanish, or English) into text using a locally hosted **Whisper** model, then matches the command to a predefined action (power, brightness, color, model change, etc.).

No external APIs, no quotas, and no API keys are required.

---

## What this does

- Accepts an audio file from the frontend
- Detects the spoken language automatically
- Translates commands to English internally
- Matches the command using fuzzy logic
- Returns a structured action for the UI to execute

---

## Tech stack

- FastAPI
- Uvicorn
- faster-whisper (CPU)
- Python 3.10

---

## Project structure

```

whisper-backend/
├── main.py            # FastAPI app
├── command_matcher.py # Command matching logic
├── requirements.txt

````

---

## Run locally

1. Install dependencies
```bash
pip install -r requirements.txt
````

2. Start the server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The Whisper model will download on first run and be reused after that.

---

## API

### POST `/transcribe`

Upload an audio file (`multipart/form-data`, field name: `file`).

Response example:

```json
{
  "success": true,
  "detected_language": "eu",
  "text": "turn on the green light",
  "action": {
    "type": "COLOR",
    "value": "GREEN"
  },
  "confidence": 0.91
}
```

---

### GET `/`

Health check.

---

## Deployment

This service is meant to run as a **long-lived backend**, not serverless.

It is currently designed to be hosted on **Railway** using:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

The model loads once on startup and is reused for all requests.

---