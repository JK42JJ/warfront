"""warfront/viz/table_renderer.py — Rich Table visualizer for DP tables.

Provides build_dp_table() for rendering 2-D DP grids with cell highlighting,
row dimming, and capacity labels on columns.
"""
from __future__ import annotations

from typing import List

from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def build_dp_table(
    dp: List[List[int]],
    current_row: int,
    current_col: int,
    title: str = "DP Table",
) -> Panel:
    """Render a 2-D DP table as a Rich Panel.

    Args:
        dp:          2-D list of integer values, shape [n+1][capacity+1].
        current_row: The row index currently being processed (0-based).
        current_col: The column index currently being processed (0-based).
        title:       Panel title text.

    Visual conventions:
        - Current cell  → bright green background
        - Current row   → normal white text
        - Previous rows → dimmed text
        - Header row    → yellow, showing capacity labels 0..capacity
    """
    if not dp or not dp[0]:
        return Panel(
            Text("(empty table)", style="dim"),
            title=f"[bold yellow]📊 {title}[/]",
            border_style="bright_black",
        )

    num_rows = len(dp)
    num_cols = len(dp[0])

    tbl = Table(
        show_header=True,
        header_style="bold yellow",
        border_style="bright_black",
        expand=False,
        padding=(0, 1),
    )

    # Row-label column
    tbl.add_column("item \\ cap", style="cyan", justify="right", no_wrap=True)

    # Capacity columns
    for j in range(num_cols):
        tbl.add_column(str(j), justify="right", no_wrap=True)

    # Data rows
    for i in range(num_rows):
        row_label = Text(f"i={i}", style="dim cyan" if i < current_row else "cyan")

        cells: List[Text] = []
        for j in range(num_cols):
            val = dp[i][j]
            if i == current_row and j == current_col:
                # Highlight the current cell
                cell_text = Text(str(val), style="bold bright_green on green4")
            elif i < current_row:
                # Dim completed rows
                cell_text = Text(str(val), style="dim white")
            elif i == current_row:
                # Current row, non-active column
                cell_text = Text(str(val), style="white")
            else:
                # Future rows
                cell_text = Text(str(val), style="dim bright_black")
            cells.append(cell_text)

        tbl.add_row(row_label, *cells)

    return Panel(
        tbl,
        title=f"[bold yellow]📊 {title}[/]",
        border_style="bright_black",
        padding=(0, 1),
    )
