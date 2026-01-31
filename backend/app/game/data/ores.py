"""
Ore definitions for mining skill.

Each ore has:
- name: Display name
- level_required: Minimum mining level to mine
- xp: XP gained per ore mined
- mining_time: Base time to mine in seconds
- ascii: ASCII representation
- color: Hex color for UI
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Ore:
    id: str
    name: str
    level_required: int
    xp: int
    mining_time: float  # seconds
    ascii: str
    color: str
    description: str


ORES: Dict[str, Ore] = {
    "copper": Ore(
        id="copper",
        name="Copper Ore",
        level_required=1,
        xp=10,
        mining_time=2.0,
        ascii="[Cu]",
        color="#B87333",
        description="A common ore, perfect for beginners."
    ),
    "iron": Ore(
        id="iron",
        name="Iron Ore",
        level_required=15,
        xp=25,
        mining_time=3.5,
        ascii="[Fe]",
        color="#A19D94",
        description="A sturdy ore used in many tools."
    ),
    "silver": Ore(
        id="silver",
        name="Silver Ore",
        level_required=30,
        xp=45,
        mining_time=5.0,
        ascii="[Ag]",
        color="#C0C0C0",
        description="A precious metal with a brilliant shine."
    ),
    "gold": Ore(
        id="gold",
        name="Gold Ore",
        level_required=50,
        xp=75,
        mining_time=7.0,
        ascii="[Au]",
        color="#FFD700",
        description="The most sought-after precious metal."
    ),
    "mithril": Ore(
        id="mithril",
        name="Mithril Ore",
        level_required=70,
        xp=120,
        mining_time=10.0,
        ascii="[Mi]",
        color="#4169E1",
        description="A legendary ore of immense power."
    ),
}


def get_ore(ore_id: str) -> Ore | None:
    """Get ore by ID."""
    return ORES.get(ore_id)


def get_available_ores(level: int) -> list[Ore]:
    """Get all ores available at a given mining level."""
    return [ore for ore in ORES.values() if ore.level_required <= level]


def get_all_ores() -> list[Ore]:
    """Get all ores sorted by level requirement."""
    return sorted(ORES.values(), key=lambda x: x.level_required)
