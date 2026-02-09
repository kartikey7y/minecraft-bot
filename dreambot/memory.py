"""Memory storage for DreamBot."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List


@dataclass
class MemoryEntry:
    category: str
    content: str


class MemoryStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def add(self, entry: MemoryEntry) -> None:
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry.__dict__) + "\n")

    def read_all(self) -> List[MemoryEntry]:
        if not self.path.exists():
            return []
        return [MemoryEntry(**item) for item in self._load_entries()]

    def _load_entries(self) -> Iterable[Dict[str, Any]]:
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    yield json.loads(line)
