"""Input dataframe schema validation."""
from __future__ import annotations

import pandas as pd

from config.constants import EXPECTED_COLUMNS


def validate_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure the dataframe contains the expected officine columns."""
    missing = [column for column in EXPECTED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"⛔ Colonnes manquantes : {missing}")
    return df
