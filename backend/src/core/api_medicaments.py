"""Client helper for fr.gouv.medicaments REST API with a simple cache."""
from __future__ import annotations

import json
import os
from typing import Any

import requests

from config import settings

BASE_URL = settings.API_MEDICAMENTS_BASE
CACHE_FILE = settings.CACHE_DIR / "medicaments_cache.json"
if CACHE_FILE.exists():
    try:
        CACHE = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        CACHE = {}
else:
    CACHE: dict[str, Any] = {}


def save_cache() -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(CACHE, indent=2), encoding="utf-8")


def search_by_cip(cip: str) -> Any:
    """Query the API for a given CIP using a local cache."""
    normalized_cip = str(cip).strip()
    if not normalized_cip:
        return None
    if normalized_cip in CACHE:
        return CACHE[normalized_cip]
    url = f"{BASE_URL}/search"
    try:
        response = requests.get(url, params={"query": normalized_cip}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            CACHE[normalized_cip] = data
            save_cache()
            return data
    except requests.RequestException:
        return None
    return None


def is_medicine_by_api(cip: str) -> bool:
    data = search_by_cip(cip)
    if not data:
        return False
    text = json.dumps(data).lower()
    keywords = ["denomination", "formepharmaceutique", "substance", "amm"]
    return any(keyword in text for keyword in keywords)
