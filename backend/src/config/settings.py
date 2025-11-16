"""Project-wide settings sourced from environment variables."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
API_MEDICAMENTS_BASE = os.getenv(
    "API_MEDICAMENTS_BASE", "https://fr.gouv.medicaments.rest/api/medicaments"
)
DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
UPLOAD_DIR = DATA_DIR / "uploaded"
OUTPUT_DIR = DATA_DIR / "output" / "v2"
HISTORY_PATH = DATA_DIR / "input" / "historiques" / "historique_global.csv"
CACHE_DIR = DATA_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
