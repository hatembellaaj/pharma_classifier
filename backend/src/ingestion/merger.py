"""Merge helper for combining multiple CSV datasets."""
from __future__ import annotations

import pandas as pd


class DataMerger:
    def merge(self, datasets: list[pd.DataFrame]) -> pd.DataFrame:
        if not datasets:
            return pd.DataFrame()
        return pd.concat(datasets, ignore_index=True).drop_duplicates(subset=["id"])
