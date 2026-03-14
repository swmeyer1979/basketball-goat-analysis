"""Basketball GOAT Analysis — data package.

Exports:
    PLAYERS      — dict of 10 player dicts, keyed by full name
    PLAYER_NAMES — ordered list of player name strings
    LEAGUE_HISTORY — dict mapping era year to league context tuple
    get_player   — lookup function by name
    get_league_tpd — talent pool depth multiplier for a given era year
"""

from .player_careers import (
    PLAYERS,
    PLAYER_NAMES,
    LEAGUE_HISTORY,
    get_player,
    get_league_tpd,
)
from .rankings import get_rankings

__all__ = [
    "PLAYERS",
    "PLAYER_NAMES",
    "LEAGUE_HISTORY",
    "get_player",
    "get_league_tpd",
    "get_rankings",
]
