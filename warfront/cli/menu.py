"""warfront/cli/menu.py — Rich Live dashboard (replaces main.py menu logic)."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from typing import List, Optional

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from warfront.cli.keybindings import (
    KEY_DOWN, KEY_DOWN2, KEY_ENTER, KEY_ESC,
    KEY_LEFT, KEY_LEFT2, KEY_NEXT, KEY_QUIT, KEY_RIGHT, KEY_RIGHT2,
    KEY_SLASH, KEY_UP, KEY_UP2,
    KEY_VIM_DOWN, KEY_VIM_LEFT, KEY_VIM_RIGHT, KEY_VIM_UP,
    get_key,
)
from warfront.config import cfg
from warfront.data.problem_loader import ProblemMeta, scan_problems
from warfront.data.progress import get_progress, increment_attempts, mark_complete
from warfront.ranks import TIER_INFO, TIER_ORDER, get_rank

# ── Paths ─────────────────────────────────────────────────────────────────────
_BASE_DIR      = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_LAUNCHER_TERM = os.path.join(_BASE_DIR, "warfront.sh")
_DONE_SIGNAL   = os.path.join(_BASE_DIR, cfg.paths.done_file)
_ATTEMPT_SIGNAL = os.path.join(_BASE_DIR, ".warfront_attempt")
_SAVES_DIR     = os.path.join(_BASE_DIR, cfg.paths.saves_dir)
_MODE_FILE     = os.path.expanduser("~/.warfront_mode")

os.makedirs(_SAVES_DIR, exist_ok=True)

console = Console()

PAGE_SIZE = cfg.ui.page_size  # default 10

# ── Filter tabs ───────────────────────────────────────────────────────────────
_FILTER_TABS = ["All", "Todo", "Done"]

# ── Difficulty stars ──────────────────────────────────────────────────────────
def _difficulty_stars(level: int) -> str:
    level = max(1, min(5, level))
    return "[yellow]" + "★" * level + "[/][dim]" + "☆" * (5 - level) + "[/]"

# ── Logo ──────────────────────────────────────────────────────────────────────
_LOGO_ART = r"""
  ██╗    ██╗ █████╗ ██████╗ ███████╗███████╗██████╗  ██████╗ ███╗   ██╗████████╗
  ██║    ██║██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗████╗  ██║╚══██╔══╝
  ██║ █╗ ██║███████║██████╔╝█████╗  █████╗  ██████╔╝██║   ██║██╔██╗ ██║   ██║
  ██║███╗██║██╔══██║██╔══██╗██╔══╝  ██╔══╝  ██╔══██╗██║   ██║██║╚██╗██║   ██║
  ╚███╔███╔╝██║  ██║██║  ██║██║     ██║     ██║  ██║╚██████╔╝██║ ╚████║   ██║"""


def _load_mode() -> str:
    """Return persisted WARFRONT_MODE (terminal or browser)."""
    mode = os.environ.get("WARFRONT_MODE", "")
    if mode:
        return mode
    if os.path.exists(_MODE_FILE):
        try:
            with open(_MODE_FILE) as f:
                return f.read().strip()
        except Exception:
            pass
    return "terminal"


def _save_mode(mode: str) -> None:
    with open(_MODE_FILE, "w") as f:
        f.write(mode)


def _filter_problems(problems: List[ProblemMeta], prog: dict, tab: str) -> List[ProblemMeta]:
    """Return problems filtered by the active tab."""
    if tab == "Todo":
        return [p for p in problems if p.file not in prog.get("completed", [])]
    if tab == "Done":
        return [p for p in problems if p.file in prog.get("completed", [])]
    return problems


def _build_paged_ui(
    prog: dict,
    problems: List[ProblemMeta],
    selected_idx: int,
    mode: str,
    active_tab: int = 0,
    command_menu: Optional[dict] = None,
) -> Group:
    total = len(problems)
    selected_idx = max(0, min(selected_idx, total - 1)) if total > 0 else 0
    start_idx = (selected_idx // PAGE_SIZE) * PAGE_SIZE
    end_idx   = min(start_idx + PAGE_SIZE, total)

    content = []

    # 1. Logo
    logo = Text(_LOGO_ART, style="bold red", no_wrap=True)
    content.append(Align.center(logo))

    # 2. Status bar — split into two lines (Claude Code style)
    all_problems = scan_problems()
    all_total    = len(all_problems)
    completed_list = prog.get("completed", [])
    done = len(completed_list)

    mode_label = (
        "[bold cyan]WEB[/]" if mode == "browser" else "[bold green]TERM[/]"
    )

    current_rank = get_rank(done)
    rank_color = current_rank.get("color", "white")
    pct = done / max(all_total, 1)
    bar_filled  = int(25 * pct)
    bar_empty   = 25 - bar_filled
    bar_filled_str = "█" * bar_filled
    bar_empty_str  = "░" * bar_empty

    total_pages  = max(1, (total - 1) // PAGE_SIZE + 1)
    current_page = (selected_idx // PAGE_SIZE) + 1 if total > 0 else 1

    tab_labels = []
    for i, tab in enumerate(_FILTER_TABS):
        if i == active_tab:
            tab_labels.append(f"[bold white on blue] {tab} [/]")
        else:
            tab_labels.append(f"[dim] {tab} [/]")
    tab_line = "  ".join(tab_labels)

    # Line 1: mode + rank + progress bar + page
    rank_line = (
        f"  {mode_label}  "
        f"{current_rank['icon']} [bold {rank_color}]{current_rank['name']}[/]  "
        f"[{rank_color}]{bar_filled_str}[/][dim]{bar_empty_str}[/]"
        f" {done}/{all_total} ({int(pct * 100)}%)"
        f"  [dim]{current_page}/{total_pages}[/]"
    )
    # Line 2: filter tabs
    status_group = Group(
        Text.from_markup(rank_line),
        Text.from_markup(f"  {tab_line}"),
    )
    content.append(Panel(status_group, border_style="bright_black", padding=(0, 1)))

    # 3. Table — all columns fixed-width so layout never shifts between pages
    table = Table(box=box.SIMPLE_HEAD, show_lines=False, expand=False, padding=(0, 1),
                  header_style="dim")
    table.add_column("",            width=2,  style="dim",      no_wrap=True)  # cursor
    table.add_column("#",           width=4,  style="dim",      no_wrap=True)  # number
    table.add_column("Difficulty",  width=14,                   no_wrap=True)  # stars
    table.add_column("Algorithm",   width=12,                   no_wrap=True)  # algo name
    table.add_column("Mission",     width=36,                   no_wrap=True, overflow="ellipsis")  # title
    table.add_column("Stat",        width=7,  justify="right",  no_wrap=True)  # tries/done
    table.add_column("Description", width=38, style="dim",      no_wrap=True, overflow="ellipsis")

    # Previous page indicator
    if start_idx > 0:
        prev_style = "bold yellow on #21262d" if selected_idx == start_idx - 1 else "dim yellow"
        table.add_row(" ", "<", "[ previous ]", "", "", "", "", style=prev_style)
    else:
        table.add_row("", "", "", "", "", "", "")

    for i in range(start_idx, start_idx + PAGE_SIZE):
        if i < total:
            p = problems[i]
            cursor    = "❯" if i == selected_idx else " "
            comp      = p.file in completed_list
            atts      = prog.get("attempts", {}).get(p.file, 0)
            rank_info = p.rank
            tier_name = TIER_INFO.get(rank_info["group"], (rank_info["group"], "white", "", ""))[0]
            grade_display = f"{rank_info['icon']} {tier_name}"
            difficulty    = int(p.difficulty or 1)
            stars         = _difficulty_stars(difficulty)
            success_count = "1" if comp else "0"

            if i == selected_idx:
                row_style = "bold white on #1c2128"
            elif comp:
                row_style = "dim"
            else:
                row_style = ""

            table.add_row(
                cursor,
                f"{i + 1:>3}",
                Text.from_markup(stars),
                grade_display,
                f"{'✅' if comp else '▶'} {p.title}",
                f"{atts}/{success_count}",
                p.desc,
                style=row_style,
            )
        else:
            table.add_row("", "", "", "", "", "", "")

    # Next page indicator
    if end_idx < total:
        next_style = "bold yellow on #21262d" if selected_idx == end_idx else "dim yellow"
        table.add_row(" ", ">", "[ next ]", "", "", "", "", style=next_style)
    else:
        table.add_row("", "", "", "", "", "", "")

    content.append(table)

    # 4. Footer / command menu
    if command_menu:
        menu_items    = command_menu["items"]
        menu_selected = command_menu["selected"]

        menu_content = Text()
        for idx, (cmd, desc) in enumerate(menu_items):
            pointer = "> " if idx == menu_selected else "  "
            style   = "bold cyan" if idx == menu_selected else "dim"
            menu_content.append(f"{pointer}{cmd:<10}", style=style)
            menu_content.append(f"{desc}\n", style="dim")

        menu_panel = Panel(
            menu_content,
            title="[bold blue]Commands[/]",
            title_align="left",
            border_style="bright_blue",
            width=45,
            padding=(1, 2),
        )
        content.append(Align.center(menu_panel))
    else:
        footer = "\n  ↑↓ navigate  Enter launch  Tab filter  n next  / cmd  q quit"
        content.append(Text(footer, style="dim", justify="center"))

    return Group(*content)


def _show_command_menu(problems: List[ProblemMeta], selected_idx: int, active_tab: int, mode: str) -> str:
    """Display the command sub-menu and return an action string."""
    menu_items = [
        ("init",   "Reset progress and saves"),
        ("mode",   "Toggle WEB/TERM mode"),
        ("clear",  "Clear terminal screen"),
        ("cancel", "Close menu"),
    ]
    menu_sel = 0

    while True:
        prog = get_progress()
        sys.stdout.write("\033[H")
        menu_data = {"items": menu_items, "selected": menu_sel}
        console.print(_build_paged_ui(prog, problems, selected_idx, mode, active_tab, command_menu=menu_data))
        sys.stdout.write("\033[J")
        sys.stdout.flush()

        key = get_key()
        if key in (KEY_UP, KEY_UP2, KEY_VIM_UP):
            menu_sel = (menu_sel - 1) % len(menu_items)
        elif key in (KEY_DOWN, KEY_DOWN2, KEY_VIM_DOWN):
            menu_sel = (menu_sel + 1) % len(menu_items)
        elif key == KEY_ENTER:
            cmd = menu_items[menu_sel][0]
            if cmd == "init":
                progress_json = os.path.join(_BASE_DIR, cfg.paths.progress_file)
                progress_db   = os.path.join(_BASE_DIR, cfg.paths.db_file)
                for path in (progress_json, progress_db):
                    if os.path.exists(path):
                        os.remove(path)
                if os.path.exists(_SAVES_DIR):
                    for fname in os.listdir(_SAVES_DIR):
                        fpath = os.path.join(_SAVES_DIR, fname)
                        if os.path.isfile(fpath):
                            os.remove(fpath)
                console.print("\n[bold red]System reset complete. Restarting...[/]")
                time.sleep(1)
                return "init"
            elif cmd == "mode":
                return "mode"
            elif cmd == "clear":
                console.clear()
                return "cancel"
            elif cmd == "cancel":
                return "cancel"
        elif key in (KEY_ESC, KEY_QUIT, KEY_SLASH):
            return "cancel"


def _launch_mission(problem: ProblemMeta, mode: str) -> None:
    """Invoke the mission launcher (browser or terminal)."""
    if os.path.exists(_ATTEMPT_SIGNAL):
        os.remove(_ATTEMPT_SIGNAL)
    if os.path.exists(_DONE_SIGNAL):
        os.remove(_DONE_SIGNAL)

    console.clear()

    if mode == "browser":
        editor_server = os.path.join(_BASE_DIR, "editor_server.py")
        save_path = os.path.join(_SAVES_DIR, problem.file)
        if not os.path.exists(save_path):
            shutil.copy(problem.path, save_path)
        subprocess.run(["pkill", "-f", "editor_server.py"], capture_output=True)
        subprocess.Popen([
            sys.executable, editor_server,
            "--problem", problem.path,
            "--savefile", save_path,
            "--mission", problem.no,
            "--rank", problem.rank["name"],
        ])
        subprocess.run(["tmux", "new-window", "-t", "warfront", "-n", "CODE"], capture_output=True)
    else:
        prog = get_progress()
        is_done = problem.file in prog.get("completed", [])
        subprocess.run([
            "bash", _LAUNCHER_TERM,
            problem.no, problem.path, "none",
            problem.rank["name"], problem.rank["bar_bg"], problem.rank["bar_fg"],
            "1" if is_done else "0",
        ])


def _wait_for_signal(problem: ProblemMeta) -> None:
    """Poll signal files until the mission ends or the user returns to MENU."""
    while True:
        try:
            if os.path.exists(_ATTEMPT_SIGNAL):
                os.remove(_ATTEMPT_SIGNAL)
                increment_attempts(problem.file)

            if os.path.exists(_DONE_SIGNAL):
                os.remove(_DONE_SIGNAL)
                mark_complete(problem.file)
                break

            result = subprocess.run(
                ["tmux", "display-message", "-p", "#W"],
                capture_output=True, text=True,
            )
            if result.stdout.strip() == "MENU":
                break
        except Exception:
            pass
        time.sleep(0.4)


def run() -> None:
    """Main entry point for the WARFRONT menu dashboard."""
    mode         = _load_mode()
    selected_idx = 0
    active_tab   = 0   # 0=All, 1=Todo, 2=Done
    last_done_file: Optional[str] = None   # track most recently completed problem

    console.clear()

    while True:
        prog          = get_progress()
        all_problems  = scan_problems()
        problems      = _filter_problems(all_problems, prog, _FILTER_TABS[active_tab])

        if not all_problems:
            console.print("[bold red]No problems found.[/]")
            break

        # Clamp selection
        selected_idx = max(0, min(selected_idx, len(problems) - 1)) if problems else 0

        sys.stdout.write("\033[H")
        console.print(_build_paged_ui(prog, problems, selected_idx, mode, active_tab))
        sys.stdout.write("\033[J")
        sys.stdout.flush()

        key = get_key()
        if not key:
            continue

        # ── Quit ─────────────────────────────────────────────────────────
        if key == KEY_QUIT:
            subprocess.run(["tmux", "kill-window", "-t", "warfront:CODE"],
                           capture_output=True)
            console.clear()
            break

        # ── Filter tab cycling via Tab key (\t) ──────────────────────────
        elif key == "\t":
            active_tab = (active_tab + 1) % len(_FILTER_TABS)
            selected_idx = 0

        # ── Command menu ─────────────────────────────────────────────────
        elif key == KEY_SLASH:
            res = _show_command_menu(problems, selected_idx, active_tab, mode)
            if res == "init":
                selected_idx = 0
                active_tab   = 0
                last_done_file = None
                console.clear()
            elif res == "mode":
                mode = "browser" if mode == "terminal" else "terminal"
                _save_mode(mode)

        # ── Launch selected mission ───────────────────────────────────────
        elif key == KEY_ENTER:
            if not problems:
                continue
            problem = problems[selected_idx]
            _launch_mission(problem, mode)
            _wait_for_signal(problem)
            last_done_file = problem.file
            console.clear()

        # ── Next problem after success ────────────────────────────────────
        elif key == KEY_NEXT:
            if last_done_file is not None and problems:
                # Find the index of the last done file in the filtered list
                for i, p in enumerate(problems):
                    if p.file == last_done_file:
                        selected_idx = min(i + 1, len(problems) - 1)
                        break
                else:
                    selected_idx = min(selected_idx + 1, len(problems) - 1)

        # ── Navigation: up ───────────────────────────────────────────────
        elif key in (KEY_UP, KEY_UP2, KEY_VIM_UP):
            start = (selected_idx // PAGE_SIZE) * PAGE_SIZE
            min_idx = start - 1 if start > 0 else 0
            if selected_idx > min_idx:
                selected_idx -= 1

        # ── Navigation: down ─────────────────────────────────────────────
        elif key in (KEY_DOWN, KEY_DOWN2, KEY_VIM_DOWN):
            total = len(problems)
            start = (selected_idx // PAGE_SIZE) * PAGE_SIZE
            end   = min(start + PAGE_SIZE, total)
            max_idx = end if end < total else end - 1
            if selected_idx < max_idx:
                selected_idx += 1

        # ── Navigation: left (page back) ─────────────────────────────────
        elif key in (KEY_LEFT, KEY_LEFT2, KEY_VIM_LEFT):
            selected_idx = max(0, selected_idx - PAGE_SIZE)

        # ── Navigation: right (page forward) ─────────────────────────────
        elif key in (KEY_RIGHT, KEY_RIGHT2, KEY_VIM_RIGHT):
            total = len(problems)
            selected_idx = min(total - 1, selected_idx + PAGE_SIZE)
