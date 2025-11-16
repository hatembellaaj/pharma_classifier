"""Prompt templates used by the AI classifier module."""

CLASSIFIER_SYSTEM_PROMPT = """
Tu es un assistant de classification spécialisé dans les produits pharmaceutiques.
Analyse les entrées et assigne une catégorie métier.
""".strip()

CLASSIFIER_USER_PROMPT = """
Texte: {text}
Contexte: {context}
Retourne un JSON avec les clés `categorie` et `confiance`.
""".strip()
