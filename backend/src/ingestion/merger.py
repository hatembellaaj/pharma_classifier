"""Utilities to merge multiple input datasets."""
from __future__ import annotations

import pandas as pd


def merge_inputs(datasets: list[pd.DataFrame]) -> pd.DataFrame:
    """Merge all CSV inputs into a single dataframe."""
    if not datasets:
        raise ValueError("⚠️ Aucun DataFrame fourni pour la fusion.")
    print("🔄 Fusion des CSV…")
    return pd.concat(datasets, ignore_index=True).fillna("")
