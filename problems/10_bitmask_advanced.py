# MISSION: 10 | Bitmask | general
# TITLE: Security Communication — Bitmask DP (TSP Approximation)
# DESC: Find the minimum-cost route visiting all bases using bitmask DP
# ALGO: Bitmask DP
# MODULE: mission_10_bitmask
# TIME_COMPLEXITY: O(n·2ⁿ)
# SPACE_COMPLEXITY: O(n·2ⁿ)
# DIFFICULTY: 5
"""
┌─ BITMASK DP (TSP) ──────────────────────────────────────────────────────────┐
│  1. dp[mask][i] = min cost to have visited the bases in mask, ending at i   │
│  2. Transition: for each unvisited v, update dp[mask|(1<<v)][v]             │
│  3. Final answer: min over all i of dp[full_mask][i] + dist[i][0]           │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['n']    : int              — number of bases (≤ 15)
# data['dist'] : list[list[int]] — dist[i][j] = travel cost from i to j
# Return: {'min_cost': int}
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Bitmask DP TSP — minimum cost to visit all bases and return to base 0."""
    n    = data['n']
    dist = data['dist']
    INF  = float('inf')

    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0   # start at base 0, mask = 0b...001

    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == INF:
                continue
            if not (mask >> u & 1):
                continue
            for v in range(n):
                if mask >> v & 1:
                    continue
                nxt = mask | (1 << v)
                # TODO: dp[nxt][v] = min(dp[nxt][v], dp[mask][u] + dist[u][v])
                pass

    full = (1 << n) - 1
    ans  = min(dp[full][i] + dist[i][0] for i in range(n))
    return {'min_cost': ans}


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ All n bases visited exactly once
#   ✅ Route returns to base 0
#   ✅ min_cost is optimal (exact for small n)
# ─────────────────────────────────────────────────────────────────────────────
