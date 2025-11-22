"""Project-wide settings sourced from environment variables."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

# Try loading from the current working directory first (e.g., when the app is started
# from the repo root), then fall back to searching relative to this file so deployments
# running from a different workdir still locate the shared .env.
env_path = find_dotenv(usecwd=True)
if not env_path:
    env_path = find_dotenv()

load_dotenv(env_path, override=False)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
API_MEDICAMENTS_BASE = os.getenv(
    "API_MEDICAMENTS_BASE", "https://medicaments-api.giygas.dev"
)
DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
UPLOAD_DIR = DATA_DIR / "uploaded"
OUTPUT_DIR = DATA_DIR / "output" / "v2"
LOG_PATH = DATA_DIR / "logs" / "pipeline.log"
HISTORY_PATH = DATA_DIR / "input" / "historiques" / "historique_global.csv"
REFERENCE_CATALOG_PATH = DATA_DIR / "input" / "referentiels" / "referentiel_categories.csv"
CACHE_DIR = DATA_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
