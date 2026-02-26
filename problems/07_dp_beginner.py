# MISSION: 07 | DP | nco
# TITLE: Logistics Optimization — DP Knapsack Basics
# DESC: Select supplies for maximum power within weight constraints
# ALGO: DP (0/1 Knapsack)
# MODULE: mission_07_dp
def solve(data):
    capacity = data['capacity']     # Maximum Weight
    items    = data['items']        # [(name, weight, value), ...]

    n  = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i, (name, w, v) in enumerate(items, 1):
        for c in range(capacity + 1):
            dp[i][c] = dp[i-1][c]
            if c >= w:
                # TODO: Knapsackto insertion vs   insertion Maximum Value
                pass

    # backtracking Select Item Reconstruction
    selected, c = [], capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i-1][c]:
            selected.append(items[i-1][0])
            c -= items[i-1][1]
    return {'max_value': dp[n][capacity], 'selected': selected[::-1]}

# --- Execution Block ---
