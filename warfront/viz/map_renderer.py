"""warfront/viz/map_renderer.py — Rich-based map rendering (port of renderer.py).

Provides rendering functions for both live GameMap objects and DiffSnapshot dicts.
All Enum comparisons use string name comparison to prevent identity bugs on module reload.

Aesthetic: phosphor-green terminal / roguelike / retro CRT
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
# Retro ASCII style tables — phosphor-green terminal / roguelike aesthetic
# ---------------------------------------------------------------------------

# terrain_name -> (char, style)
TERRAIN_STYLE: Dict[str, Tuple[str, str]] = {
    "PLAIN":    ("·", "dim green"),           # ground — dim phosphor dot
    "FOREST":   ("♣", "green"),               # treeline — classic card symbol
    "MOUNTAIN": ("▲", "yellow"),              # peak — ASCII mountain
    "RIVER":    ("≈", "bright_blue"),         # current — double-wave
    "WALL":     ("▓", "white"),               # blockade — shade block
    "BASE":     ("B", "bold bright_cyan"),    # forward operating base
}

# unit_name -> (char, style)
UNIT_CHAR: Dict[str, Tuple[str, str]] = {
    "ALLY":   ("@", "bold bright_green"),     # commander — roguelike tradition
    "ENEMY":  ("X", "bold bright_red"),       # hostile — eliminated marker
    "TARGET": ("◎", "bold bright_yellow"),    # objective — bullseye
    "DRONE":  ("◆", "bold bright_cyan"),      # aerial unit
}

# CRT scanline: rows at this interval get a darker tint
_SCANLINE_INTERVAL = 4


# ---------------------------------------------------------------------------
# Internal cell rendering helpers
# ---------------------------------------------------------------------------

def _render_cell_from_live(cell: "Cell", scanline: bool = False) -> Text:
    """Render a live Cell object into a Rich Text segment."""
    t = Text()

    # Unit check using string name comparison
    unit_info: Optional[Tuple[str, str]] = None
    if cell.unit is not None:
        unit_info = UNIT_CHAR.get(cell.unit.name)

    if unit_info is not None:
        ch, style = unit_info
        if scanline:
            t.append(ch, style="dim " + style)
        else:
            t.append(ch, style="bold bright_green" if cell.in_path else style)
        return t

    # Terrain check using string name comparison
    terrain_name = cell.terrain.name
    terrain_info = TERRAIN_STYLE.get(terrain_name, ("·", "dim green"))
    ch, style = terrain_info

    if cell.in_path:
        t.append("*", style="dim bold bright_green" if scanline else "bold bright_green")
    elif cell.highlight:
        t.append(ch, style=f"dim bold {cell.highlight}" if scanline else f"bold {cell.highlight}")
    elif cell.visited:
        # Core terrains keep their own character/style even when visited
        if terrain_name in ("WALL", "RIVER", "BASE"):
            t.append(ch, style=("dim " + style) if scanline else style)
        elif cell.distance is not None and cell.distance != float("inf"):
            dist_str = str(int(cell.distance))[-1]
            bg_color = style.split()[-1]
            base = f"bold white on {bg_color}"
            t.append(dist_str, style=("dim " + base) if scanline else base)
        else:
            t.append("▒", style="dim cyan" if not scanline else "dim green")
    else:
        t.append(ch, style=("dim " + style) if scanline else style)

    return t


def _render_cell_from_state(state: "CellState", scanline: bool = False) -> Text:
    """Render a CellState (from DiffSnapshot) into a Rich Text segment."""
    t = Text()

    # Unit check
    unit_info: Optional[Tuple[str, str]] = None
    if state.unit_name is not None:
        unit_info = UNIT_CHAR.get(state.unit_name)

    if unit_info is not None:
        ch, style = unit_info
        if scanline:
            t.append(ch, style="dim " + style)
        else:
            t.append(ch, style="bold bright_green" if state.in_path else style)
        return t

    # Terrain check
    terrain_name = state.terrain_name
    terrain_info = TERRAIN_STYLE.get(terrain_name, ("·", "dim green"))
    ch, style = terrain_info

    if state.in_path:
        t.append("*", style="dim bold bright_green" if scanline else "bold bright_green")
    elif state.highlight:
        t.append(ch, style=f"dim bold {state.highlight}" if scanline else f"bold {state.highlight}")
    elif state.visited:
        if terrain_name in ("WALL", "RIVER", "BASE"):
            t.append(ch, style=("dim " + style) if scanline else style)
        elif state.distance is not None and state.distance != float("inf"):
            dist_str = str(int(state.distance))[-1]
            bg_color = style.split()[-1]
            base = f"bold white on {bg_color}"
            t.append(dist_str, style=("dim " + base) if scanline else base)
        else:
            t.append("▒", style="dim cyan" if not scanline else "dim green")
    else:
        t.append(ch, style=("dim " + style) if scanline else style)

    return t


def _build_column_header(cols: int) -> Text:
    """Build the column-number header row."""
    hdr = Text()
    hdr.append("    ", style="")
    for c in range(cols):
        if c % 5 == 0:
            hdr.append(f"{c:<2}", style="bold bright_green")
        else:
            hdr.append("  ", style="")
    return hdr


def _build_separator(cols: int) -> Text:
    """Build the separator row below the column header."""
    sep = Text()
    sep.append("    ")
    for c in range(cols):
        sep.append("┬─" if c % 5 == 0 else "──", style="dim green")
    return sep


# ---------------------------------------------------------------------------
# Public rendering functions
# ---------------------------------------------------------------------------

def build_map_renderable(gmap: "GameMap", title: str = "Tactical Map") -> Panel:
    """Render a live GameMap into a Rich Panel (retro CRT aesthetic).

    Takes a live GameMap object (same signature as the original renderer.py).
    """
    lines = []
    lines.append(_build_column_header(gmap.cols))
    lines.append(_build_separator(gmap.cols))

    for r in range(gmap.rows):
        scanline = (r % _SCANLINE_INTERVAL == _SCANLINE_INTERVAL - 1)
        row = Text()
        if r % 5 == 0:
            row.append(f"{r:2d}┤ ", style="bold bright_green")
        else:
            row.append(f"{r:2d}│ ", style="dim green")

        for c in range(gmap.cols):
            row.append_text(_render_cell_from_live(gmap.grid[r][c], scanline=scanline))
            row.append(" ")
        lines.append(row)

    body = Text("\n").join(lines)
    return Panel(
        body,
        title=f"[bold green]◄◄  {title}  ►► [/]",
        border_style="green",
        padding=(0, 1),
    )


def build_snapshot_renderable(
    snap: "DiffSnapshot",
    rows: int,
    cols: int,
    title: str = "Tactical Map",
) -> Panel:
    """Render a DiffSnapshot dict into a Rich Panel (retro CRT aesthetic).

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
        scanline = (r % _SCANLINE_INTERVAL == _SCANLINE_INTERVAL - 1)
        row = Text()
        if r % 5 == 0:
            row.append(f"{r:2d}┤ ", style="bold bright_green")
        else:
            row.append(f"{r:2d}│ ", style="dim green")

        for c in range(cols):
            state = snap.get((r, c))
            if state is not None:
                row.append_text(_render_cell_from_state(state, scanline=scanline))
            else:
                # Fallback for sparse snapshots: render plain terrain
                row.append_text(Text("·", style="dim green"))
            row.append(" ")
        lines.append(row)

    body = Text("\n").join(lines)
    return Panel(
        body,
        title=f"[bold green]◄◄  {title}  ►► [/]",
        border_style="green",
        padding=(0, 1),
    )


