"""OpenAI-powered classifier helper."""
from __future__ import annotations

import openai

from config.prompts import PROMPT_CLASSIFICATION
from config.settings import OPENAI_API_KEY

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY


def classify_with_ai(label: str) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY est requis pour la classification IA")
    messages = [
        {"role": "system", "content": PROMPT_CLASSIFICATION},
        {"role": "user", "content": f"Libellé : {label}"},
    ]
    try:
        response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
        return response.choices[0].message["content"]
    except AttributeError:
        response = openai.ChatCompletion.create(model="gpt-4o-mini", messages=messages)
        return response.choices[0].message["content"]
