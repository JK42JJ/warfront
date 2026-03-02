"""warfront/viz/animator.py — Unified step animation loop for WARFRONT v2.

Uses Rich Live for smooth terminal rendering. Supports Space to pause/resume.
Key detection is done via select + tty (no readchar dependency).
"""
from __future__ import annotations

import select
import sys
import termios
import time
import tty
from typing import Any, List, Optional, Tuple

from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from warfront.config import cfg
from warfront.viz.map_renderer import build_legend, build_map_renderable

console = Console()


# ---------------------------------------------------------------------------
# Non-blocking single-character read helpers
# ---------------------------------------------------------------------------

def _is_tty() -> bool:
    """Return True if stdin is a real TTY (not a pipe or redirect)."""
    return sys.stdin.isatty()


def _read_key_nonblocking(timeout: float = 0.0) -> Optional[str]:
    """Try to read a single character from stdin without blocking.

    Returns the character string if one is available within *timeout* seconds,
    otherwise returns None.  Falls back gracefully when stdin is not a TTY.
    """
    if not _is_tty():
        return None
    try:
        rlist, _, _ = select.select([sys.stdin], [], [], timeout)
        if rlist:
            return sys.stdin.read(1)
    except Exception:
        pass
    return None


def _set_raw_mode(fd: int) -> Optional[list]:
    """Set terminal to raw mode and return old settings (or None on failure)."""
    try:
        old = termios.tcgetattr(fd)
        tty.setraw(fd)
        return old
    except Exception:
        return None


def _restore_mode(fd: int, old_settings: Optional[list]) -> None:
    """Restore terminal settings saved by _set_raw_mode."""
    if old_settings is not None:
        try:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Step status panel
# ---------------------------------------------------------------------------

def _build_status_panel(
    step_idx: int,
    total_steps: int,
    description: str,
    extra: str,
    paused: bool,
) -> Panel:
    """Build a small status/info panel shown below the map."""
    t = Text()
    t.append(f"  Step {step_idx + 1}/{total_steps}", style="bold cyan")
    if paused:
        t.append("  [PAUSED — press Space to resume]", style="bold yellow")
    else:
        t.append("  [Space: pause]", style="dim")
    t.append(f"\n  {description}", style="white")
    if extra:
        t.append(f"\n  {extra}", style="dim cyan")
    return Panel(t, title="[dim]Status[/]", border_style="bright_black", padding=(0, 1))


# ---------------------------------------------------------------------------
# Main animation entry point
# ---------------------------------------------------------------------------

def animate_steps(
    steps: List[Tuple[Any, str, str]],
    gmap,
    solution_path: Optional[List[Tuple[int, int]]] = None,
    console: Optional[Console] = None,
) -> None:
    """Animate a list of algorithm steps using Rich Live.

    Args:
        steps:          List of (state, description, extra_info) tuples produced
                        by an algorithm function in warfront.core.algorithms.
                        For map-based algorithms, *state* should be a DiffSnapshot.
                        For non-map algorithms, *state* is ignored for map rendering
                        and only description/extra_info are shown in the status panel.
        gmap:           The live GameMap object used for the map panel.  The map is
                        updated from DiffSnapshot states when possible.
        solution_path:  Optional list of (r, c) tuples representing the final
                        solution path (used for post-animation display).
        console:        Optional Rich Console instance; a default one is created if
                        not provided.
    """
    if console is None:
        console = Console()

    if not steps:
        console.print("[yellow]No steps to animate.[/]")
        return

    total_steps = len(steps)
    paused = False
    fd = sys.stdin.fileno() if _is_tty() else -1
    old_settings = _set_raw_mode(fd) if fd >= 0 else None

    # Import snapshot utilities for map reconstruction
    try:
        from warfront.core.snapshot import apply_snapshot, snapshot as full_snapshot
        from warfront.core.snapshot import DiffSnapshot
        _has_snapshot = True
        # Capture a clean baseline before any animation touches the map
        baseline = full_snapshot(gmap)
    except Exception:
        _has_snapshot = False
        baseline = None

    try:
        refresh_per_second = max(4, int(1.0 / max(cfg.animation.move_speed, 0.05)))

        with Live(console=console, refresh_per_second=refresh_per_second) as live:
            for idx, step in enumerate(steps):
                state, description, extra_info = step

                # Attempt to apply snapshot to gmap for map rendering
                if _has_snapshot and baseline is not None:
                    try:
                        # state may be a full or diff snapshot (Dict[(r,c), CellState])
                        if isinstance(state, dict):
                            apply_snapshot(gmap, baseline, state)
                    except Exception:
                        pass  # Silently degrade — map may not update

                # Build renderable group
                map_panel = build_map_renderable(gmap, title="Tactical Map")
                status_panel = _build_status_panel(idx, total_steps, description, extra_info, paused)

                renderables = [map_panel]
                if cfg.ui.show_legend:
                    renderables.append(build_legend())
                renderables.append(status_panel)

                live.update(Group(*renderables))

                # Timing loop with pause/resume support
                elapsed = 0.0
                step_duration = cfg.animation.move_speed

                while elapsed < step_duration or paused:
                    key = _read_key_nonblocking(timeout=0.05)
                    if key == " ":
                        paused = not paused
                        # Refresh display immediately to show pause state change
                        status_panel = _build_status_panel(
                            idx, total_steps, description, extra_info, paused
                        )
                        renderables[-1] = status_panel
                        live.update(Group(*renderables))
                    elif key == "q":
                        # Allow quitting early
                        return

                    if not paused:
                        elapsed += 0.05

    finally:
        _restore_mode(fd, old_settings)
