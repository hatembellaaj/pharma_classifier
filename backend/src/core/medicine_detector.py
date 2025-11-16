"""Rule-based medicine detection using regexes."""
from __future__ import annotations

import re
from dataclasses import dataclass

MEDICINE_REGEX = re.compile(r"\b(?:mg|gélule|comprimé|sirop)\b", flags=re.IGNORECASE)


@dataclass
class DetectionResult:
    has_medicine: bool
    matches: list[str]


def detect(text: str) -> DetectionResult:
    matches = MEDICINE_REGEX.findall(text)
    return DetectionResult(has_medicine=bool(matches), matches=matches)
