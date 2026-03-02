"""warfront/engine/runner.py — Thread-based execution with hard timeout.

Uses threading.Thread + threading.Timer + ctypes.PyThreadState_SetAsyncExc
to kill the user's solve() thread if it exceeds TIMEOUT_SECS (3 s).
"""
from __future__ import annotations
import ctypes
import importlib
import os
import queue
import sys
import threading
from typing import Any, Callable, Optional, Tuple

from warfront.engine.sandbox import ExecutionResult, run_solution

TIMEOUT_SECS = 3.0
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINES_DIR = os.path.join(BASE_DIR, "engines")

if ENGINES_DIR not in sys.path:
    sys.path.insert(0, ENGINES_DIR)


def _raise_in_thread(tid: int) -> None:
    """Inject KeyboardInterrupt into thread *tid* via CPython internal."""
    ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_ulong(tid),
        ctypes.py_object(TimeoutError),
    )


def _load_mission_module(module_name: str):
    """Import/reload a mission engine module by name."""
    if module_name == "none" or not module_name:
        return None
    try:
        if module_name in sys.modules:
            del sys.modules[module_name]
        return importlib.import_module(module_name)
    except Exception:
        return None


def _build_data(module_name: str):
    """Build the data dict passed to solve(), loading the mission engine."""
    from warfront.data.models import GameMap

    mission_mod = _load_mission_module(module_name)

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


class SolutionRunner:
    """Run solve() in a background thread with a 3-second timeout.

    Results are pushed to *result_queue* as ExecutionResult objects.
    """

    def __init__(self, result_queue: "queue.Queue[Tuple[ExecutionResult, Any]]") -> None:
        self._q = result_queue
        self._lock = threading.Lock()
        self._current_thread: Optional[threading.Thread] = None

    def run(self, solution_path: str, module_name: str) -> None:
        """Start a new execution (cancels any previous in-flight run)."""
        with self._lock:
            self._cancel_current()
            t = threading.Thread(
                target=self._worker,
                args=(solution_path, module_name),
                daemon=True,
            )
            self._current_thread = t
            t.start()

    def _cancel_current(self) -> None:
        """Attempt to kill the currently running thread (best-effort)."""
        t = self._current_thread
        if t is not None and t.is_alive():
            _raise_in_thread(t.ident)

    def _worker(self, solution_path: str, module_name: str) -> None:
        """Thread body: build data, run sandbox, push result."""
        timer: Optional[threading.Timer] = None
        try:
            data, mission_mod = _build_data(module_name)

            # Arm the timeout
            tid = threading.current_thread().ident
            timer = threading.Timer(TIMEOUT_SECS, _raise_in_thread, args=(tid,))
            timer.start()

            result = run_solution(solution_path, data)

            timer.cancel()

            # Collect visualisation steps if available
            steps = None
            if (
                result.status == "success"
                and mission_mod
                and hasattr(mission_mod, "visualize_result")
            ):
                try:
                    steps = mission_mod.visualize_result(data["gmap"], result.result)
                except Exception:
                    steps = None

            self._q.put((result, steps))

        except TimeoutError:
            if timer:
                timer.cancel()
            self._q.put((
                ExecutionResult(
                    status="timeout",
                    error=f"⏱ Execution exceeded {TIMEOUT_SECS}s — check for infinite loops",
                ),
                None,
            ))
        except Exception as exc:
            if timer:
                timer.cancel()
            self._q.put((
                ExecutionResult(status="error", error=str(exc)),
                None,
            ))
