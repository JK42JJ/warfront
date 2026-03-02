# MISSION: 07 | DP | general
# TITLE: Logistics Optimization — 1D Knapsack (Space Optimised)
# DESC: Optimise space from O(n·W) to O(W) using a rolling 1D DP array
# ALGO: DP (0/1 Knapsack, space optimised)
# MODULE: mission_07_dp
# TIME_COMPLEXITY: O(n·W)
# SPACE_COMPLEXITY: O(W)
# DIFFICULTY: 5
"""
┌─ 1D KNAPSACK ───────────────────────────────────────────────────────────────┐
│  1. dp[c] = max value achievable with exactly capacity c                    │
│  2. Iterate capacity in REVERSE (c → w) to avoid using item twice           │
│  3. Why reverse? Forward iteration would count the same item multiple times │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['capacity'] : int
# data['items']    : list[(name, weight, value)]
# Return: {'max_value': int}
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Space-optimised 1D knapsack."""
    capacity = data['capacity']
    items    = data['items']
    dp       = [0] * (capacity + 1)

    for name, w, v in items:
        # Iterate BACKWARDS from capacity down to w
        for c in range(capacity, w - 1, -1):
            # TODO: dp[c] = max(dp[c], dp[c-w] + v)
            pass

    return {'max_value': dp[capacity]}


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ max_value matches the 2D knapsack result
#   ✅ Uses only O(W) memory
# ─────────────────────────────────────────────────────────────────────────────
