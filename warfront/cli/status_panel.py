"""warfront/cli/status_panel.py — Rich Panel showing execution status."""
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
    title: str = "Status",
) -> Panel:
    """Return a Rich Panel summarising an ExecutionResult.

    Layout:
        ┌─ Status ─────────────────────────────────────────┐
        │  ✅ Success  |  12.3 ms  |  T: O(n)  S: O(n)   │
        │  Attempts: 3                                      │
        └───────────────────────────────────────────────────┘

    For errors the last 5 lines of the traceback are shown.
    Border colour:
        green  → success
        red    → error
        yellow → timeout
    """
    status = result.status  # "success" | "error" | "timeout"
    is_empty = not result.result or (
        isinstance(result.result, dict) and not any(result.result.values())
    )

    # ── Border / icon ────────────────────────────────────────────────────
    if status == "timeout":
        border = "yellow"
        status_label = "[bold yellow]⏱ Timeout[/]"
    elif status == "error":
        border = "bright_red"
        status_label = "[bold red]✘ Error[/]"
    elif is_empty:
        border = "yellow"
        status_label = "[yellow]⚠  Incomplete — solve() returns empty[/]"
    else:
        border = "bright_green"
        status_label = "[bold green]✔ Success[/]"

    # ── Build text content ────────────────────────────────────────────────
    content = Text()

    # Line 1 — status | exec time | complexity
    exec_ms = f"{result.duration_ms:.1f} ms"
    content.append("  ")
    content.append_text(Text.from_markup(status_label))
    content.append(f"  |  {exec_ms}")

    if complexity is not None:
        content.append(f"  |  T: {complexity.time}  S: {complexity.space}")

    content.append("\n")

    # Line 2 — attempt counter + path info
    if isinstance(attempts, tuple):
        atts, completions = attempts
        content.append(f"  Edits: {atts}  Solved: {completions}", style="dim")
    else:
        content.append(f"  Attempts: {attempts}", style="dim")

    if status == "success" and not is_empty and isinstance(result.result, list) and len(result.result) > 0:
        content.append(f"  |  Path length: {len(result.result)} cells", style="dim")

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
        title=f"[bold]{title}[/]",
        title_align="left",
        border_style=border,
        padding=(0, 1),
    )
