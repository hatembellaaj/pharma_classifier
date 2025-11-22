"""Pipeline principal de classification pharmaceutique."""
from __future__ import annotations

import pandas as pd

from typing import Optional

from core.api_medicaments import (
    extract_tva_from_payload,
    is_medicine_payload,
    search_by_cip,
    summarize_payload,
)
from core.ai_classifier import classify_with_ai
from core.category_assigner import apply_ai_classification, force_medicine_categories
from core.historical_matcher import match_in_history
from core.medicine_detector import is_medicine_by_label
from config import settings
from utils.progress_log import ProgressLog
from utils.history import extract_history_clusters, normalize_history_dataframe
from utils.dataframe import coalesce_duplicate_columns


def run_pipeline(df: pd.DataFrame, progress_logger: Optional[ProgressLog] = None) -> pd.DataFrame:
    """Exécute les 4 étapes clés du pipeline."""

    def emit(message: str) -> None:
        print(message, flush=True)
        if progress_logger:
            progress_logger.append(message)

    emit("\n🚀 Lancement du pipeline...")
    try:
        historique = pd.read_csv(settings.HISTORY_PATH, dtype=str).fillna("")
        historique = coalesce_duplicate_columns(historique)
        historique = normalize_history_dataframe(historique)
    except FileNotFoundError:
        emit(
            "ℹ️ Aucun fichier d'historique trouvé à "
            f"{settings.HISTORY_PATH} → utilisation d'un historique vide"
        )
        historique = pd.DataFrame()

    try:
        reference_df = pd.read_csv(settings.REFERENCE_CATALOG_PATH, dtype=str).fillna("")
        reference_df = coalesce_duplicate_columns(reference_df)
        reference_df = normalize_history_dataframe(reference_df)
        reference_catalog = extract_history_clusters(reference_df)
        emit(
            "\n📚 Référentiel chargé depuis "
            f"{settings.REFERENCE_CATALOG_PATH} ({len(reference_df)} lignes)"
        )
    except FileNotFoundError:
        emit(
            "ℹ️ Aucun référentiel trouvé à "
            f"{settings.REFERENCE_CATALOG_PATH} → utilisation de l'historique"
        )
        reference_catalog = extract_history_clusters(historique)

    cluster_catalog = extract_history_clusters(historique)
    emit("\n📚 Clusters extraits depuis l'historique :")
    for column, values in cluster_catalog.items():
        if values:
            emit(f"   • {column} ({len(values)}) : {', '.join(values)}")
        else:
            emit(f"   • {column} : aucun cluster trouvé")
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
        api_payload = search_by_cip(cip, label=label) if cip or label else None
        if api_payload is not None:
            emit(f"   ↪ Réponse API officielle : {summarize_payload(api_payload)}")
            if is_medicine_payload(api_payload):
                emit("➡️ Détection médicament via API BDPM REST")
                medicine_row = force_medicine_categories(row)
                tva_value = extract_tva_from_payload(api_payload, cip)
                if tva_value:
                    medicine_row["TVA"] = tva_value
                    emit(f"   ↪ TVA calculée via l'API : {tva_value}")
                processed_rows.append(medicine_row)
                continue
        elif cip:
            emit("   ↪ API BDPM REST interrogée : aucune réponse exploitable")
        emit("➡️ Produit parapharmaceutique → IA")
        labo = row.get("LABO", "")
        ai_json = classify_with_ai(
            label,
            labo=labo,
            cluster_catalog=cluster_catalog,
            reference_catalog=reference_catalog,
        )
        processed_rows.append(apply_ai_classification(row, ai_json))
    emit("\n✅ Pipeline terminé")
    if not processed_rows:
        return pd.DataFrame(columns=df.columns)
    result = pd.DataFrame(processed_rows).fillna("")
    return coalesce_duplicate_columns(result)
