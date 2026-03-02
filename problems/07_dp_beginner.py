# MISSION: 07 | DP | nco
# TITLE: Logistics Optimization — 0/1 Knapsack Basics
# DESC: Select supplies for maximum combat value within weight constraints
# ALGO: DP (0/1 Knapsack)
# MODULE: mission_07_dp
# TIME_COMPLEXITY: O(n·W)
# SPACE_COMPLEXITY: O(n·W)
# DIFFICULTY: 3
"""
┌─ 0/1 KNAPSACK ──────────────────────────────────────────────────────────────┐
│  1. dp[i][c] = max value using first i items with capacity c                │
│  2. For each item: either skip it (dp[i-1][c]) or take it (dp[i-1][c-w]+v) │
│  3. Backtrack through dp table to find which items were selected            │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['capacity'] : int                     — maximum weight
# data['items']    : list[(name, weight, value)]
# Return: {'max_value': int, 'selected': list[str]}
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """0/1 Knapsack — maximise value within weight capacity."""
    capacity = data['capacity']
    items    = data['items']
    n        = len(items)
    dp       = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i, (name, w, v) in enumerate(items, 1):
        for c in range(capacity + 1):
            dp[i][c] = dp[i-1][c]    # skip item i
            if c >= w:
                # TODO: dp[i][c] = max(dp[i][c], dp[i-1][c-w] + v)
                pass

    # Backtrack to find selected items
    selected, c = [], capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i-1][c]:
            selected.append(items[i-1][0])
            c -= items[i-1][1]

    return {'max_value': dp[n][capacity], 'selected': selected[::-1]}


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ max_value is optimal (not greedy)
#   ✅ total weight of selected items <= capacity
# ─────────────────────────────────────────────────────────────────────────────
