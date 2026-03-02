# MISSION: 09 | Binary Search | nco
# TITLE: Radar Detection — Binary Search Basics
# DESC: Rapidly detect a specific coordinate in a sorted enemy position list
# ALGO: Binary Search
# MODULE: mission_09_binary
# TIME_COMPLEXITY: O(log N)
# SPACE_COMPLEXITY: O(1)
# DIFFICULTY: 3
"""
┌─ BINARY SEARCH ─────────────────────────────────────────────────────────────┐
│  1. Requires a SORTED array — check middle element each step                │
│  2. If mid < target: search right half (lo = mid + 1)                       │
│  3. If mid > target: search left half  (hi = mid - 1)                       │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['positions'] : list[int]  — sorted list of enemy coordinates
# data['target']    : int        — coordinate to find
# Return: {'found': bool, 'index': int}  (index = -1 if not found)
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Binary search — find target in sorted positions list."""
    positions = data['positions']
    target    = data['target']
    lo, hi    = 0, len(positions) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        if positions[mid] == target:
            return {'found': True, 'index': mid}
        elif positions[mid] < target:
            # TODO: lo = mid + 1  (target is in the right half)
            break
        else:
            # TODO: hi = mid - 1  (target is in the left half)
            break

    return {'found': False, 'index': -1}


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ O(log N) comparisons
#   ✅ found == True when target is in the list
# ─────────────────────────────────────────────────────────────────────────────
