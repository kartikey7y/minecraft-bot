"""Core data models for DreamBot."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


class TimeOfDay(str, Enum):
    DAWN = "dawn"
    DAY = "day"
    DUSK = "dusk"
    NIGHT = "night"


@dataclass(frozen=True)
class Observation:
    position: str
    health: int
    hunger: int
    time_of_day: TimeOfDay
    inventory: Dict[str, int] = field(default_factory=dict)
    nearby_entities: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class Action:
    name: str
    details: Dict[str, str] = field(default_factory=dict)
