"""Detect algorithm type from a Python file's filename and AST imports."""

from dataclasses import dataclass, field
from typing import List, Optional
import ast
import re

@dataclass
class AlgoEstimate:
    algo: str           # "bfs", "dijkstra", "dfs", "topo", "mst", "uf", "dp", "greedy", "binary", "bitmask", "unknown"
    confidence: float   # 0.0 - 1.0
    evidence: List[str] = field(default_factory=list)


# Ordered list of (pattern, algo, confidence) for filename matching.
# Patterns are matched against the individual tokens produced by splitting the
# filename stem on non-alphanumeric separator characters (e.g. "_", "-", ".").
# This avoids false positives from word-boundary issues with underscores.
#
# Each entry: (regex_pattern, algo, confidence)
# The pattern is tested against each token; a match on any token wins.
# More specific / longer patterns are listed first.
_FILENAME_RULES = [
    (r"^dijkstra$|^dijk$",  "dijkstra", 0.9),
    (r"^bitmask$",          "bitmask",  0.9),
    (r"^kruskal$|^mst$",    "mst",      0.9),
    (r"^knapsack$|^dp$",    "dp",       0.9),
    (r"^union$|^uf$",       "uf",       0.9),
    (r"^binary$|^bisect$",  "binary",   0.9),
    (r"^greedy$",           "greedy",   0.9),
    (r"^topo$",             "topo",     0.9),
    (r"^bfs$",              "bfs",      0.9),
    (r"^dfs$",              "dfs",      0.9),
    # Fallback substring match for names like "mybfsolver" (less common)
    (r"dijkstra|dijk",      "dijkstra", 0.75),
    (r"bitmask",            "bitmask",  0.75),
    (r"kruskal",            "mst",      0.75),
    (r"knapsack",           "dp",       0.75),
    (r"greedy",             "greedy",   0.75),
    (r"binary|bisect",      "binary",   0.75),
    (r"topo",               "topo",     0.75),
]

# AST import signals: (module, name_or_None) -> (algo_hint, weight)
# weight accumulates; multiple signals can reinforce confidence.
_IMPORT_SIGNALS = [
    # BFS
    ("collections", "deque",     "bfs",     0.6),
    ("collections", "deque",     "bfs",     0.0),  # placeholder for alias import
    # Dijkstra
    ("heapq",       None,        "dijkstra", 0.7),
    # Binary Search
    ("bisect",      None,        "binary",   0.7),
    # DP
    ("functools",   "lru_cache", "dp",       0.6),
    ("functools",   "cache",     "dp",       0.6),
]


def detect_from_filename(filename: str) -> AlgoEstimate:
    """Regex match filename patterns to algorithm type.

    The stem is split into tokens on non-alphanumeric separator characters so
    that patterns like "^bfs$" correctly match a filename like "my_bfs_solution.py".
    """
    stem = filename.lower()
    # Strip directory components and extension
    stem = re.sub(r".*[/\\]", "", stem)
    stem = re.sub(r"\.[^.]+$", "", stem)

    # Split stem into tokens on non-alphanumeric separators
    tokens = re.split(r"[^a-z0-9]+", stem)

    for pattern, algo, confidence in _FILENAME_RULES:
        # Test each token individually (covers "^bfs$" style patterns)
        for tok in tokens:
            if re.search(pattern, tok):
                return AlgoEstimate(
                    algo=algo,
                    confidence=confidence,
                    evidence=[
                        f"filename token '{tok}' in '{filename}' matches pattern '{pattern}'"
                    ],
                )
        # Also test the full stem for substring fallback patterns (no ^ / $)
        if not (pattern.startswith("^") or pattern.endswith("$")):
            if re.search(pattern, stem):
                return AlgoEstimate(
                    algo=algo,
                    confidence=confidence,
                    evidence=[f"filename stem '{stem}' matches pattern '{pattern}'"],
                )

    return AlgoEstimate(
        algo="unknown",
        confidence=0.0,
        evidence=[f"no algorithm pattern matched in filename '{filename}'"],
    )


