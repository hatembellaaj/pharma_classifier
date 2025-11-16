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

    dedupe_keys = [col for col in ("CIP", "Libelle") if col in combined.columns]
    if dedupe_keys:
        combined.drop_duplicates(subset=dedupe_keys, keep="last", inplace=True)
    else:
        print(
            "⚠️ Colonnes de déduplication absentes (CIP/Libelle) → historisation sans filtre."
        )
    combined.to_csv(history_path, index=False)
    print("📚 Historique mis à jour.")
    return str(history_path)
