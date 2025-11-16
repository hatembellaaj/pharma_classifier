"""Point d'entrée CLI pour lancer le pipeline complet."""
from __future__ import annotations

import pandas as pd

from core.pipeline import run_pipeline
from export.exporter import export_results
from export.update_history import update_history
from ingestion.loader import load_inputs
from ingestion.merger import merge_inputs
from ingestion.normalizer import normalize_text
from ingestion.validator import validate_schema
from utils.logger import log

INPUT_DIR = "data/input/base_initiale"
OUTPUT_PATH = "data/output/v2/pharmacie_classifiee_v2.csv"


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    for column in df.columns:
        if column.lower() == "cip":
            continue
        df[column] = df[column].astype(str).apply(normalize_text)
    return df


def main() -> None:
    log("🚀 Lancement du pipeline Pharma Classifier...")
    datasets = load_inputs(INPUT_DIR)
    if not datasets:
        log("⛔ Aucun fichier dans data/input/base_initiale/.")
        return
    validated = [validate_schema(df) for df in datasets]
    merged = merge_inputs(validated)
    log("🧽 Normalisation du texte...")
    merged = normalize_dataframe(merged)
    log("⚙️ Exécution du pipeline principal...")
    df_v2 = run_pipeline(merged)
    log("📦 Export du résultat V2...")
    export_results(df_v2, OUTPUT_PATH)
    log("📚 Mise à jour de l'historique global...")
    update_history(df_v2)
    log("🎉 Pipeline terminé avec succès !")
    log(f"📦 Résultat disponible dans : {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
