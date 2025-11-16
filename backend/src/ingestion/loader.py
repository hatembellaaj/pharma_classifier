"""CSV loading utilities."""
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd


def load_inputs(path: str | os.PathLike[str]) -> list[pd.DataFrame]:
    """Load every CSV file in *path* and return a list of DataFrames."""
    folder = Path(path)
    folder.mkdir(parents=True, exist_ok=True)
    files = sorted(f for f in folder.iterdir() if f.suffix.lower() == ".csv")
    if not files:
        print(f"⚠️ Aucun fichier CSV trouvé dans {folder}")
        return []
    datasets: list[pd.DataFrame] = []
    for file in files:
        print(f"📄 Chargement : {file}")
        df = pd.read_csv(file, dtype=str).fillna("")
        datasets.append(df)
    return datasets
