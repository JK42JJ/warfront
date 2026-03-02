# MISSION: 09 | Binary Search | officer
# TITLE: Radar Detection — Lower / Upper Bound
# DESC: Count enemies within a value range in O(log n) using sorted logs
# ALGO: Binary Search (lower/upper bound)
# MODULE: mission_09_binary
# TIME_COMPLEXITY: O(log N)
# SPACE_COMPLEXITY: O(1)
# DIFFICULTY: 4
"""
┌─ LOWER / UPPER BOUND ───────────────────────────────────────────────────────┐
│  1. lower_bound(t): first index where arr[i] >= t                           │
│  2. upper_bound(t): first index where arr[i] >  t                           │
│  3. Count in range [lo_v, hi_v] = upper_bound(hi_v) - lower_bound(lo_v)    │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['positions'] : list[int]  — will be sorted inside solve
# data['range_lo']  : int        — inclusive lower bound
# data['range_hi']  : int        — inclusive upper bound
# Return: {'count': int, 'positions': list[int]}
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Count values in [range_lo, range_hi] using binary search bounds."""
    arr  = sorted(data['positions'])
    lo_v = data['range_lo']
    hi_v = data['range_hi']

    def lower_bound(target: int) -> int:
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] < target:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def upper_bound(target: int) -> int:
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = (lo + hi) // 2
            # TODO: if arr[mid] <= target: lo = mid + 1   else: hi = mid
            if arr[mid] <= target:
                lo = mid + 1
            else:
                hi = mid
        return lo

    lb = lower_bound(lo_v)
    ub = upper_bound(hi_v)
    return {'count': ub - lb, 'positions': arr[lb:ub]}


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ count == len(positions in output)
#   ✅ all returned positions are within [range_lo, range_hi]
# ─────────────────────────────────────────────────────────────────────────────
