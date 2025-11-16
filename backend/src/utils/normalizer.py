"""Text normalization helpers."""
from __future__ import annotations

import unicodedata


def normalize(text: str) -> str:
    return unicodedata.normalize("NFKC", text).strip().lower()
