"""Adapter interfaces for Mineflayer-compatible environments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from dreambot.types import Action, Observation, TimeOfDay


class BotAdapter(Protocol):
    def connect(self) -> None:
        ...

    def disconnect(self) -> None:
        ...

    def observe(self) -> Observation:
        ...

    def act(self, action: Action) -> None:
        ...


@dataclass
class NullAdapter:
    """Offline adapter for dry runs and strategy validation."""

    tick: int = 0

    def connect(self) -> None:
        return None

    def disconnect(self) -> None:
        return None

    def observe(self) -> Observation:
        self.tick += 1
        time_of_day = TimeOfDay.DAY if self.tick % 3 else TimeOfDay.NIGHT
        return Observation(
            position="0,64,0",
            health=20,
            hunger=20,
            time_of_day=time_of_day,
            inventory={"oak_log": 12},
            nearby_entities=["cow"],
        )

    def act(self, action: Action) -> None:
        return None


@dataclass
class MineflayerUnavailableError(RuntimeError):
    """Raised when Mineflayer bindings are not available."""


class MineflayerAdapter:
    """Thin Python wrapper for Mineflayer-compatible runtimes."""

    host: str
    port: int
    username: str
    _client: Optional[object] = None

    @staticmethod
    def is_available() -> bool:
        try:
            import mineflayer  # type: ignore  # noqa: F401
        except ImportError:
            return False
        return True

    def connect(self) -> None:
        if not self.is_available():
            raise MineflayerUnavailableError(
                "Mineflayer bindings are not available. "
                "Install a compatible Python package or use --dry-run."
            )
        from mineflayer import create_bot  # type: ignore

        self._client = create_bot(
            {
                "host": self.host,
                "port": self.port,
                "username": self.username,
            }
        )

    def disconnect(self) -> None:
        if self._client and hasattr(self._client, "quit"):
            self._client.quit()

    def observe(self) -> Observation:
        if not self._client:
            raise RuntimeError("Mineflayer client not connected.")
        health = getattr(self._client, "health", 20)
        hunger = getattr(self._client, "food", 20)
        position = str(getattr(self._client, "entity", {}).get("position", "0,64,0"))
        time_of_day = TimeOfDay.DAY
        return Observation(
            position=position,
            health=int(health),
            hunger=int(hunger),
            time_of_day=time_of_day,
            inventory={},
            nearby_entities=[],
        )

    def act(self, action: Action) -> None:
        if not self._client:
            raise RuntimeError("Mineflayer client not connected.")
        if action.name == "gather_resources":
            return None
        if action.name == "find_shelter":
            return None
        if action.name == "defend":
            return None
        if action.name == "eat_food":
            return None
        if action.name == "seek_cover":
            return None
