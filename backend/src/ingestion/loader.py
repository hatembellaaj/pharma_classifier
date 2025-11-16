"""Utilities for loading CSV inputs into pandas dataframes."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


class CSVLoader:
    """Loads CSV files with consistent options."""

    def __init__(self, *, encoding: str = "utf-8", sep: str = ";") -> None:
        self.encoding = encoding
        self.sep = sep

    def load(self, path: str | Path) -> pd.DataFrame:
        df = pd.read_csv(path, encoding=self.encoding, sep=self.sep)
        df.columns = [col.strip().lower() for col in df.columns]
        return df

    def load_many(self, paths: Iterable[str | Path]) -> list[pd.DataFrame]:
        return [self.load(path) for path in paths]
