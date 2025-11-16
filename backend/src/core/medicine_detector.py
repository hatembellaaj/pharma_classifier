"""Regex-based medicine detection."""
from __future__ import annotations

import re

from config.constants import MEDICINE_HINTS

MEDICINE_REGEX = re.compile(
    r"\b(" + r"|".join(MEDICINE_HINTS) + r")\b", re.IGNORECASE
)


def is_medicine_by_label(label: str) -> bool:
    """Detect if a product label looks like a medicine."""
    if not isinstance(label, str):
        return False
    return bool(MEDICINE_REGEX.search(label))
