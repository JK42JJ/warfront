# MISSION: 07 | DP | general
# TITLE: Logistics Optimization — DP 1D    
# DESC: Optimize space complexity from O(N*W) to O(W) using 1D arrays
# ALGO: DP (0/1 Knapsack, space optimized)
# MODULE: mission_07_dp
def solve(data):
    capacity = data['capacity']
    items    = data['items']
    dp = [0] * (capacity + 1)

    for name, w, v in items:
        # TODO:   Traversewith 1D Knapsack Implement (why must it be in reverse order?)
        for c in range(capacity, w - 1, -1):
            pass  # dp[c] = max(dp[c], dp[c-w] + v)

    return {'max_value': dp[capacity]}

# --- Execution Block ---
