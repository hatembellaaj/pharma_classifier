"""Append-only history helper."""
from __future__ import annotations

import csv
from pathlib import Path


class HistoryUpdater:
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, item_id: str, label: str) -> None:
        with self.path.open("a", newline="", encoding="utf-8") as fp:
            writer = csv.writer(fp)
            writer.writerow([item_id, label])