def build_data_panel(data: dict, title: str = "Data Analysis") -> Panel:
    """Visualize a data dict with bar graphs for numeric values."""
    from rich.table import Table

    t = Table.grid(expand=True)
    t.add_column(style="bright_green", width=15)
    t.add_column(style="green")

    if not isinstance(data, dict):
        return Panel(
            Text(f"Invalid format: {type(data).__name__}", style="yellow"),
            title=f"[bold green]▸ {title}[/]",
            border_style="green",
        )

    for k, v in data.items():
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            val = min(float(v), 100.0)
            bar = (
                f"[bright_green]{'█' * int(val / 5)}[/]"
                f"[dim green]{'░' * (20 - int(val / 5))}[/] [green]{v}[/]"
            )
            t.add_row(f" {k}", bar)
        elif isinstance(v, list):
            content_str = str(v)
            if len(content_str) > 100:
                content_str = content_str[:97] + "..."
            t.add_row(f" {k}", f"[yellow][{len(v)} items][/]\n [dim]{content_str}[/]")
        else:
            t.add_row(f" {k}", f" [green]{v}[/]")

    return Panel(
        t,
        title=f"[bold green]▸ {title}[/]",
        border_style="green",
        padding=(1, 2),
    )


def build_legend() -> Panel:
    """Build the map legend panel (retro phosphor-green aesthetic)."""
    items = [
        ("@", "bold bright_green",  " Ally"),
        ("X", "bold bright_red",    " Enemy"),
        ("◎", "bold bright_yellow", " Target"),
        ("*", "bold bright_green",  " Path"),
        ("▒", "dim cyan",           " Visited"),
        ("▓", "white",              " Wall"),
        ("♣", "green",              " Forest"),
        ("▲", "yellow",             " Mountain"),
        ("≈", "bright_blue",        " River"),
        ("B", "bold bright_cyan",   " Base"),
    ]
    t = Text()
    for ch, style, label in items:
        t.append(f" {ch}", style=style)
        t.append(label, style="dim green")
        t.append("  ")
    return Panel(
        t,
        title="[dim green]Legend  ┤=Row  ┬=Col[/]",
        border_style="green",
        padding=(0, 1),
    )
