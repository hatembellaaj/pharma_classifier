"""Client helper for fr.gouv.medicaments REST API with a simple cache."""
from __future__ import annotations

import json
from typing import Any, Iterable

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


def is_medicine_payload(payload: Any) -> bool:
    """Heuristically check whether *payload* describes a medicine."""

    if not payload:
        return False
    try:
        text = json.dumps(payload).lower()
    except (TypeError, ValueError):
        return False
    keywords = ["denomination", "formepharmaceutique", "substance", "amm"]
    return any(keyword in text for keyword in keywords)


def _normalize_digits(value: Any) -> str:
    return "".join(char for char in str(value) if char.isdigit())


def _first_value(data: dict[str, Any], keys: Iterable[str]) -> Any:
    for key in keys:
        if key in data and data[key] not in (None, ""):
            return data[key]
    return None


def _as_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        return None


def _iter_presentations(payload: Any) -> Iterable[dict[str, Any]]:
    if isinstance(payload, dict):
        presentations = payload.get("presentations")
        if isinstance(presentations, list):
            for presentation in presentations:
                if isinstance(presentation, dict):
                    yield presentation
        results = payload.get("results")
        if isinstance(results, list):
            for entry in results:
                yield from _iter_presentations(entry)
    elif isinstance(payload, list):
        for item in payload:
            yield from _iter_presentations(item)


def _format_rate(rate: float) -> str:
    if rate.is_integer():
        return f"{int(rate)}%"
    return f"{rate:.1f}%"


def extract_tva_from_payload(payload: Any, target_cip: str | None = None) -> str | None:
    """Return the TVA rate inferred from the API *payload* if present."""

    if not payload:
        return None
    normalized_cip = _normalize_digits(target_cip) if target_cip else ""
    code_keys = ("codeCIP13", "codeCIP7", "cip13", "cip")
    for presentation in _iter_presentations(payload):
        if normalized_cip:
            codes = {_normalize_digits(presentation.get(key, "")) for key in code_keys}
            if normalized_cip and normalized_cip not in codes:
                continue
        rate_value = _first_value(
            presentation,
            ("taux_tva", "tauxTVA", "tva", "tauxTva", "tauxTVA_presentation"),
        )
        rate = _as_float(rate_value)
        if rate is None:
            price_ttc = _as_float(
                _first_value(
                    presentation,
                    ("prix_ttc", "prixTTC", "prix", "prixPublic", "prix_public"),
                )
            )
            price_ht = _as_float(
                _first_value(
                    presentation,
                    ("prix_ht", "prixHT", "prixHorsTaxe", "prix_hors_taxe"),
                )
            )
            if price_ttc and price_ht and price_ht > 0:
                rate = round(((price_ttc / price_ht) - 1) * 100, 1)
        if rate is not None:
            return _format_rate(rate)
    return None


def summarize_payload(payload: Any, limit: int = 600) -> str:
    """Return a human-readable summary of the API response for logging."""

    try:
        serialized = json.dumps(payload, ensure_ascii=False)
    except (TypeError, ValueError):
        serialized = str(payload)
    if len(serialized) <= limit:
        return serialized
    return serialized[: limit - 1] + "…"


def is_medicine_by_api(cip: str) -> bool:
    """Backward-compatible helper preserved for legacy callers."""

    return is_medicine_payload(search_by_cip(cip))
