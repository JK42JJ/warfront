"""CLI commands for `warfront import` and `warfront export`.

Entry points
------------
  warfront-import   — defined in pyproject.toml [project.scripts]
  warfront-export   — defined in pyproject.toml [project.scripts]

Usage
-----
  warfront-import import problems.zip
  warfront-import import problems.zip --problems-dir /path/to/problems
  warfront-import export --output my_progress.json
"""

import argparse
import json
import os
import re
import sys
from typing import List, Optional

from warfront.importer.header_detector import AlgoEstimate
from warfront.importer.zip_parser import ImportCandidate, parse_zip
from warfront.importer.engine_stub import write_engine_stub

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_VALID_ALGOS = [
    "bfs", "dijkstra", "dfs", "topo", "mst", "uf",
    "dp", "greedy", "binary", "bitmask", "unknown",
]

_ALGO_TO_MISSION_NO: dict = {
    "bfs":      "01",
    "dijkstra": "02",
    "dfs":      "03",
    "topo":     "04",
    "mst":      "05",
    "uf":       "06",
    "dp":       "07",
    "greedy":   "08",
    "binary":   "09",
    "bitmask":  "10",
    "unknown":  "99",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _project_root() -> str:
    """Best-effort location of the WARFRONT project root.

    Walks up from this file until we find a directory containing 'problems/'
    or falls back to the current working directory.
    """
    here = os.path.abspath(__file__)
    candidate = here
    for _ in range(8):
        candidate = os.path.dirname(candidate)
        if os.path.isdir(os.path.join(candidate, "problems")):
            return candidate
    return os.getcwd()


def _safe_id(filename: str) -> str:
    """Derive a filesystem-safe identifier from a zip entry filename."""
    stem = os.path.splitext(os.path.basename(filename))[0]
    stem = re.sub(r"[^\w]+", "_", stem).strip("_")
    return stem[:48] or "custom"


def _ask_algo(candidate: ImportCandidate) -> str:
    """Prompt the user to choose the algorithm for a low-confidence candidate."""
    print()
    print(f"  File      : {candidate.filename}")
    print(f"  Detection : {candidate.algo_estimate.algo!r}  "
          f"(confidence {candidate.algo_estimate.confidence:.0%})")
    print(f"  Evidence  : {', '.join(candidate.algo_estimate.evidence) or 'none'}")
    print()
    print("  Available algorithms:")
    for i, a in enumerate(_VALID_ALGOS, 1):
        print(f"    [{i:2d}] {a}")
    print()

    while True:
        raw = input("  Select algorithm (number or name) [Enter to keep detection]: ").strip()
        if raw == "":
            return candidate.algo_estimate.algo
        # numeric selection
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(_VALID_ALGOS):
                return _VALID_ALGOS[idx]
        # name selection
        if raw.lower() in _VALID_ALGOS:
            return raw.lower()
        print(f"  Invalid choice '{raw}'. Please enter a number 1-{len(_VALID_ALGOS)} or a name.")


def _generate_problem_file(candidate: ImportCandidate, algo: str, custom_id: str) -> str:
    """Return the source text for a WARFRONT-compatible problem file."""
    mission_no = _ALGO_TO_MISSION_NO.get(algo, "99")
    algo_upper = algo.upper()
    module_name = f"custom_{custom_id}"
    original_name = os.path.basename(candidate.filename)

    header = f"""\
# MISSION: {mission_no} | {algo_upper} | custom
# TITLE: Custom — {original_name}
# DESC: Imported from {original_name} via warfront-import
# ALGO: {algo_upper}
# MODULE: {module_name}
"""

    body = candidate.source

    # If the source already has a MISSION header, strip it to avoid duplication
    cleaned_body = re.sub(r"^#\s*MISSION:.*$", "", body, flags=re.MULTILINE)
    cleaned_body = re.sub(r"^#\s*TITLE:.*$",   "", cleaned_body, flags=re.MULTILINE)
    cleaned_body = re.sub(r"^#\s*DESC:.*$",     "", cleaned_body, flags=re.MULTILINE)
    cleaned_body = re.sub(r"^#\s*ALGO:.*$",     "", cleaned_body, flags=re.MULTILINE)
    cleaned_body = re.sub(r"^#\s*MODULE:.*$",   "", cleaned_body, flags=re.MULTILINE)
    # Collapse leading blank lines after header removal
    cleaned_body = re.sub(r"^\n{2,}", "\n", cleaned_body.lstrip("\n"))

    return header + "\n" + cleaned_body


def _write_problem_file(source: str, custom_id: str, problems_dir: str) -> str:
    """Write a problem file and return its absolute path."""
    os.makedirs(problems_dir, exist_ok=True)
    filename = f"custom_{custom_id}.py"
    dest = os.path.join(problems_dir, filename)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(source)
    return dest


# ---------------------------------------------------------------------------
# import command
# ---------------------------------------------------------------------------

def import_cmd(args=None) -> int:
    """warfront-import import <zip_path>

    Steps
    -----
    1. Parse the zip file for .py candidates.
    2. For each candidate, detect the algorithm.
    3. If confidence < 0.7, interactively ask the user.
    4. Write a problem file with WARFRONT headers into problems/.
    5. Write an engine stub into engines/.

    Returns 0 on success, non-zero on error.
    """
    parser = argparse.ArgumentParser(
        prog="warfront-import import",
        description="Import problems from a .zip file into WARFRONT.",
    )
    parser.add_argument("zip_path", help="Path to the .zip file to import")
    parser.add_argument(
        "--problems-dir",
        default=None,
        help="Target problems/ directory (default: auto-detected from project root)",
    )
    parser.add_argument(
        "--engines-dir",
        default=None,
        help="Target engines/ directory (default: auto-detected from project root)",
    )
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.7,
        help="Minimum confidence to accept auto-detection (default: 0.7)",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Skip user prompts; use detected algo even if confidence is low",
    )

    parsed = parser.parse_args(args)

    zip_path = os.path.abspath(parsed.zip_path)
    if not os.path.isfile(zip_path):
        print(f"ERROR: zip file not found: {zip_path}", file=sys.stderr)
        return 1

    root = _project_root()
    problems_dir = os.path.abspath(parsed.problems_dir) if parsed.problems_dir else os.path.join(root, "problems")
    engines_dir  = os.path.abspath(parsed.engines_dir)  if parsed.engines_dir  else os.path.join(root, "engines")

    print(f"[warfront-import] Reading: {zip_path}")

    try:
        candidates: List[ImportCandidate] = parse_zip(zip_path)
    except Exception as exc:
        print(f"ERROR: failed to parse zip: {exc}", file=sys.stderr)
        return 2

    if not candidates:
        print("No .py files found in the zip archive.")
        return 0

    print(f"[warfront-import] Found {len(candidates)} Python file(s).")

    success_count = 0
    error_count = 0

    for candidate in candidates:
        print()
        print(f"  Processing: {candidate.filename}")
        est: AlgoEstimate = candidate.algo_estimate
        print(f"    Detected algo : {est.algo!r}  (confidence {est.confidence:.0%})")

        # Determine final algo
        if est.confidence < parsed.confidence_threshold and not parsed.non_interactive:
            algo = _ask_algo(candidate)
        else:
            algo = est.algo

        custom_id = _safe_id(candidate.filename)

        # Write problem file
        try:
            problem_src = _generate_problem_file(candidate, algo, custom_id)
            problem_path = _write_problem_file(problem_src, custom_id, problems_dir)
            print(f"    Problem file  : {problem_path}")
        except OSError as exc:
            print(f"    ERROR writing problem file: {exc}", file=sys.stderr)
            error_count += 1
            continue

        # Write engine stub
        try:
            engine_path = write_engine_stub(algo, custom_id, engines_dir)
            print(f"    Engine stub   : {engine_path}")
        except OSError as exc:
            print(f"    ERROR writing engine stub: {exc}", file=sys.stderr)
            error_count += 1
            continue

        success_count += 1

    print()
    print(f"[warfront-import] Done — {success_count} imported, {error_count} error(s).")
    return 0 if error_count == 0 else 3


