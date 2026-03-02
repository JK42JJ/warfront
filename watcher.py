#!/usr/bin/env python3
"""watcher.py v2.0 — tmux visualization pane script.

Replaces v1 (getmtime polling + pickle IPC) with:
  - watchdog-based file watching (SolutionWatcher)
  - in-process exec() sandbox (SolutionRunner / run_solution)
  - diff-based snapshots (no deepcopy per step)
  - string-based Enum comparison (no reload bug)
  - queue.Queue IPC (no signal file TOCTOU)
  - @dataclass Config (no silent __getattr__ bug)
"""
import os
import queue
import subprocess
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
ENGINES_DIR = os.path.join(BASE_DIR, "engines")
if ENGINES_DIR not in sys.path:
    sys.path.insert(0, ENGINES_DIR)

from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from warfront.config import cfg
from warfront.data.progress import increment_attempts, mark_complete, init_db
from warfront.engine.sandbox import run_solution, ExecutionResult
from warfront.engine.watcher import SolutionWatcher
from warfront.engine.complexity import analyze_file
from warfront.viz.map_renderer import build_map_renderable, build_data_panel, build_legend
from warfront.cli.status_panel import build_status_panel

console = Console()

LOG_FILE     = os.path.join(BASE_DIR, cfg.paths.log_file)
DONE_SIGNAL  = os.path.join(BASE_DIR, cfg.paths.done_file)

init_db()


# ── Helpers ────────────────────────────────────────────────────────────────

def _write_log(filename: str, result, solve_result=None) -> None:
    lines = [f"FILE:{os.path.basename(filename)}"]
    if result.status == "success":
        is_empty = not solve_result or (
            isinstance(solve_result, dict) and not any(solve_result.values())
        )
        if is_empty:
            lines.append("⚠ No result returned yet — complete the TODO")
        else:
            lines.append("✔ Operation Successful")
            lines.append(f"\n🚀 [RETURN] {solve_result}")
        if result.stdout.strip():
            lines.append(f"\n[User Output]\n{result.stdout.strip()}")
    elif result.status == "timeout":
        lines.append(f"⏱ Timeout — {result.error}")
    else:
        lines.append(f"❌ Error\n{result.error}")
        if result.stdout.strip():
            lines.append(f"\n[Output before error]\n{result.stdout.strip()}")
    with open(LOG_FILE, "w") as f:
        f.write("\n".join(lines))


def _signal_done() -> None:
    with open(DONE_SIGNAL, "w") as f:
        f.write("done")
    time.sleep(1)
    subprocess.run(["tmux", "select-window", "-t", "warfront:MENU"], capture_output=True)


def _read_module_name(solution_path: str) -> str:
    """Extract # MODULE: value from the first 15 lines."""
    try:
        with open(solution_path, encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= 15:
                    break
                if "MODULE:" in line:
                    mod = line.split("MODULE:")[1].strip()
                    return mod if mod.lower() != "none" else "none"
    except Exception:
        pass
    return "none"


def _build_data_from_module(module_name: str):
    """Load mission module and build data dict."""
    import importlib
    from warfront.data.models import GameMap

    mission_mod = None
    if module_name != "none":
        try:
            if module_name in sys.modules:
                del sys.modules[module_name]
            mission_mod = importlib.import_module(module_name)
        except Exception:
            pass

    if mission_mod and hasattr(mission_mod, "build_map"):
        gmap, start, goal = mission_mod.build_map()
    else:
        gmap = GameMap(12, 12)
        start, goal = (0, 0), (11, 11)

    data = {"gmap": gmap, "start": start, "goal": goal}
    if mission_mod and hasattr(mission_mod, "get_test_data"):
        try:
            data.update(mission_mod.get_test_data())
        except Exception:
            pass

    return data, mission_mod


def _build_view(gmap, solution_path: str, status_result=None, complexity=None, attempts=0, step_data=None) -> Group:
    content = []
    if gmap:
        title = os.path.basename(solution_path).replace(".py", "")
        content.append(build_map_renderable(gmap, title=f"Operation: {title}"))
    if step_data:
        content.append(build_data_panel(step_data, title="Algorithm State"))
    elif status_result:
        content.append(build_status_panel(status_result, complexity=complexity, attempts=attempts))
    if cfg.ui.show_legend:
        content.append(build_legend())
    return Group(*content)


# ── Main loop ──────────────────────────────────────────────────────────────

def main(solution_path: str, mission_no: str, already_done: bool) -> None:
    file_queue: queue.Queue = queue.Queue()

    watcher = SolutionWatcher(solution_path, file_queue)
    watcher.start()

    problem_file = os.path.basename(solution_path)
    attempts = 0
    current_gmap = None
    complexity = None
    is_first_run = True
    last_result = None

    console.clear()

    with Live(None, console=console, vertical_overflow="crop", refresh_per_second=10) as live:
        # Trigger initial render
        file_queue.put(solution_path)

        while True:
            try:
                changed_path = file_queue.get(timeout=0.5)
            except queue.Empty:
                continue
            except KeyboardInterrupt:
                break

            # Count attempt (except first auto-trigger)
            if not is_first_run:
                attempts += 1
                increment_attempts(problem_file)

            # Analyze complexity (static, fast)
            try:
                complexity = analyze_file(changed_path)
            except Exception:
                complexity = None

            # Detect module name from file header
            module_name = _read_module_name(changed_path)
            data, mission_mod = _build_data_from_module(module_name)

            # Run solution in-process (with 3s timeout via runner thread)
            result: ExecutionResult = run_solution(changed_path, data)

            _write_log(changed_path, result, solve_result=result.result)

            current_gmap = data.get("gmap")
            last_result = result

            # Render error / timeout immediately
            if result.status in ("error", "timeout"):
                live.update(_build_view(current_gmap, changed_path, result, complexity, attempts))
                is_first_run = False
                continue

            # Animate steps if mission provides visualize_result
            steps = None
            if mission_mod and hasattr(mission_mod, "visualize_result"):
                try:
                    steps = mission_mod.visualize_result(data["gmap"], result.result)
                except Exception:
                    steps = None

            if steps and not (is_first_run and already_done):
                for step in steps:
                    step_gmap  = step[0]
                    step_desc  = step[1] if len(step) > 1 else ""
                    step_extra = step[2] if len(step) > 2 else ""
                    # step_gmap may be a GameMap (legacy engines) or a DiffSnapshot dict
                    if hasattr(step_gmap, "grid"):
                        current_gmap = step_gmap
                    step_data = {"Status": step_desc, "Detail": step_extra}
                    live.update(_build_view(
                        current_gmap, changed_path, result, complexity, attempts,
                        step_data=step_data,
                    ))
                    time.sleep(cfg.animation.move_speed)

            live.update(_build_view(current_gmap, changed_path, result, complexity, attempts))

            # Signal success
            is_empty = not result.result or (
                isinstance(result.result, dict) and not any(result.result.values())
            )
            if not is_empty and not is_first_run and not already_done:
                mark_complete(problem_file)
                _signal_done()

            is_first_run = False

    watcher.stop()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    _mission  = sys.argv[1]
    _sol_path = sys.argv[2]
    _already  = len(sys.argv) > 4 and sys.argv[4] == "1"
    main(_sol_path, _mission, _already)
