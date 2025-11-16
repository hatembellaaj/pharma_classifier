"""Post-processing utilities for classifier outputs."""
from __future__ import annotations

from .ai_classifier import ClassificationResult


class CategoryAssigner:
    def __init__(self, *, default_category: str) -> None:
        self.default_category = default_category

    def assign(self, result: ClassificationResult | None) -> str:
        if result is None:
            return self.default_category
        return result.label or self.default_category
