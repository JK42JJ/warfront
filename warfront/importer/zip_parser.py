"""Parse a .zip file and extract ImportCandidate list."""

from dataclasses import dataclass, field
from typing import List
import zipfile

from warfront.importer.header_detector import AlgoEstimate, detect_algorithm


@dataclass
class ImportCandidate:
    filename: str           # original filename (path) inside the zip
    source: str             # decoded file content
    algo_estimate: AlgoEstimate


def parse_zip(zip_path: str) -> List[ImportCandidate]:
    """Open zip, find .py files, run header_detector on each.

    Args:
        zip_path: Filesystem path to a .zip archive.

    Returns:
        List of ImportCandidate, one per .py file found in the archive.
        Files that cannot be decoded as UTF-8 are skipped with a warning.

    Raises:
        FileNotFoundError: If zip_path does not exist.
        zipfile.BadZipFile: If the file is not a valid zip archive.
    """
    candidates: List[ImportCandidate] = []

    with zipfile.ZipFile(zip_path, "r") as zf:
        py_entries = [
            info for info in zf.infolist()
            if not info.is_dir() and info.filename.endswith(".py")
        ]

        for info in py_entries:
            raw_bytes = zf.read(info.filename)
            # Attempt UTF-8, fall back to latin-1 to avoid hard crashes
            try:
                source = raw_bytes.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    source = raw_bytes.decode("latin-1")
                except Exception:
                    print(f"[zip_parser] WARNING: cannot decode '{info.filename}', skipping.")
                    continue

            estimate = detect_algorithm(info.filename, source)
            candidates.append(
                ImportCandidate(
                    filename=info.filename,
                    source=source,
                    algo_estimate=estimate,
                )
            )

    return candidates
