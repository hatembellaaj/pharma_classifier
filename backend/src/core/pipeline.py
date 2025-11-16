"""Pipeline principal de classification pharmaceutique."""
from __future__ import annotations

import pandas as pd

from core.api_medicaments import is_medicine_by_api
from core.ai_classifier import classify_with_ai
from core.category_assigner import apply_ai_classification, force_medicine_categories
from core.historical_matcher import match_in_history
from core.medicine_detector import is_medicine_by_label


def run_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """Exécute les 4 étapes clés du pipeline."""
    print("\n🚀 Lancement du pipeline...")
    try:
        historique = pd.read_csv(
            "data/input/historiques/historique_global.csv", dtype=str
        ).fillna("")
    except FileNotFoundError:
        historique = pd.DataFrame()
    processed_rows: list[pd.Series] = []
    for idx, row in df.iterrows():
        label = row.get("Libelle", "")
        cip = row.get("CIP", "")
        print(f"\n🔎 Produit #{idx + 1} – {label}")
        match = match_in_history(label, historique)
        if match is not None:
            print("➡️ Match historique trouvé")
            processed_rows.append(match)
            continue
        if is_medicine_by_label(label):
            print("➡️ Détection médicament via libellé")
            processed_rows.append(force_medicine_categories(row))
            continue
        if cip and is_medicine_by_api(cip):
            print("➡️ Détection médicament via API BDPM REST")
            processed_rows.append(force_medicine_categories(row))
            continue
        print("➡️ Produit parapharmaceutique → IA")
        ai_json = classify_with_ai(label)
        processed_rows.append(apply_ai_classification(row, ai_json))
    print("\n✅ Pipeline terminé")
    if not processed_rows:
        return pd.DataFrame(columns=df.columns)
    return pd.DataFrame(processed_rows).fillna("")
