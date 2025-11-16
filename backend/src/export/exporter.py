"""CSV export helpers."""
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd


def export_results(df: pd.DataFrame, path: str | os.PathLike[str]) -> str:
    """Persist the classified dataframe to the requested path."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"📦 Fichier exporté : {output_path}")
    return str(output_path)
