"""DataFrame helpers for cleaning incoming datasets."""
from __future__ import annotations

import re
from typing import Iterable

import pandas as pd


def _coalesce_frame_columns(frame: pd.DataFrame, columns: Iterable[str]) -> pd.Series:
    """Merge *columns* into a single Series named *target*.

    Values are taken from left to right, keeping the first non-empty/non-null
    entry. Empty strings are treated as missing values and replaced by later
    candidates.
    """

    def _as_missing(value):
        if value is None:
            return None
        if isinstance(value, str) and value.strip() == "":
            return None
        if pd.isna(value):
            return None
        return value

    cleaned = frame[list(columns)].applymap(_as_missing)
    merged = cleaned.bfill(axis=1).iloc[:, 0]
    return merged.fillna("")


def coalesce_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return *df* with duplicate column suffixes removed.

    Pandas adds suffixes (e.g., ``.1``) when reading CSV files that contain
    duplicate headers. Those duplicated columns should simply backfill missing
    values in the canonical column instead of creating new columns in the
    exported dataset.
    """

    if df is None or df.empty:
        return pd.DataFrame(df)

    result = df.copy()
    grouped: dict[str, list[str]] = {}
    for column in result.columns:
        base = re.sub(r"\.\d+$", "", column)
        grouped.setdefault(base, []).append(column)

    for base, columns in grouped.items():
        if len(columns) == 1:
            continue
        result[base] = _coalesce_frame_columns(result, columns)
        for duplicate in columns:
            if duplicate != base:
                result.drop(columns=duplicate, inplace=True, errors="ignore")

    return result


__all__ = ["coalesce_duplicate_columns"]
