"""Core strategy loop for DreamBot."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from dreambot.types import Action, Observation, TimeOfDay


@dataclass
class StrategyDecision:
    action: Action
    reason: str


class StrategyBrain:
    def decide(self, observation: Observation) -> StrategyDecision:
        if observation.health <= 6:
            return StrategyDecision(
                action=Action(name="seek_cover"),
                reason="Health is low; prioritize survival.",
            )
        if observation.hunger <= 6:
            return StrategyDecision(
                action=Action(name="eat_food"),
                reason="Hunger is low; refuel before continuing.",
            )
        if observation.time_of_day in {TimeOfDay.DUSK, TimeOfDay.NIGHT}:
            return StrategyDecision(
                action=Action(name="find_shelter"),
                reason="Night time detected; avoid hostile mobs.",
            )
        if self._hostiles_nearby(observation.nearby_entities):
            return StrategyDecision(
                action=Action(name="defend"),
                reason="Hostile entities nearby; prepare to fight or flee.",
            )
        return StrategyDecision(
            action=Action(name="gather_resources"),
            reason="Stable conditions; collect resources.",
        )

    @staticmethod
    def _hostiles_nearby(entities: List[str]) -> bool:
        hostiles = {"zombie", "skeleton", "creeper", "spider", "enderman"}
        return any(entity in hostiles for entity in entities)
