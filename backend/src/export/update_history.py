"""Helpers to append new records to the global history."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

HISTORY_PATH = Path("data/input/historiques/historique_global.csv")


def update_history(df: pd.DataFrame, path: Path | str | None = None) -> str:
    """Append the new classified rows to the global history CSV."""
    history_path = Path(path) if path else HISTORY_PATH
    history_path.parent.mkdir(parents=True, exist_ok=True)
    if not history_path.exists():
        print("⚠️ Historique non trouvé → création.")
        df.to_csv(history_path, index=False)
        return str(history_path)
    existing = pd.read_csv(history_path, dtype=str).fillna("")
    combined = pd.concat([existing, df], ignore_index=True)
    combined.drop_duplicates(subset=["CIP", "Libelle"], keep="last", inplace=True)
    combined.to_csv(history_path, index=False)
    print("📚 Historique mis à jour.")
    return str(history_path)
