"""Client helper for the public BDPM API with a simple cache and logging."""
from __future__ import annotations

import json
from typing import Any, Iterable
from urllib.parse import quote

import requests

from config import settings
from utils.logger import log

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


def _log_rate_limit(headers: dict[str, Any]) -> None:
    limit = headers.get("X-RateLimit-Limit")
    remaining = headers.get("X-RateLimit-Remaining")
    rate = headers.get("X-RateLimit-Rate")
    if any((limit, remaining, rate)):
        log(
            "   ↪ Rate limit : "
            + ", ".join(
                part
                for part in [
                    f"limite={limit}" if limit else "",
                    f"reste={remaining}" if remaining else "",
                    f"recharge={rate}/s" if rate else "",
                ]
                if part
            )
        )


def search_by_cip(cip: str, label: str | None = None) -> Any:
    """Query the BDPM API for a given CIP or label using a local cache."""

    normalized_cip = str(cip).strip() if cip is not None else ""
    if normalized_cip.lower() in {"nan", "none"}:
        normalized_cip = ""
    normalized_digits = _normalize_digits(normalized_cip)
    normalized_label = label.strip() if isinstance(label, str) else ""
    cache_keys: list[str] = []
    if normalized_cip:
        cache_keys.append(f"cip:{normalized_cip}")
    if normalized_label:
        cache_keys.append(f"label:{normalized_label.lower()}")
    for cache_key in cache_keys:
        if cache_key in CACHE:
            log(f"🔁 API BDPM : utilisation du cache pour {cache_key}")
            return CACHE[cache_key]

    attempts: list[tuple[str, str]] = []
    if normalized_digits:
        if len(normalized_digits) <= 9:
            attempts.append(
                (f"cis {normalized_digits}", f"{BASE_URL}/medicament/id/{normalized_digits}")
            )
        attempts.append(
            (f"terme {normalized_digits}", f"{BASE_URL}/medicament/{quote(normalized_digits)}")
        )
    if normalized_label:
        attempts.append((f"nom {normalized_label}", f"{BASE_URL}/medicament/{quote(normalized_label)}"))

    if not attempts:
        log("🔁 API BDPM ignorée : aucun CIP ou libellé exploitable")
        return None

    last_payload: Any = None
    for descriptor, url in attempts:
        try:
            log(f"🌐 API BDPM : requête {descriptor} en cours")
            response = requests.get(url, timeout=10)
            _log_rate_limit(response.headers)
            log(f"🌐 API BDPM : réponse HTTP {response.status_code} pour {descriptor}")
            if response.status_code == 200:
                payload = response.json()
                log(
                    f"🌐 API BDPM : payload {descriptor} → "
                    f"{summarize_payload(payload)}"
                )
                cache_key = cache_keys[0] if cache_keys else descriptor
                CACHE[cache_key] = payload
                save_cache()
                return payload
            if response.status_code == 404:
                log(f"   ↪ API BDPM : aucun médicament trouvé pour {descriptor}")
            else:
                log(
                    "   ↪ API BDPM : réponse inattendue "
                    f"{response.status_code} pour {descriptor}"
                )
            last_payload = None
        except requests.RequestException as exc:
            log(f"⚠️ API BDPM : erreur réseau pour {descriptor} → {exc}")
            last_payload = None
    return last_payload


def is_medicine_payload(payload: Any) -> bool:
    """Heuristically check whether *payload* describes a medicine."""

    if not payload:
        return False
    try:
        text = json.dumps(payload).lower()
    except (TypeError, ValueError):
        return False
    keywords = [
        "cis",
        "denomination",
        "formepharmaceutique",
        "substance",
        "voiesadministration",
        "amm",
    ]
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
        presentations = payload.get("presentations") or payload.get("presentation")
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
    code_keys = ("codeCIP13", "codeCIP7", "cip13", "cip7", "cip")
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
