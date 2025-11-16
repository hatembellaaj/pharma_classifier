"""Static constants shared across the backend."""

EXPECTED_COLUMNS = [
    "CIP",
    "Libelle",
    "Marque",
    "Univers",
    "Famille",
    "Tablette",
    "Tablette_consolidee",
]

MEDICINE_HINTS = [
    "mg",
    "µg",
    "mcg",
    "ui",
    "comprime",
    "comprimé",
    "gelule",
    "gélule",
    "suspension",
    "solution",
    "sirop",
    "inject",
    "pommade",
]

FORCED_MEDICINE_CATEGORIES = {
    "Univers": "CONSEILS ET ORDONNANCES",
    "Famille": "CONSEILS ET ORDONNANCES",
    "Tablette": "CONSEILS ET ORDONNANCES",
    "Tablette_consolidee": "CONSEILS ET ORDONNANCES",
}

HISTORY_MATCH_THRESHOLD = 0.82
