"""warfront/data/problem_loader.py — Parse problem file headers → ProblemMeta"""
from __future__ import annotations
import os
import re
from dataclasses import dataclass, field
from typing import List, Optional

REQUIRED_FIELDS = {"MISSION", "TITLE", "DESC", "ALGO", "MODULE"}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@dataclass
class ProblemMeta:
    file: str
    path: str
    no: str = ""
    algo: str = ""
    level: str = ""
    title: str = ""
    desc: str = ""
    module: str = "none"
    time_complexity: str = ""
    space_complexity: str = ""
    difficulty: str = ""
    # Runtime-populated
    rank: dict = field(default_factory=dict)
    gidx: int = 0

    def is_valid(self) -> bool:
        return bool(self.no)


def parse_header(path: str) -> dict:
    """Read up to 20 comment lines from *path*, return key→value dict."""
    result = {}
    try:
        with open(path, encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= 20:
                    break
                line = line.strip()
                if not line.startswith("#"):
                    break
                m = re.match(r"#\s*([A-Z_]+):\s*(.+)", line)
                if m:
                    result[m.group(1).strip()] = m.group(2).strip()
    except Exception:
        pass
    return result


def load_problem(fname: str, problems_dir: str) -> Optional[ProblemMeta]:
    """Parse a single problem file and return ProblemMeta (or None if invalid)."""
    if not fname.endswith(".py"):
        return None
    path = os.path.join(problems_dir, fname)
    headers = parse_header(path)

    meta = ProblemMeta(file=fname, path=path, title=fname)

    mission_raw = headers.get("MISSION", "")
    if mission_raw:
        parts = [x.strip() for x in mission_raw.split("|")]
        meta.no    = (parts + ["", "", ""])[0]
        meta.algo  = (parts + ["", "", ""])[1]
        meta.level = (parts + ["", "", ""])[2]

    meta.title           = headers.get("TITLE", fname)
    meta.desc            = headers.get("DESC", "")
    meta.module          = headers.get("MODULE", "none")
    meta.time_complexity  = headers.get("TIME_COMPLEXITY", "")
    meta.space_complexity = headers.get("SPACE_COMPLEXITY", "")
    meta.difficulty       = headers.get("DIFFICULTY", "")

    return meta if meta.is_valid() else None


def scan_problems(problems_dir: Optional[str] = None) -> List[ProblemMeta]:
    """Scan *problems_dir* and return list of valid ProblemMeta sorted by filename."""
    if problems_dir is None:
        from warfront.config import cfg
        problems_dir = os.path.join(BASE_DIR, cfg.paths.problems_dir)

    if not os.path.isdir(problems_dir):
        return []

    from warfront.ranks import get_rank  # local import to avoid circular deps

    _LEVEL_RANK = {"trainee": 0, "beginner": 1, "intermediate": 2, "advanced": 3}

    def _problem_sort_key(fname: str) -> tuple:
        level = 0
        for suffix, rank in _LEVEL_RANK.items():
            if f"_{suffix}" in fname:
                level = rank
                break
        num = fname.split("_")[0]   # "00", "01", ... "10"
        return (level, num, fname)

    problems = []
    for fname in sorted(os.listdir(problems_dir), key=_problem_sort_key):
        meta = load_problem(fname, problems_dir)
        if meta:
            problems.append(meta)

    for i, p in enumerate(problems):
        p.gidx = i
        p.rank = get_rank(i)

    return problems
