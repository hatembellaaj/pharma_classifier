"""Thread-safe helper to persist pipeline progress logs."""
from __future__ import annotations

from pathlib import Path
from threading import Lock
from typing import Iterable, List


class ProgressLog:
    """Simple file-backed logger used to expose pipeline progress to the UI."""

    def __init__(self, path: Path):
        self.path = path
        self._lock = Lock()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.touch()

    def reset(self) -> None:
        with self._lock:
            self.path.write_text("", encoding="utf-8")

    def extend(self, lines: Iterable[str]) -> None:
        for line in lines:
            self.append(line)

    def append(self, line: str) -> None:
        with self._lock:
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(f"{line}\n")

    def read(self) -> List[str]:
        if not self.path.exists():
            return []
        with self._lock:
            content = self.path.read_text(encoding="utf-8")
        return [line for line in content.splitlines() if line.strip()]


__all__ = ["ProgressLog"]
