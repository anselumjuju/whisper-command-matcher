import re
from difflib import SequenceMatcher
from typing import Optional, Dict


# -----------------------------
# Helpers
# -----------------------------
def normalize(text: str) -> str:
    """
    Normalize text for matching:
    - lowercase
    - remove spaces
    - remove punctuation
    """
    text = text.lower()
    text = re.sub(r"[^\w]", "", text)
    return text


def similarity(a: str, b: str) -> float:
    """
    Returns similarity between two strings (0–1)
    """
    return SequenceMatcher(None, a, b).ratio()


# -----------------------------
# Command definitions
# Easy to extend later
# -----------------------------


COMMANDS = [
    # -----------------------------
    # Power ON
    # -----------------------------
    {
        "action": {"type": "POWER", "value": "ON"},
        "phrases": {
            "en": [
                "turn on the light",
                "switch on the light",
                "turn the light on",
                "light on"
            ],
            "es": [
                "encender la luz",
                "prender la luz",
                "enciende la luz"
            ],
            "eu": [
                "eusebio piztu argia",
                "eusebio pistoardia",
                "piztu argia",
                "argia piztu"
            ]
        }
    },

    # -----------------------------
    # Power OFF
    # -----------------------------
    {
        "action": {"type": "POWER", "value": "OFF"},
        "phrases": {
            "en": [
                "turn off the light",
                "switch off the light",
                "turn the light off",
                "light off"
            ],
            "es": [
                "apagar la luz",
                "apaga la luz"
            ],
            "eu": [
                "eusebio itzali argia",
                "eusebio, italii arvija.",
                "itzali argia",
                "argia itzali"
            ]
        }
    },

    # -----------------------------
    # Brightness UP
    # -----------------------------
    {
        "action": {"type": "BRIGHTNESS", "value": "UP"},
        "phrases": {
            "en": [
                "make the light brighter",
                "increase brightness",
                "more light"
            ],
            "es": [
                "más brillo",
                "aumentar brillo",
                "más luz"
            ],
            "eu": [
                "eusebio argi gehiago",
                "eusebio ardile yago",
                "argi gehiago"
            ]
        }
    },

    # -----------------------------
    # Brightness DOWN
    # -----------------------------
    {
        "action": {"type": "BRIGHTNESS", "value": "DOWN"},
        "phrases": {
            "en": [
                "make the light darker",
                "decrease brightness",
                "less light"
            ],
            "es": [
                "menos brillo",
                "reducir brillo",
                "menos luz"
            ],
            "eu": [
                "eusebio argi gutxiago",
                "argi gutxiago",
                "eusebio arribuciavo",
                "eusebio argi gutxiago"
            ]
        }
    },

    # -----------------------------
    # Change Lamp Model
    # -----------------------------
    {
        "action": {"type": "MODEL", "value": "CHANGE"},
        "phrases": {
            "en": [
                "change the lamp model",
                "switch the lamp model",
                "change model"
            ],
            "es": [
                "cambiar el modelo de la lámpara",
                "cambiar modelo"
            ],
            "eu": [
                "eusebio aldatu lanpara",
                "eusebio aldatulam paramota.",
                "lanpara aldatu"
            ]
        }
    },

    # -----------------------------
    # Blue Light
    # -----------------------------
    {
        "action": {"type": "COLOR", "value": "BLUE"},
        "phrases": {
            "en": [
                "switch on blue light",
                "blue light",
                "turn on blue light"
            ],
            "es": [
                "luz azul",
                "enciende la luz azul"
            ],
            "eu": [
                "eusebio piztu argi urdina",
                "eusebio pistuardi-urdiña.",
                "argi urdina piztu"
            ]
        }
    },

    # -----------------------------
    # Green Light
    # -----------------------------
    {
        "action": {"type": "COLOR", "value": "GREEN"},
        "phrases": {
            "en": [
                "switch on green light",
                "green light",
                "turn on green light"
            ],
            "es": [
                "luz verde",
                "enciende la luz verde"
            ],
            "eu": [
                "eusebio piztu argi berdea",
                "eusebio pistuardi verdea",
                "argi berdea piztu"
            ]
        }
    },

    # -----------------------------
    # Red Light
    # -----------------------------
    {
        "action": {"type": "COLOR", "value": "RED"},
        "phrases": {
            "en": [
                "switch on red light",
                "red light",
                "turn on red light"
            ],
            "es": [
                "luz roja",
                "enciende la luz roja"
            ],
            "eu": [
                "eusebio piztu argi gorria",
                "eusebio pistuardi gorria",
                "argi gorria piztu"
            ]
        }
    },
]


# -----------------------------
# Main matcher
# -----------------------------
def detect_action_fuzzy(
    transcript: str,
    threshold: float = 0.80
) -> Dict:
    """
    Detect the best matching action using fuzzy matching.
    Returns UNKNOWN if nothing matches above threshold.
    """

    normalized_input = normalize(transcript)

    best_match: Optional[Dict] = None
    best_score = 0.0

    for command in COMMANDS:
        for lang, phrases in command["phrases"].items():
            for phrase in phrases:
                score = similarity(
                    normalized_input,
                    normalize(phrase)
                )

                if score > best_score:
                    best_score = score
                    best_match = command["action"]

    if best_match and best_score >= threshold:
        return {
            "matched": True,
            "score": round(best_score, 2),
            "action": best_match
        }

    return {
        "matched": False,
        "score": round(best_score, 2),
        "action": {"type": "UNKNOWN", "value": None}
    }
