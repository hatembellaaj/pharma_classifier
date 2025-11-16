"""Text normalization helpers."""
from __future__ import annotations

import unicodedata


def normalize_text(text: str) -> str:
    """Normalize unicode accents, trim spaces and uppercase the payload."""
    if not isinstance(text, str):
        return ""
    normalized = unicodedata.normalize("NFKD", text)
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    normalized = " ".join(normalized.split())
    return normalized.upper()
