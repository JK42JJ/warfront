"""warfront/core/snapshot.py — Diff-based map snapshots (replaces deepcopy).

Instead of deep-copying the entire 12×12 GameMap, we store only the cells
that differ from a *baseline* state captured at the start of an algorithm run.
This reduces memory from O(rows×cols) per step to O(changed_cells) per step.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from warfront.data.models import GameMap, Terrain, UnitType


@dataclass(frozen=True)
class CellState:
    """Immutable snapshot of a single cell's mutable fields."""
    terrain_name: str        # Terrain.name (string) — avoids Enum identity bug
    unit_name: Optional[str]  # UnitType.name or None
    visited: bool
    in_path: bool
    distance: float
    highlight: Optional[str]


# Type alias
DiffSnapshot = Dict[Tuple[int, int], CellState]


def cell_state(cell) -> CellState:
    """Extract an immutable CellState from a live Cell."""
    return CellState(
        terrain_name=cell.terrain.name,
        unit_name=cell.unit.name if cell.unit is not None else None,
        visited=cell.visited,
        in_path=cell.in_path,
        distance=cell.distance,
        highlight=cell.highlight,
    )


def snapshot(gmap) -> DiffSnapshot:
    """Capture the full map as a DiffSnapshot (all cells).

    For the first step (baseline), call this once and store the result.
    For subsequent steps, call diff_snapshot() to store only changes.
    """
    result: DiffSnapshot = {}
    for r in range(gmap.rows):
        for c in range(gmap.cols):
            result[(r, c)] = cell_state(gmap.grid[r][c])
    return result


def diff_snapshot(gmap, baseline: DiffSnapshot) -> DiffSnapshot:
    """Return only cells that differ from *baseline*."""
    delta: DiffSnapshot = {}
    for r in range(gmap.rows):
        for c in range(gmap.cols):
            state = cell_state(gmap.grid[r][c])
            if state != baseline.get((r, c)):
                delta[(r, c)] = state
    return delta


def apply_snapshot(gmap, base: DiffSnapshot, delta: DiffSnapshot) -> None:
    """Apply a diff snapshot on top of *base* to restore the map state.

    Used by the animator to reconstruct map state at any step without
    storing a full copy per step.
    """
    from warfront.data.models import Terrain, UnitType

    terrain_map = {t.name: t for t in Terrain}
    unit_map    = {u.name: u for u in UnitType}

    # First restore base state
    for (r, c), state in base.items():
        cell = gmap.grid[r][c]
        cell.terrain  = terrain_map[state.terrain_name]
        cell.unit     = unit_map[state.unit_name] if state.unit_name else None
        cell.visited  = state.visited
        cell.in_path  = state.in_path
        cell.distance = state.distance
        cell.highlight = state.highlight

    # Then apply delta on top
    for (r, c), state in delta.items():
        cell = gmap.grid[r][c]
        cell.terrain  = terrain_map[state.terrain_name]
        cell.unit     = unit_map[state.unit_name] if state.unit_name else None
        cell.visited  = state.visited
        cell.in_path  = state.in_path
        cell.distance = state.distance
        cell.highlight = state.highlight
