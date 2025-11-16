"""Handles exporting latest pipeline outputs."""
from __future__ import annotations

from pathlib import Path

import pandas as pd


class Exporter:
    def __init__(self, history_path: str) -> None:
        self.history_path = Path(history_path)
        self.history_path.parent.mkdir(parents=True, exist_ok=True)

    def save_latest(self, df: pd.DataFrame) -> None:
        output_path = self.history_path.with_suffix(".latest.csv")
        df.to_csv(output_path, index=False)
