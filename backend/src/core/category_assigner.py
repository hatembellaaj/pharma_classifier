"""Helpers to apply deterministic categories to dataframe rows."""
from __future__ import annotations

import json
from typing import Any

import pandas as pd

from config.constants import FORCED_MEDICINE_CATEGORIES


def force_medicine_categories(row: pd.Series) -> pd.Series:
    new_row = row.copy()
    for column, value in FORCED_MEDICINE_CATEGORIES.items():
        new_row[column] = value
    labo = row.get("LABO", "") if isinstance(row, pd.Series) else ""
    if (not str(new_row.get("Marque", "")).strip()) and labo:
        new_row["Marque"] = labo
    new_row["Classification_source"] = "MEDICAMENT"
    return new_row


def _parse_ai_payload(payload: Any) -> dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return {}
    return {}


def apply_ai_classification(row: pd.Series, payload: Any) -> pd.Series:
    data = _parse_ai_payload(payload)
    new_row = row.copy()
    for field in ["Marque", "Univers", "Famille", "Tablette", "Tablette_consolidee"]:
        if field in data and data[field]:
            new_row[field] = data[field]
    labo = row.get("LABO", "") if isinstance(row, pd.Series) else ""
    if (not str(new_row.get("Marque", "")).strip()) and labo:
        new_row["Marque"] = labo
    new_row["Classification_source"] = "IA"
    return new_row
