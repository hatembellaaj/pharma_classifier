"""Client for fr.gouv medicaments REST API (mock implementation)."""
from __future__ import annotations

from typing import Any

import httpx

BASE_URL = "https://fr.gouv.medicaments.rest/api"


class MedicamentAPI:
    def __init__(self, *, client: httpx.AsyncClient | None = None) -> None:
        self._client = client or httpx.AsyncClient(base_url=BASE_URL, timeout=10.0)

    async def close(self) -> None:
        await self._client.aclose()

    async def search(self, query: str) -> list[dict[str, Any]]:
        response = await self._client.get("/search", params={"q": query})
        response.raise_for_status()
        return response.json()
