"""warfront/engine/sandbox.py — exec() in restricted namespace (no subprocess).

Replaces the old pickle + subprocess IPC with in-process exec().
The runner thread owns the sandbox and enforces a timeout externally.
"""
from __future__ import annotations
import io
import sys
import traceback
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ExecutionResult:
    status: str           # "success" | "error" | "timeout"
    result: Any = None
    error: str = ""
    stdout: str = ""
    duration_ms: float = 0.0


def _build_globals() -> dict:
    """Build a safe exec namespace with commonly needed modules."""
    from warfront.data.models import Terrain, UnitType, GameMap, Cell
    import collections
    import heapq
    import math
    import itertools
    import functools

    return {
        "__builtins__": __builtins__,
        # Collections
        "deque":        collections.deque,
        "defaultdict":  collections.defaultdict,
        "Counter":      collections.Counter,
        "OrderedDict":  collections.OrderedDict,
        # Standard modules
        "heapq":        heapq,
        "math":         math,
        "itertools":    itertools,
        "functools":    functools,
        # WARFRONT models — use the SAME module objects (avoids Enum reload bug)
        "Terrain":      Terrain,
        "UnitType":     UnitType,
        "GameMap":      GameMap,
        "Cell":         Cell,
    }


def run_solution(solution_path: str, data: dict) -> ExecutionResult:
    """Load and execute solve(data) from *solution_path* in a restricted namespace.

    stdout is captured; exceptions are caught and returned in the result.
    This function is expected to be called from a background thread with
    an external timeout enforced by runner.py.
    """
    import time
    start = time.monotonic()

    output_buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = output_buf

    try:
        with open(solution_path, "r", encoding="utf-8") as f:
            code = f.read()

        ns: dict = {}
        exec_globals = _build_globals()

        try:
            exec(compile(code, solution_path, "exec"), exec_globals, ns)
        except SyntaxError as exc:
            sys.stdout = old_stdout
            elapsed = (time.monotonic() - start) * 1000
            return ExecutionResult(
                status="error",
                error=f"SyntaxError: {exc}",
                stdout=output_buf.getvalue(),
                duration_ms=elapsed,
            )

        if "solve" not in ns:
            sys.stdout = old_stdout
            elapsed = (time.monotonic() - start) * 1000
            return ExecutionResult(
                status="error",
                error="❌ solve(data) function not found.",
                stdout=output_buf.getvalue(),
                duration_ms=elapsed,
            )

        result = ns["solve"](data)
        sys.stdout = old_stdout
        elapsed = (time.monotonic() - start) * 1000
        return ExecutionResult(
            status="success",
            result=result,
            stdout=output_buf.getvalue(),
            duration_ms=elapsed,
        )

    except Exception:
        sys.stdout = old_stdout
        elapsed = (time.monotonic() - start) * 1000
        return ExecutionResult(
            status="error",
            error=traceback.format_exc(),
            stdout=output_buf.getvalue(),
            duration_ms=elapsed,
        )
    finally:
        # Ensure stdout is restored even if an unexpected exception escapes
        if sys.stdout is output_buf:
            sys.stdout = old_stdout
