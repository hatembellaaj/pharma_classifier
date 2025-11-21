"""OpenAI-powered classifier helper."""
from __future__ import annotations

import requests

from config.prompts import build_classification_prompt
from config.settings import OPENAI_API_KEY

OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"


def classify_with_ai(
    label: str, labo: str | None = None, cluster_catalog: dict[str, list[str]] | None = None
) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY est requis pour la classification IA")

    user_content = f"Libellé : {label}"
    if labo:
        user_content += f"\nLaboratoire : {labo}"

    system_prompt = build_classification_prompt(cluster_catalog)

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
    }

    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()

    data = response.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:  # pragma: no cover - defensive
        raise RuntimeError("Réponse inattendue de l'API OpenAI") from exc
