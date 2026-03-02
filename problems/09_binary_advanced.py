# MISSION: 09 | Binary Search | general
# TITLE: Radar Detection — Parametric Search
# DESC: Maximise the minimum distance between radars using binary search on answer
# ALGO: Binary Search (Parametric)
# MODULE: mission_09_binary
# TIME_COMPLEXITY: O(N log N)
# SPACE_COMPLEXITY: O(1)
# DIFFICULTY: 5
"""
┌─ PARAMETRIC BINARY SEARCH ──────────────────────────────────────────────────┐
│  1. Binary search on the ANSWER (min_dist), not on array index              │
│  2. can_place(d): greedy — place radars at least d apart, count >= m?       │
│  3. Maximise d: if can_place(mid) → answer=mid, try larger (lo=mid+1)       │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['positions']    : list[int] — radar candidate positions (unsorted)
# data['radar_count']  : int       — number of radars to place (m)
# Return: {'max_min_distance': int}
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Maximise minimum inter-radar distance using binary search."""
    positions = sorted(data['positions'])
    m         = data['radar_count']

    def can_place(min_dist: int) -> bool:
        count, last = 1, positions[0]
        for pos in positions[1:]:
            if pos - last >= min_dist:
                count += 1
                last   = pos
        return count >= m

    lo, hi, answer = 1, positions[-1] - positions[0], 0

    while lo <= hi:
        mid = (lo + hi) // 2
        if can_place(mid):
            answer = mid
            # TODO: lo = mid + 1  (try to push distance even larger)
            lo = mid + 1
        else:
            hi = mid - 1

    return {'max_min_distance': answer}


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ can_place(answer) == True
#   ✅ can_place(answer + 1) == False
# ─────────────────────────────────────────────────────────────────────────────
