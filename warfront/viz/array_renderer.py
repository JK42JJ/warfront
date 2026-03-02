"""warfront/viz/array_renderer.py — Horizontal bar visualizer for binary search arrays.

Provides build_array_bar() which renders an integer array with lo/mid/hi pointer
markers and target highlighting.
"""
from __future__ import annotations

from typing import List

from rich.console import Group
from rich.panel import Panel
from rich.text import Text


def build_array_bar(
    arr: List[int],
    lo: int,
    hi: int,
    mid: int,
    target: int,
    title: str = "Binary Search",
) -> Panel:
    """Render a 1-D array as a horizontal bar with search pointers.

    Args:
        arr:    The sorted integer array being searched.
        lo:     Current low-bound index (inclusive).
        hi:     Current high-bound index (inclusive).
        mid:    Current midpoint index (-1 if not yet computed / not found).
        target: The value being searched for.
        title:  Panel title text.

    Visual layout (3 lines):
        Line 1 — pointer labels above (MID marker)
        Line 2 — the array values, each cell padded to fixed width
        Line 3 — pointer labels below (LO / HI markers)
    """
    if not arr:
        return Panel(
            Text("(empty array)", style="dim"),
            title=f"[bold yellow]🔍 {title}[/]",
            border_style="bright_black",
        )

    cell_width = max(len(str(v)) for v in arr) + 2  # padding

    # -----------------------------------------------------------------------
    # Line 1 — above-array markers (MID label)
    # -----------------------------------------------------------------------
    above = Text()
    for i in range(len(arr)):
        label = " MID" if i == mid else ""
        # Pad label to cell_width characters
        above.append(label.center(cell_width), style="bold bright_cyan" if i == mid else "")
    above.append("\n")

    # -----------------------------------------------------------------------
    # Line 2 — array values
    # -----------------------------------------------------------------------
    values = Text()
    for i, v in enumerate(arr):
        val_str = str(v).center(cell_width)
        if i == mid and v == target:
            # Found!
            style = "bold bright_green on green4"
        elif i == mid:
            style = "bold bright_cyan on dark_cyan"
        elif lo <= i <= hi:
            style = "bold white"
        else:
            style = "dim bright_black"

        values.append(f"[{val_str}]", style=style)

    values.append("\n")

    # -----------------------------------------------------------------------
    # Line 3 — below-array markers (LO and HI labels)
    # -----------------------------------------------------------------------
    below = Text()
    for i in range(len(arr)):
        if i == lo and i == hi:
            label = " LO=HI"
        elif i == lo:
            label = " LO"
        elif i == hi:
            label = " HI"
        else:
            label = ""
        below.append(label.center(cell_width), style="bold bright_yellow" if label else "")

    # -----------------------------------------------------------------------
    # Status line
    # -----------------------------------------------------------------------
    status = Text()
    active_range = hi - lo + 1 if lo <= hi else 0
    status.append(f"\n  Target: ", style="dim")
    status.append(str(target), style="bold bright_yellow")
    status.append("  |  Search range: ", style="dim")
    status.append(f"[{lo}, {hi}]", style="bold white")
    status.append(f"  ({active_range} elements)", style="dim")

    if mid >= 0 and mid < len(arr):
        status.append("  |  arr[mid]=", style="dim")
        val_style = "bold bright_green" if arr[mid] == target else "bold bright_cyan"
        status.append(str(arr[mid]), style=val_style)

    body = Group(above, values, below, status)

    return Panel(
        body,
        title=f"[bold yellow]🔍 {title}[/]",
        border_style="bright_black",
        padding=(0, 1),
    )
