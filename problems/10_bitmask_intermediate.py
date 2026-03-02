# MISSION: 10 | Bitmask | officer
# TITLE: Security Communication — Bitmask Subset Enumeration
# DESC: Find the smallest unit combination meeting required total power
# ALGO: Bitmask (subset enumeration)
# MODULE: mission_10_bitmask
# TIME_COMPLEXITY: O(n·2ⁿ)
# SPACE_COMPLEXITY: O(2ⁿ)
# DIFFICULTY: 4
"""
┌─ BITMASK SUBSET ENUMERATION ────────────────────────────────────────────────┐
│  1. Iterate mask from 0 to 2ⁿ − 1 — each mask encodes a subset             │
│  2. Bit i set in mask → include units[i] in the subset                      │
│  3. Among all valid subsets, keep the one with fewest selected units        │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['units']    : list[{'name': str, 'power': int}]  (≤ 20 items)
# data['required'] : int — minimum total power needed
# Return: {'selected': list[str], 'power': int}
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Find the minimum-size subset of units meeting required power."""
    units    = data['units']
    required = data['required']
    n        = len(units)
    best     = None

    for mask in range(1 << n):
        selected     = []
        total_power  = 0
        for i in range(n):
            if mask >> i & 1:
                selected.append(units[i]['name'])
                total_power += units[i]['power']
        if total_power >= required:
            if best is None or len(selected) < len(best['selected']):
                best = {'selected': selected, 'power': total_power}

    return best or {'selected': [], 'power': 0}


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ sum(power of selected) >= required
#   ✅ No smaller subset satisfies the requirement
# ─────────────────────────────────────────────────────────────────────────────
