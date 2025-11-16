"""Placeholder AI classifier abstraction."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ClassificationResult:
    label: str
    confidence: float


class AIClassifier:
    def __init__(self, *, model_path: str) -> None:
        self.model_path = model_path

    def predict(self, text: str) -> ClassificationResult:
        # Placeholder rule to keep the example self-contained
        score = min(len(text) / 100, 1.0)
        label = "pharma" if score > 0.5 else "autre"
        return ClassificationResult(label=label, confidence=score)
