"""
OSRS-inspired XP table for 100 levels.
Formula: xp_for_level(n) = floor(sum(floor(i + 300 * 2^(i/7))) / 4) for i from 1 to n-1

Level 1: 0 XP
Level 50: ~101,333 XP  
Level 100: ~13,034,431 XP

This creates fast early progression that becomes exponentially slower.
"""

import math
from functools import lru_cache


def _calculate_xp_table() -> list[int]:
    """Generate XP requirements for levels 1-100."""
    table = [0]  # Level 1 = 0 XP
    total = 0
    
    for level in range(1, 100):
        # OSRS formula
        total += math.floor(level + 300 * (2 ** (level / 7)))
        xp_needed = math.floor(total / 4)
        table.append(xp_needed)
    
    return table


# Pre-calculated XP table for levels 1-100
XP_TABLE: list[int] = _calculate_xp_table()


@lru_cache(maxsize=128)
def get_level_for_xp(xp: int) -> int:
    """Get the level for a given amount of XP."""
    for level in range(99, 0, -1):
        if xp >= XP_TABLE[level]:
            return level + 1
    return 1


def get_xp_for_level(level: int) -> int:
    """Get the XP required to reach a specific level."""
    if level < 1:
        return 0
    if level > 100:
        return XP_TABLE[99]
    return XP_TABLE[level - 1]


def get_xp_to_next_level(current_xp: int, current_level: int) -> tuple[int, int]:
    """
    Get XP progress to next level.
    Returns (current_xp_in_level, xp_needed_for_next_level)
    """
    if current_level >= 100:
        return (0, 0)
    
    xp_for_current = XP_TABLE[current_level - 1]
    xp_for_next = XP_TABLE[current_level]
    
    xp_in_level = current_xp - xp_for_current
    xp_needed = xp_for_next - xp_for_current
    
    return (xp_in_level, xp_needed)


# Print some sample values for verification
if __name__ == "__main__":
    print("XP Table Sample:")
    for lvl in [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        print(f"Level {lvl}: {XP_TABLE[lvl-1]:,} XP")
