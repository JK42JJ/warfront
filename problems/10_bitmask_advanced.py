# MISSION: 10 | Bitmask | general
# TITLE: Security Communication — Bitmasking DP (Subset Traverse)
# DESC: Approximate TSP by representing visited node sets with bits
# ALGO: Bitmask DP
# MODULE: mission_10_bitmask
def solve(data):
    n    = data['n']        # Base Count (≤15)
    dist = data['dist']     # dist[i][j] = Move Cost
    INF  = float('inf')
    # dp[mask][i] = maskto corresponding Base  Visitedand ito      Minimum Cost
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # Base 0 to  Start

    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == INF:
                continue
            if not (mask >> u & 1):
                continue
            for v in range(n):
                if mask >> v & 1:
                    continue
                # TODO: Next Status Update
                nxt = mask | (1 << v)
                dp[nxt][v] = min(dp[nxt][v], dp[mask][u] + dist[u][v])

    full = (1 << n) - 1
    ans  = min(dp[full][i] + dist[i][0] for i in range(n))
    return {'min_cost': ans}

# --- Execution Block ---