def _collect_import_signals(source: str) -> List[tuple]:
    """Parse source with AST and return list of (algo, weight, description)."""
    signals = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return signals

    for node in ast.walk(tree):
        # import heapq / import bisect / import collections
        if isinstance(node, ast.Import):
            for alias in node.names:
                base = alias.name.split(".")[0]
                if base == "heapq":
                    signals.append(("dijkstra", 0.7, "import heapq"))
                elif base == "bisect":
                    signals.append(("binary", 0.7, "import bisect"))

        # from collections import deque
        # from functools import lru_cache / cache
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names = {alias.name for alias in node.names}
            base = module.split(".")[0]

            if base == "collections":
                if "deque" in names:
                    signals.append(("bfs", 0.6, "from collections import deque"))
            elif base == "heapq":
                signals.append(("dijkstra", 0.7, "from heapq import ..."))
            elif base == "bisect":
                signals.append(("binary", 0.7, "from bisect import ..."))
            elif base == "functools":
                if "lru_cache" in names:
                    signals.append(("dp", 0.6, "from functools import lru_cache"))
                if "cache" in names:
                    signals.append(("dp", 0.6, "from functools import cache"))

    return signals


def detect_from_imports(source: str) -> AlgoEstimate:
    """AST-analyze imports to guess algorithm."""
    signals = _collect_import_signals(source)

    if not signals:
        return AlgoEstimate(
            algo="unknown",
            confidence=0.0,
            evidence=["no recognizable algorithm imports found"],
        )

    # Accumulate weights per algo
    weights: dict = {}
    evidence: dict = {}
    for algo, weight, desc in signals:
        weights[algo] = weights.get(algo, 0.0) + weight
        evidence.setdefault(algo, []).append(desc)

    # Pick the highest-weight algo; cap confidence at 0.85 for import-only detection
    best_algo = max(weights, key=lambda a: weights[a])
    confidence = min(weights[best_algo], 0.85)

    return AlgoEstimate(
        algo=best_algo,
        confidence=confidence,
        evidence=evidence[best_algo],
    )


def detect_algorithm(filename: str, source: str) -> AlgoEstimate:
    """Combine filename and import analysis into a single estimate.

    Strategy:
    - If filename gives high confidence (>= 0.8), use it and add import evidence.
    - Otherwise average filename and import signals, preferring whichever is stronger.
    """
    fn_est = detect_from_filename(filename)
    imp_est = detect_from_imports(source)

    # Filename match is authoritative when strong
    if fn_est.confidence >= 0.8:
        combined_evidence = fn_est.evidence + imp_est.evidence
        # Slightly boost confidence if imports agree
        bonus = 0.05 if (imp_est.algo == fn_est.algo) else 0.0
        return AlgoEstimate(
            algo=fn_est.algo,
            confidence=min(fn_est.confidence + bonus, 1.0),
            evidence=combined_evidence,
        )

    # Import signal is stronger than filename
    if imp_est.confidence > fn_est.confidence:
        combined_evidence = imp_est.evidence + fn_est.evidence
        bonus = 0.05 if (fn_est.algo == imp_est.algo and fn_est.algo != "unknown") else 0.0
        return AlgoEstimate(
            algo=imp_est.algo,
            confidence=min(imp_est.confidence + bonus, 1.0),
            evidence=combined_evidence,
        )

    # Both are weak — return the best we have
    if fn_est.confidence > 0 or imp_est.confidence > 0:
        best = fn_est if fn_est.confidence >= imp_est.confidence else imp_est
        return AlgoEstimate(
            algo=best.algo,
            confidence=best.confidence,
            evidence=fn_est.evidence + imp_est.evidence,
        )

    return AlgoEstimate(
        algo="unknown",
        confidence=0.0,
        evidence=fn_est.evidence + imp_est.evidence,
    )
