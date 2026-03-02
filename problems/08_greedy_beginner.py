# MISSION: 08 | Greedy | nco
# TITLE: Artillery Priority — Greedy Activity Selection
# DESC: Neutralise maximum targets with no time overlap (activity selection)
# ALGO: Greedy
# MODULE: mission_08_greedy
# TIME_COMPLEXITY: O(n log n)
# SPACE_COMPLEXITY: O(n)
# DIFFICULTY: 3
"""
┌─ GREEDY ACTIVITY SELECTION ─────────────────────────────────────────────────┐
│  1. Sort targets by END time (earliest finish first)                        │
│  2. Select a target if its START >= last selected target's END              │
│  3. Greedy proof: earliest-ending target never blocks more future targets   │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['targets'] : list[(start, end, threat)]  — operation time window
# Return: {'selected': [(start,end,threat),...], 'count': int}
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Activity selection — maximise non-overlapping targets hit."""
    targets_sorted = sorted(data['targets'], key=lambda x: x[1])
    selected = []
    last_end = -1

    for start, end, threat in targets_sorted:
        if start >= last_end:
            selected.append((start, end, threat))
            # TODO: update last_end = end
            pass

    return {'selected': selected, 'count': len(selected)}


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ No two selected targets overlap in time
#   ✅ count is maximised
# ─────────────────────────────────────────────────────────────────────────────
