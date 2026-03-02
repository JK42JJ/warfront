"""warfront/ranks.py — Re-export from root ranks.py for package compatibility."""
import sys
import os

# Ensure the project root is on the path
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from ranks import get_rank, TIER_INFO, TIER_ORDER, RANKS  # noqa: F401, E402
