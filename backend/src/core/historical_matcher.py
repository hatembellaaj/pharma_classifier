"""Fuzzy matching helpers against the historique CSV."""
from __future__ import annotations

import pandas as pd

from config import constants
from utils import fuzzy


def match_in_history(label: str, historique: pd.DataFrame) -> pd.Series | None:
    if historique is None or historique.empty:
        return None
    best_idx = None
    best_score = 0
    for idx, row in historique.iterrows():
        candidate = row.get("Libelle", "")
        score = fuzzy.fuzzy_score(label, candidate)
        if score > best_score:
            best_idx = idx
            best_score = score
    if best_idx is None:
        return None
    if best_score < constants.HISTORY_MATCH_THRESHOLD * 100:
        return None
    return historique.loc[best_idx]
