"""Fuzzy helper functions using rapidfuzz."""
from __future__ import annotations

from rapidfuzz import fuzz


def fuzzy_score(a: str | None, b: str | None) -> int:
    left = (a or "").lower()
    right = (b or "").lower()
    return int(fuzz.token_sort_ratio(left, right))
