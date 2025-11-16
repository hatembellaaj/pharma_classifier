"""Helpers related to the historique CSV schema."""
from __future__ import annotations

import unicodedata

import pandas as pd

from config.constants import EXPECTED_COLUMNS


def _slugify(name: str) -> str:
    """Return a lowercase/ASCII/underscore-only version of *name*."""

    if not isinstance(name, str):
        return ""
    normalized = unicodedata.normalize("NFKD", name)
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    normalized = normalized.lower()
    for token in (" ", "-", ".", "/", "\\"):
        normalized = normalized.replace(token, "_")
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    return normalized.strip("_")


HISTORY_COLUMN_ALIASES = {
    "cip": "CIP",
    "cip13": "CIP",
    "cip_13": "CIP",
    "code_cip": "CIP",
    "libelle": "Libelle",
    "libelle_long": "Libelle",
    "libelle_court": "Libelle",
    "libelle_produit": "Libelle",
    "libellé": "Libelle",
    "produit": "Libelle",
    "designation": "Libelle",
    "marque": "Marque",
    "univers": "Univers",
    "famille": "Famille",
    "tablette": "Tablette",
    "tablettes": "Tablette",
    "tablette_consolidee": "Tablette_consolidee",
    "tablette_consolidée": "Tablette_consolidee",
    "tablette_consolidees": "Tablette_consolidee",
    "tablette consolidée": "Tablette_consolidee",
    "tablette consolidee": "Tablette_consolidee",
}


def normalize_history_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Return *df* with canonical column names expected by the backend."""

    if df is None or df.empty:
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    rename_map: dict[str, str] = {}
    for column in df.columns:
        key = _slugify(column)
        if key in HISTORY_COLUMN_ALIASES:
            rename_map[column] = HISTORY_COLUMN_ALIASES[key]

    normalized = df.rename(columns=rename_map)

    for column in EXPECTED_COLUMNS:
        if column not in normalized.columns:
            normalized[column] = ""

    ordered_columns = EXPECTED_COLUMNS + [
        column for column in normalized.columns if column not in EXPECTED_COLUMNS
    ]

    return normalized[ordered_columns].fillna("")


__all__ = ["normalize_history_dataframe"]
