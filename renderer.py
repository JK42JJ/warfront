import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich import box
from map import GameMap, Terrain, UnitType, Cell
from typing import Optional
from config import cfg

console = Console()

TERRAIN_STYLE = {
    Terrain.PLAIN:    ("·", "dim white"),
    Terrain.FOREST:   ("F", "green"),
    Terrain.MOUNTAIN: ("M", "yellow"),
    Terrain.RIVER:    ("~", "blue"),
    Terrain.WALL:     ("█", "bright_white"),
    Terrain.BASE:     ("B", "cyan"),
}
UNIT_CHAR = {
    UnitType.ALLY:   ("@", "bold bright_blue"),
    UnitType.ENEMY:  ("X", "bold bright_red"),
    UnitType.TARGET: ("★", "bold bright_yellow"),
    UnitType.DRONE:  ("^", "bold bright_cyan"),
}


def _render_cell(cell: Cell) -> Text:
    t = Text()
    
    # Lookup based on name instead of Enum object to prevent type mismatch on reload
    unit_info = None
    if cell.unit:
        for u_type, info in UNIT_CHAR.items():
            if cell.unit == u_type or cell.unit.name == u_type.name:
                unit_info = info
                break
    
    if unit_info:
        ch, style = unit_info
        t.append(ch, style="bold bright_green" if cell.in_path else style)
        return t
    
    # Terrain info lookup
    terrain_info = TERRAIN_STYLE.get(Terrain.PLAIN)
    current_terrain = Terrain.PLAIN
    for t_type, info in TERRAIN_STYLE.items():
        if cell.terrain == t_type or cell.terrain.name == t_type.name:
            terrain_info = info
            current_terrain = t_type
            break
            
    ch, style = terrain_info
    
    if cell.in_path:       t.append("*", style="bold bright_green")
    elif cell.highlight:   t.append(ch, style=f"bold {cell.highlight}")
    elif cell.visited:     
        # Core terrain like Wall, River, Base not overwritten by numbers
        if current_terrain.name in ["WALL", "RIVER", "BASE"]:
            t.append(ch, style=style)
        elif cell.distance is not None and cell.distance != float('inf'):
            dist_str = str(int(cell.distance))[-1]
            # Use terrain background color for numbers to maintain feel
            bg_color = terrain_info[1].split()[-1]
            t.append(dist_str, style=f"bold white on {bg_color}")
        else:
            t.append("░", style="dim cyan")
    else:
        t.append(ch, style=style)
    return t


def build_map_renderable(gmap: GameMap, title: str = "Tactical Map") -> Panel:
    """Map with horizontal column numbers and vertical row number scales"""
    lines = []

    # Column header (highlighted every 5)
    hdr = Text()
    hdr.append("    ")
    for c in range(gmap.cols):
        if c % 5 == 0: hdr.append(f"{c:<2}", style="bold yellow")
        else: hdr.append("  ", style="")
    lines.append(hdr)

    # Separator
    sep = Text()
    sep.append("    ")
    for c in range(gmap.cols):
        sep.append("┬─" if c % 5 == 0 else "──", style="dim bright_black")
    lines.append(sep)

    # Rows
    for r in range(gmap.rows):
        row = Text()
        if r % 5 == 0: row.append(f"{r:2d}┤ ", style="bold yellow")
        else: row.append(f"{r:2d}│ ", style="dim bright_black")

        for c in range(gmap.cols):
            row.append_text(_render_cell(gmap.grid[r][c]))
            row.append(" ")
        lines.append(row)

    body = Text("\n").join(lines)
    return Panel(body, title=f"[bold yellow]⚔  {title}[/]", border_style="bright_black", padding=(0, 1))


def build_data_panel(data: dict, title: str = "Data Analysis") -> Panel:
    """Visualize data dict (bar graphs, etc.)"""
    from rich.table import Table
    t = Table.grid(expand=True)
    t.add_column(style="cyan", width=15)
    t.add_column(style="white")

    if not isinstance(data, dict):
        return Panel(Text(f"Invalid format: {type(data).__name__}", style="yellow"), 
                     title=f"[bold yellow]📊 {title}[/]", border_style="bright_black")

    for k, v in data.items():
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            val = min(float(v), 100.0)
            bar = f"[bright_green]{'█' * int(val/5)}[/][dim]{'░' * (20 - int(val/5))}[/] {v}"
            t.add_row(f" {k}", bar)
        elif isinstance(v, list):
            content_str = str(v)
            if len(content_str) > 100: content_str = content_str[:97] + "..."
            t.add_row(f" {k}", f"[yellow][{len(v)} items][/]\n {content_str}")
        else:
            t.add_row(f" {k}", f" {v}")

    return Panel(t, title=f"[bold yellow]📊 {title}[/]", border_style="bright_black", padding=(1, 2))


def build_legend() -> Panel:
    items = [("@","bold bright_blue"," Ally"),("X","bold bright_red"," Enemy"),
             ("★","bold bright_yellow"," Target"),("*","bold bright_green"," Path"),
             ("░","dim cyan"," Visited"),("█","bright_white"," Wall"),
             ("F","green"," Forest"),("M","yellow"," Mountain"),("~","blue"," River")]
    t = Text()
    for ch, style, label in items:
        t.append(f" {ch}", style=style)
        t.append(label, style="dim")
        t.append("  ")
    return Panel(t, title="[dim]Legend  ┤=Row, ┬=Col[/]", border_style="bright_black", padding=(0, 1))


class Renderer:
    def __init__(self, gmap, mission_name, algo_name, speed=0.4):
        self.gmap = gmap
        self.mission_name = mission_name
        self.algo_name = algo_name
        self.speed = speed

    def render_step(self, step_idx, total_steps, description, extra=""):
        """Main method for visualizing algorithm steps"""
        from rich.console import Group
        map_panel = build_map_renderable(self.gmap, title=self.mission_name)
        content = [map_panel]
        if cfg.ui["show_legend"]: content.append(build_legend())
        return Group(*content)