# ---------------------------------------------------------------------------
# export command
# ---------------------------------------------------------------------------

def export_cmd(args=None) -> int:
    """warfront-import export

    Exports current user progress from .warfront_progress.json to a file.

    Returns 0 on success, non-zero on error.
    """
    parser = argparse.ArgumentParser(
        prog="warfront-import export",
        description="Export WARFRONT progress to JSON.",
    )
    parser.add_argument(
        "--output",
        default="warfront_export.json",
        help="Output file path (default: warfront_export.json)",
    )
    parser.add_argument(
        "--progress-file",
        default=None,
        help="Path to .warfront_progress.json (default: auto-detected)",
    )

    parsed = parser.parse_args(args)

    root = _project_root()
    progress_file = (
        os.path.abspath(parsed.progress_file)
        if parsed.progress_file
        else os.path.join(root, ".warfront_progress.json")
    )
    output_path = os.path.abspath(parsed.output)

    if not os.path.isfile(progress_file):
        print(f"ERROR: progress file not found: {progress_file}", file=sys.stderr)
        return 1

    try:
        with open(progress_file, encoding="utf-8") as fh:
            progress_data = json.load(fh)
    except Exception as exc:
        print(f"ERROR: failed to read progress file: {exc}", file=sys.stderr)
        return 2

    export_payload = {
        "warfront_version": "2.0",
        "export_source": progress_file,
        "progress": progress_data,
    }

    try:
        with open(output_path, "w", encoding="utf-8") as fh:
            json.dump(export_payload, fh, indent=2)
    except OSError as exc:
        print(f"ERROR: failed to write export file: {exc}", file=sys.stderr)
        return 3

    print(f"[warfront-export] Progress exported to: {output_path}")
    return 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(args=None) -> None:
    """Entry point for the warfront-import script."""
    parser = argparse.ArgumentParser(
        prog="warfront-import",
        description="WARFRONT problem importer / exporter",
    )
    subparsers = parser.add_subparsers(dest="command")

    # -- import sub-command --
    imp = subparsers.add_parser("import", help="Import problems from a .zip file")
    imp.add_argument("zip_path", help="Path to .zip file")
    imp.add_argument("--problems-dir", default=None, help="Target problems directory")
    imp.add_argument("--engines-dir",  default=None, help="Target engines directory")
    imp.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.7,
        help="Minimum confidence to accept auto-detection (default: 0.7)",
    )
    imp.add_argument(
        "--non-interactive",
        action="store_true",
        help="Skip user prompts; use detected algo even if confidence is low",
    )

    # -- export sub-command --
    exp = subparsers.add_parser("export", help="Export current progress")
    exp.add_argument("--output", default="warfront_export.json", help="Output file")
    exp.add_argument("--progress-file", default=None, help="Path to progress JSON")

    parsed = parser.parse_args(args)

    if parsed.command == "import":
        sys.exit(import_cmd(
            [parsed.zip_path]
            + (["--problems-dir", parsed.problems_dir] if parsed.problems_dir else [])
            + (["--engines-dir",  parsed.engines_dir]  if parsed.engines_dir  else [])
            + [f"--confidence-threshold={parsed.confidence_threshold}"]
            + (["--non-interactive"] if parsed.non_interactive else [])
        ))
    elif parsed.command == "export":
        sys.exit(export_cmd(
            ["--output", parsed.output]
            + (["--progress-file", parsed.progress_file] if parsed.progress_file else [])
        ))
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
