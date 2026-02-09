"""DreamBot agent loop."""

from __future__ import annotations

import time
from dataclasses import dataclass

from dreambot.adapter import BotAdapter
from dreambot.memory import MemoryEntry, MemoryStore
from dreambot.strategy import StrategyBrain


@dataclass
class DreamBot:
    adapter: BotAdapter
    memory: MemoryStore
    brain: StrategyBrain
    tick_rate: float = 1.5

    def run(self, cycles: int | None = None) -> None:
        self.adapter.connect()
        completed = 0
        try:
            while True:
                observation = self.adapter.observe()
                decision = self.brain.decide(observation)
                self.adapter.act(decision.action)
                self.memory.add(
                    MemoryEntry(
                        category="decision",
                        content=f"{decision.action.name}: {decision.reason}",
                    )
                )
                completed += 1
                if cycles is not None and completed >= cycles:
                    break
                time.sleep(self.tick_rate)
        finally:
            self.adapter.disconnect()
