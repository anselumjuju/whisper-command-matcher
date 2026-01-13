from glob import translate

from fastapi import FastAPI, UploadFile, File, Query
from faster_whisper import WhisperModel
import tempfile
import os
from command_matcher import detect_action_fuzzy

app = FastAPI(title="Voice Command Backend")

# -----------------------------
# Load Whisper model (CPU)
# -----------------------------
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

# -----------------------------
# Action detection logic
# -----------------------------
def detect_action(text: str):
    t = text.lower()

    # Power
    if any(k in t for k in ["turn on", "switch on", "power on", "encender", "piztu"]):
        return {"type": "POWER", "value": "ON"}

    if any(k in t for k in ["turn off", "switch off", "power off", "apagar", "itzali"]):
        return {"type": "POWER", "value": "OFF"}

    # Brightness
    if any(k in t for k in ["brighter", "increase brightness", "más brillo", "argiago"]):
        return {"type": "BRIGHTNESS", "value": "UP"}

    if any(k in t for k in ["dimmer", "decrease brightness", "menos brillo", "ilunago"]):
        return {"type": "BRIGHTNESS", "value": "DOWN"}

    # Colors
    colors = {
        "green": ["green", "verde", "berde"],
        "red": ["red", "rojo", "gorri"],
        "blue": ["blue", "azul", "urdin"],
        "white": ["white", "blanco", "zuri"],
        "yellow": ["yellow", "amarillo", "hori"],
        "purple": ["purple", "morado", "more"]
    }

    for color, keywords in colors.items():
        if any(k in t for k in keywords):
            return {"type": "COLOR", "value": color.upper()}

    return {"type": "UNKNOWN", "value": None}


# -----------------------------
# Transcription endpoint
# -----------------------------
@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
        lang: str = Query("en", description="en | es | eu")
):
    # Save uploaded audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # Transcribe audio
        segments, info = model.transcribe(
            tmp_path,
        )

        text = " ".join(segment.text.strip() for segment in segments)

        # Detect action
        match = detect_action_fuzzy(text)

        return {
            "success": True,
            "text": text,
            "language" : lang,
            "action": match["action"],
            "confidence": match["score"],
            "matched": match["matched"]
        }

    finally:
        # Clean up temp file
        os.remove(tmp_path)


# -----------------------------
# Health check
# -----------------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "Whisper backend running"}
