"""Fuzzy matching against historical classification records."""
from __future__ import annotations

from dataclasses import dataclass

from ..utils import fuzzy


@dataclass
class MatchResult:
    label: str
    score: float


class HistoricalMatcher:
    def __init__(self, history_index: dict[str, str] | None = None) -> None:
        self.history_index = history_index or {}

    def match(self, text: str) -> MatchResult | None:
        if not self.history_index:
            return None
        best_label, best_score = None, 0.0
        for candidate, label in self.history_index.items():
            score = fuzzy.similarity(text, candidate)
            if score > best_score:
                best_label, best_score = label, score
        if best_label is None:
            return None
        return MatchResult(label=best_label, score=best_score)
