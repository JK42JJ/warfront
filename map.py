from enum import Enum
from typing import List, Tuple, Optional

class Terrain(Enum):
    # (Character, Move Cost, Color, Description)
    PLAIN   = (".", 1,  "green",    "Plain")
    FOREST  = ("F", 2,  "dark_green","Forest")
    MOUNTAIN= ("M", 5,  "yellow",   "Calculation")
    RIVER   = ("~", 4,  "blue",     "River")
    WALL    = ("#", 999,"white",    "Wall")
    BASE    = ("B", 1,  "cyan",     "Base")

class UnitType(Enum):
    # (Character, Color, Description)
    ALLY    = ("🔵", "blue",   "Ally")
    ENEMY   = ("🔴", "red",    "Enemy")
    TARGET  = ("⭐", "yellow", "Target")
    DRONE   = ("🚁", "cyan",   "Drone")

class Cell:
    def __init__(self, terrain: Terrain = Terrain.PLAIN):
        self.terrain = terrain
        self.unit: Optional[UnitType] = None
        self.visited = False
        self.in_path = False
        self.distance: Optional[float] = float('inf')
        self.highlight: Optional[str] = None # Color name for highlighting

class GameMap:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]

    def place_unit(self, r: int, c: int, unit: UnitType):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.grid[r][c].unit = unit

    def set_terrain(self, r: int, c: int, terrain: Terrain):
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
        """Returns the movement cost of the terrain at (r, c)"""
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c].terrain.value[1]
        return 999

    def reset_simulation_state(self):
        """Reset visited/path/highlight states while keeping terrain and units"""
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c].visited = False
                self.grid[r][c].in_path = False
                self.grid[r][c].distance = float('inf')
                self.grid[r][c].highlight = None
