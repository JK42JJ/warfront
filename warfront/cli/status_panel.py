"""warfront/cli/status_panel.py — Rich Panel showing execution status.

Retro phosphor-green HUD aesthetic — like a classic DEFCON terminal readout.
"""
from __future__ import annotations

from typing import Optional

from rich.panel import Panel
from rich.text import Text

from warfront.engine.sandbox import ExecutionResult
from warfront.engine.complexity import ComplexityEstimate


def build_status_panel(
    result: ExecutionResult,
    complexity: Optional[ComplexityEstimate] = None,
    attempts: int = 0,
    title: str = "Mission Status",
) -> Panel:
    """Return a Rich Panel summarising an ExecutionResult.

    Retro HUD layout:
        ┌─ ◄ Mission Status ► ──────────────────────────────┐
        │  ✔ MISSION SUCCESS  │  12.3 ms  │  T: O(n)  S: O(n)  │
        │  ATTEMPTS: 3  ·  PATH LENGTH: 14 cells              │
        └────────────────────────────────────────────────────┘

    Border colour:
        green  → success
        red    → error
        yellow → timeout / incomplete
    """
    status = result.status  # "success" | "error" | "timeout"
    is_empty = not result.result or (
        isinstance(result.result, dict) and not any(result.result.values())
    )

    # ── Border / icon ────────────────────────────────────────────────────
    if status == "timeout":
        border = "yellow"
        status_label = "[bold yellow]⏱  TIMEOUT[/]"
    elif status == "error":
        border = "red"
        status_label = "[bold red]✘  MISSION FAILED[/]"
    elif is_empty:
        border = "yellow"
        status_label = "[yellow]▸  AWAITING ORDERS — solve() returns empty[/]"
    else:
        border = "green"
        status_label = "[bold bright_green]✔  MISSION SUCCESS[/]"

    # ── Build text content ────────────────────────────────────────────────
    content = Text()

    # Line 1 — status | exec time | complexity
    exec_ms = f"{result.duration_ms:.1f} ms"
    content.append("  ")
    content.append_text(Text.from_markup(status_label))
    content.append(f"  │  {exec_ms}", style="dim green")

    if complexity is not None:
        content.append(f"  │  T: {complexity.time}  S: {complexity.space}", style="dim green")

    content.append("\n")

    # Line 2 — attempt counter + path info
    content.append("  ", style="")
    if isinstance(attempts, tuple):
        atts, completions = attempts
        content.append(f"EDITS: {atts}  ·  SOLVED: {completions}", style="dim green")
    else:
        content.append(f"ATTEMPTS: {attempts}", style="dim green")

    if status == "success" and not is_empty and isinstance(result.result, list) and len(result.result) > 0:
        content.append(f"  ·  PATH LENGTH: {len(result.result)} cells", style="dim green")

    content.append("\n")

    # Error/timeout traceback excerpt (last 3 lines)
    if status in ("error", "timeout") and result.error:
        tb_lines = result.error.strip().splitlines()
        excerpt_lines = tb_lines[-3:]
        content.append("\n")
        for line in excerpt_lines:
            content.append(f"  {line}\n", style="red")

    return Panel(
        content,
        title=f"[bold green]◄  {title}  ►[/]",
        title_align="left",
        border_style=border,
        padding=(0, 1),
    )
