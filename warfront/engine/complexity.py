"""AST walker that estimates time/space complexity from Python source code."""
from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ComplexityEstimate:
    time: str = "O(1)"     # e.g. "O(n²)", "O(V+E)", "O(n log n)"
    space: str = "O(1)"    # e.g. "O(n)", "O(1)"
    evidence: List[str] = field(default_factory=list)  # list of str explaining why


class _ComplexityVisitor(ast.NodeVisitor):
    """AST NodeVisitor that detects complexity patterns."""

    def __init__(self) -> None:
        self.max_loop_depth: int = 0
        self._current_loop_depth: int = 0

        self.has_heapq: bool = False
        self.has_bisect: bool = False
        self.has_lru_cache: bool = False
        self.has_deque: bool = False
        self.has_2d_listcomp: bool = False
        self.loop_count: int = 0   # total loops at any depth

        self.evidence: List[str] = []

    # ── Import detection ────────────────────────────────────────────────

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            name = alias.name.split(".")[0]
            if name == "heapq":
                self.has_heapq = True
            elif name == "bisect":
                self.has_bisect = True
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module or ""
        names = {alias.name for alias in node.names}
        if module == "heapq" or "heapq" in names:
            self.has_heapq = True
        if module == "bisect" or "bisect" in names:
            self.has_bisect = True
        if module == "collections":
            if "deque" in names:
                self.has_deque = True
        if module == "functools" and "lru_cache" in names:
            self.has_lru_cache = True
        self.generic_visit(node)

    # ── Decorator detection (lru_cache as decorator) ────────────────────

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == "lru_cache":
                self.has_lru_cache = True
            elif isinstance(decorator, ast.Attribute) and decorator.attr == "lru_cache":
                self.has_lru_cache = True
            elif (
                isinstance(decorator, ast.Call)
                and isinstance(decorator.func, (ast.Name, ast.Attribute))
            ):
                func = decorator.func
                if isinstance(func, ast.Name) and func.id == "lru_cache":
                    self.has_lru_cache = True
                elif isinstance(func, ast.Attribute) and func.attr == "lru_cache":
                    self.has_lru_cache = True
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    # ── Loop nesting depth tracking ─────────────────────────────────────

    def _enter_loop(self, node: ast.AST) -> None:
        self.loop_count += 1
        self._current_loop_depth += 1
        if self._current_loop_depth > self.max_loop_depth:
            self.max_loop_depth = self._current_loop_depth
        self.generic_visit(node)
        self._current_loop_depth -= 1

    def visit_For(self, node: ast.For) -> None:
        self._enter_loop(node)

    def visit_While(self, node: ast.While) -> None:
        self._enter_loop(node)

    # ── List comprehension detection ────────────────────────────────────

    def visit_ListComp(self, node: ast.ListComp) -> None:
        if len(node.generators) >= 2:
            self.has_2d_listcomp = True
        self.generic_visit(node)

    # ── deque() call detection (in addition to import) ──────────────────

    def visit_Call(self, node: ast.Call) -> None:
        func = node.func
        if isinstance(func, ast.Name) and func.id == "deque":
            self.has_deque = True
        elif isinstance(func, ast.Attribute) and func.attr == "deque":
            self.has_deque = True
        self.generic_visit(node)


def analyze_code(source: str) -> ComplexityEstimate:
    """Analyze Python source code string and return a ComplexityEstimate."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return ComplexityEstimate(
            time="O(?)",
            space="O(?)",
            evidence=["SyntaxError: could not parse source"],
        )

    visitor = _ComplexityVisitor()
    visitor.visit(tree)

    evidence: List[str] = []

    # ── Space complexity ────────────────────────────────────────────────
    if visitor.has_2d_listcomp:
        space = "O(n²)"
        evidence.append("2D list comprehension [[...] for ... for ...] → O(n²) space")
    elif visitor.has_deque:
        space = "O(V)"
        evidence.append("deque import → BFS queue → O(V) space")
    elif visitor.loop_count > 0:
        space = "O(n)"
        evidence.append("loop with data structure → O(n) space")
    else:
        space = "O(1)"
        evidence.append("no data structure growth detected → O(1) space")

    # ── Time complexity ─────────────────────────────────────────────────
    depth = visitor.max_loop_depth

    # BFS/deque pattern overrides simple loop analysis
    if visitor.has_deque and depth <= 1:
        base_time = "O(V+E)"
        evidence.append("deque import → BFS pattern → O(V+E) time")
    elif depth == 0:
        base_time = "O(1)"
        evidence.append("no loops detected → O(1)")
    elif depth == 1:
        base_time = "O(n)"
        evidence.append("single loop, no inner loop → O(n)")
    else:
        exp = "²" if depth == 2 else "³" if depth == 3 else f"^{depth}"
        base_time = f"O(n{exp})"
        evidence.append(f"nested {depth} loops → O(n{exp})")

    # Add log factor for heapq/bisect
    log_factor_added = False
    if visitor.has_heapq:
        evidence.append("heapq import → log factor → O(n log n)")
        log_factor_added = True
    if visitor.has_bisect:
        evidence.append("bisect import → log factor → O(n log n)")
        log_factor_added = True

    if log_factor_added:
        # Upgrade time estimate to include log factor
        if base_time == "O(1)":
            time = "O(log n)"
        elif base_time == "O(n)":
            time = "O(n log n)"
        elif base_time == "O(V+E)":
            time = "O((V+E) log V)"
        else:
            # For O(n²) etc., annotate with log
            time = base_time.rstrip(")") + " log n)"
    else:
        time = base_time

    # DP hint (lru_cache)
    if visitor.has_lru_cache:
        evidence.append("@lru_cache / lru_cache import → DP memoization pattern")

    return ComplexityEstimate(time=time, space=space, evidence=evidence)


def analyze_file(path: str) -> ComplexityEstimate:
    """Read and analyze a Python source file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()
    except OSError as exc:
        return ComplexityEstimate(
            time="O(?)",
            space="O(?)",
            evidence=[f"Could not read file: {exc}"],
        )
    return analyze_code(source)
