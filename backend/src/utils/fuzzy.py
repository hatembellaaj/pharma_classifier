"""Simple fuzzy similarity helpers."""
from __future__ import annotations

from difflib import SequenceMatcher


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(a=a.lower(), b=b.lower()).ratio()
