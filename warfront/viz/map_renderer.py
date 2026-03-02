"""warfront/viz/map_renderer.py — Rich-based map rendering (port of renderer.py).

Provides rendering functions for both live GameMap objects and DiffSnapshot dicts.
All Enum comparisons use string name comparison to prevent identity bugs on module reload.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional, Tuple

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from warfront.config import cfg

if TYPE_CHECKING:
    from warfront.data.models import GameMap, Cell
    from warfront.core.snapshot import DiffSnapshot, CellState

console = Console()

# ---------------------------------------------------------------------------
# Style tables — keyed by string name to avoid Enum identity bugs
# ---------------------------------------------------------------------------

# terrain_name -> (char, style)
TERRAIN_STYLE: Dict[str, Tuple[str, str]] = {
    "PLAIN":    ("·", "dim white"),
    "FOREST":   ("F", "green"),
    "MOUNTAIN": ("M", "yellow"),
    "RIVER":    ("~", "blue"),
    "WALL":     ("█", "bright_white"),
    "BASE":     ("B", "cyan"),
}

# unit_name -> (char, style)
UNIT_CHAR: Dict[str, Tuple[str, str]] = {
    "ALLY":   ("@", "bold bright_blue"),
    "ENEMY":  ("X", "bold bright_red"),
    "TARGET": ("★", "bold bright_yellow"),
    "DRONE":  ("^", "bold bright_cyan"),
}


# ---------------------------------------------------------------------------
# Internal cell rendering helpers
# ---------------------------------------------------------------------------

def _render_cell_from_live(cell: "Cell") -> Text:
    """Render a live Cell object into a Rich Text segment."""
    t = Text()

    # Unit check using string name comparison
    unit_info: Optional[Tuple[str, str]] = None
    if cell.unit is not None:
        unit_info = UNIT_CHAR.get(cell.unit.name)

    if unit_info is not None:
        ch, style = unit_info
        t.append(ch, style="bold bright_green" if cell.in_path else style)
        return t

    # Terrain check using string name comparison
    terrain_name = cell.terrain.name
    terrain_info = TERRAIN_STYLE.get(terrain_name, ("·", "dim white"))
    ch, style = terrain_info

    if cell.in_path:
        t.append("*", style="bold bright_green")
    elif cell.highlight:
        t.append(ch, style=f"bold {cell.highlight}")
    elif cell.visited:
        # Core terrains keep their own character/style even when visited
        if terrain_name in ("WALL", "RIVER", "BASE"):
            t.append(ch, style=style)
        elif cell.distance is not None and cell.distance != float("inf"):
            dist_str = str(int(cell.distance))[-1]
            bg_color = style.split()[-1]
            t.append(dist_str, style=f"bold white on {bg_color}")
        else:
            t.append("░", style="dim cyan")
    else:
        t.append(ch, style=style)

    return t


def _render_cell_from_state(state: "CellState") -> Text:
    """Render a CellState (from DiffSnapshot) into a Rich Text segment."""
    t = Text()

    # Unit check
    unit_info: Optional[Tuple[str, str]] = None
    if state.unit_name is not None:
        unit_info = UNIT_CHAR.get(state.unit_name)

    if unit_info is not None:
        ch, style = unit_info
        t.append(ch, style="bold bright_green" if state.in_path else style)
        return t

    # Terrain check
    terrain_name = state.terrain_name
    terrain_info = TERRAIN_STYLE.get(terrain_name, ("·", "dim white"))
    ch, style = terrain_info

    if state.in_path:
        t.append("*", style="bold bright_green")
    elif state.highlight:
        t.append(ch, style=f"bold {state.highlight}")
    elif state.visited:
        if terrain_name in ("WALL", "RIVER", "BASE"):
            t.append(ch, style=style)
        elif state.distance is not None and state.distance != float("inf"):
            dist_str = str(int(state.distance))[-1]
            bg_color = style.split()[-1]
            t.append(dist_str, style=f"bold white on {bg_color}")
        else:
            t.append("░", style="dim cyan")
    else:
        t.append(ch, style=style)

    return t


def _build_column_header(cols: int) -> Text:
    """Build the column-number header row."""
    hdr = Text()
    hdr.append("    ")
    for c in range(cols):
        if c % 5 == 0:
            hdr.append(f"{c:<2}", style="bold yellow")
        else:
            hdr.append("  ", style="")
    return hdr


def _build_separator(cols: int) -> Text:
    """Build the separator row below the column header."""
    sep = Text()
    sep.append("    ")
    for c in range(cols):
        sep.append("┬─" if c % 5 == 0 else "──", style="dim bright_black")
    return sep


# ---------------------------------------------------------------------------
# Public rendering functions
# ---------------------------------------------------------------------------

def build_map_renderable(gmap: "GameMap", title: str = "Tactical Map") -> Panel:
    """Render a live GameMap into a Rich Panel.

    Takes a live GameMap object (same signature as the original renderer.py).
    """
    lines = []
    lines.append(_build_column_header(gmap.cols))
    lines.append(_build_separator(gmap.cols))

    for r in range(gmap.rows):
        row = Text()
        if r % 5 == 0:
            row.append(f"{r:2d}┤ ", style="bold yellow")
        else:
            row.append(f"{r:2d}│ ", style="dim bright_black")

        for c in range(gmap.cols):
            row.append_text(_render_cell_from_live(gmap.grid[r][c]))
            row.append(" ")
        lines.append(row)

    body = Text("\n").join(lines)
    return Panel(
        body,
        title=f"[bold yellow]⚔  {title}[/]",
        border_style="bright_black",
        padding=(0, 1),
    )


def build_snapshot_renderable(
    snap: "DiffSnapshot",
    rows: int,
    cols: int,
    title: str = "Tactical Map",
) -> Panel:
    """Render a DiffSnapshot dict into a Rich Panel.

    Args:
        snap:  DiffSnapshot (Dict[Tuple[int,int], CellState]) — must be a *full*
               snapshot (all cells present), not a sparse diff.
        rows:  Number of map rows.
        cols:  Number of map columns.
        title: Panel title.
    """
    lines = []
    lines.append(_build_column_header(cols))
    lines.append(_build_separator(cols))

    for r in range(rows):
        row = Text()
        if r % 5 == 0:
            row.append(f"{r:2d}┤ ", style="bold yellow")
        else:
            row.append(f"{r:2d}│ ", style="dim bright_black")

        for c in range(cols):
            state = snap.get((r, c))
            if state is not None:
                row.append_text(_render_cell_from_state(state))
            else:
                # Fallback for sparse snapshots: render plain terrain
                row.append_text(Text("·", style="dim white"))
            row.append(" ")
        lines.append(row)

    body = Text("\n").join(lines)
    return Panel(
        body,
        title=f"[bold yellow]⚔  {title}[/]",
        border_style="bright_black",
        padding=(0, 1),
    )


def build_data_panel(data: dict, title: str = "Data Analysis") -> Panel:
    """Visualize a data dict with bar graphs for numeric values."""
    from rich.table import Table

    t = Table.grid(expand=True)
    t.add_column(style="cyan", width=15)
    t.add_column(style="white")

    if not isinstance(data, dict):
        return Panel(
            Text(f"Invalid format: {type(data).__name__}", style="yellow"),
            title=f"[bold yellow]📊 {title}[/]",
            border_style="bright_black",
        )

    for k, v in data.items():
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            val = min(float(v), 100.0)
            bar = (
                f"[bright_green]{'█' * int(val / 5)}[/]"
                f"[dim]{'░' * (20 - int(val / 5))}[/] {v}"
            )
            t.add_row(f" {k}", bar)
        elif isinstance(v, list):
            content_str = str(v)
            if len(content_str) > 100:
                content_str = content_str[:97] + "..."
            t.add_row(f" {k}", f"[yellow][{len(v)} items][/]\n {content_str}")
        else:
            t.add_row(f" {k}", f" {v}")

    return Panel(
        t,
        title=f"[bold yellow]📊 {title}[/]",
        border_style="bright_black",
        padding=(1, 2),
    )


def build_legend() -> Panel:
    """Build the map legend panel."""
    items = [
        ("@", "bold bright_blue",   " Ally"),
        ("X", "bold bright_red",    " Enemy"),
        ("★", "bold bright_yellow", " Target"),
        ("*", "bold bright_green",  " Path"),
        ("░", "dim cyan",           " Visited"),
        ("█", "bright_white",       " Wall"),
        ("F", "green",              " Forest"),
        ("M", "yellow",             " Mountain"),
        ("~", "blue",               " River"),
    ]
    t = Text()
    for ch, style, label in items:
        t.append(f" {ch}", style=style)
        t.append(label, style="dim")
        t.append("  ")
    return Panel(
        t,
        title="[dim]Legend  ┤=Row, ┬=Col[/]",
        border_style="bright_black",
        padding=(0, 1),
    )
