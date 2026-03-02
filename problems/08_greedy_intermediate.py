# MISSION: 08 | Greedy | officer
# TITLE: Artillery Priority — Minimum Weapons for Concurrent Targets
# DESC: Find the minimum number of artillery pieces needed to cover all targets
# ALGO: Greedy
# MODULE: mission_08_greedy
# TIME_COMPLEXITY: O(n log n)
# SPACE_COMPLEXITY: O(n)
# DIFFICULTY: 4
"""
┌─ GREEDY (INTERVAL SCHEDULING) ─────────────────────────────────────────────┐
│  1. Sort targets by start time                                               │
│  2. Track all currently active artillery pieces in a min-heap (by end time) │
│  3. When a new target starts, free artillery pieces whose end <= start       │
└─────────────────────────────────────────────────────────────────────────────┘
"""
import heapq

# ── Data Reference ────────────────────────────────────────────────────────────
# data['targets']      : list[(start, end, threat)]
# data['weapon_count'] : int — available artillery pieces
# Return: {'weapons_needed': int, 'sufficient': bool}
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Find minimum concurrent weapons needed to cover all targets."""
    targets = sorted(data['targets'], key=lambda x: x[0])
    weapons = data['weapon_count']
    heap    = []   # active weapon end-times (min-heap)
    max_concurrent = 0

    for start, end, _ in targets:
        # Free weapons whose mission ended before this target starts
        while heap and heap[0] <= start:
            heapq.heappop(heap)
        heapq.heappush(heap, end)
        # TODO: update max_concurrent = max(max_concurrent, len(heap))
        pass

    return {'weapons_needed': max_concurrent,
            'sufficient': max_concurrent <= weapons}


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ weapons_needed == peak concurrent target count
#   ✅ sufficient == True if available weapons cover the peak
# ─────────────────────────────────────────────────────────────────────────────
