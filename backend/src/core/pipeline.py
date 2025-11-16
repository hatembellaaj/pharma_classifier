"""Pipeline principal de classification pharmaceutique."""
from __future__ import annotations

import pandas as pd

from typing import Optional

from core.api_medicaments import is_medicine_by_api
from core.ai_classifier import classify_with_ai
from core.category_assigner import apply_ai_classification, force_medicine_categories
from core.historical_matcher import match_in_history
from core.medicine_detector import is_medicine_by_label
from config import settings
from utils.progress_log import ProgressLog


def run_pipeline(df: pd.DataFrame, progress_logger: Optional[ProgressLog] = None) -> pd.DataFrame:
    """Exécute les 4 étapes clés du pipeline."""

    def emit(message: str) -> None:
        print(message, flush=True)
        if progress_logger:
            progress_logger.append(message)

    emit("\n🚀 Lancement du pipeline...")
    try:
        historique = pd.read_csv(settings.HISTORY_PATH, dtype=str).fillna("")
    except FileNotFoundError:
        emit(
            "ℹ️ Aucun fichier d'historique trouvé à "
            f"{settings.HISTORY_PATH} → utilisation d'un historique vide"
        )
        historique = pd.DataFrame()
    processed_rows: list[pd.Series] = []
    for idx, row in df.iterrows():
        label = row.get("Libelle", "")
        cip = row.get("CIP", "")
        emit(f"\n🔎 Produit #{idx + 1} – {label}")
        match = match_in_history(label, historique)
        if match is not None:
            emit("➡️ Match historique trouvé")
            processed_rows.append(match)
            continue
        if is_medicine_by_label(label):
            emit("➡️ Détection médicament via libellé")
            processed_rows.append(force_medicine_categories(row))
            continue
        if cip and is_medicine_by_api(cip):
            emit("➡️ Détection médicament via API BDPM REST")
            processed_rows.append(force_medicine_categories(row))
            continue
        emit("➡️ Produit parapharmaceutique → IA")
        ai_json = classify_with_ai(label)
        processed_rows.append(apply_ai_classification(row, ai_json))
    emit("\n✅ Pipeline terminé")
    if not processed_rows:
        return pd.DataFrame(columns=df.columns)
    return pd.DataFrame(processed_rows).fillna("")
