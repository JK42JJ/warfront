"""warfront/data/models.py — Data structures (port of map.py with __slots__ on Cell)"""
from __future__ import annotations
from enum import Enum
from typing import List, Tuple, Optional


class Terrain(Enum):
    # (Character, Move Cost, Color, Description)
    PLAIN    = (".", 1,   "green",      "Plain")
    FOREST   = ("F", 2,   "dark_green", "Forest")
    MOUNTAIN = ("M", 5,   "yellow",     "Calculation")
    RIVER    = ("~", 4,   "blue",       "River")
    WALL     = ("#", 999, "white",      "Wall")
    BASE     = ("B", 1,   "cyan",       "Base")


class UnitType(Enum):
    # (Character, Color, Description)
    ALLY   = ("🔵", "blue",   "Ally")
    ENEMY  = ("🔴", "red",    "Enemy")
    TARGET = ("⭐", "yellow", "Target")
    DRONE  = ("🚁", "cyan",   "Drone")


class Cell:
    """Single map cell.  __slots__ cuts per-instance memory ~40%."""
    __slots__ = ("terrain", "unit", "visited", "in_path", "distance", "highlight")

    def __init__(self, terrain: Terrain = Terrain.PLAIN) -> None:
        self.terrain: Terrain = terrain
        self.unit: Optional[UnitType] = None
        self.visited: bool = False
        self.in_path: bool = False
        self.distance: float = float("inf")
        self.highlight: Optional[str] = None


class GameMap:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.grid: List[List[Cell]] = [
            [Cell() for _ in range(cols)] for _ in range(rows)
        ]

    def place_unit(self, r: int, c: int, unit: UnitType) -> None:
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.grid[r][c].unit = unit

    def set_terrain(self, r: int, c: int, terrain: Terrain) -> None:
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.grid[r][c].terrain = terrain

    def get_neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbors.append((nr, nc))
        return neighbors

    def get_cost(self, r: int, c: int) -> int:
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c].terrain.value[1]
        return 999

    def reset_simulation_state(self) -> None:
        """Reset visited/path/highlight states while keeping terrain and units."""
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                cell.visited = False
                cell.in_path = False
                cell.distance = float("inf")
                cell.highlight = None
