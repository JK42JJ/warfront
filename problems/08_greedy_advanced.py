# MISSION: 08 | Greedy | general
# TITLE: Artillery Priority — Fractional Knapsack
# DESC: Maximise total threat neutralised by allowing fractional item selection
# ALGO: Greedy (Fractional Knapsack)
# MODULE: mission_08_greedy
# TIME_COMPLEXITY: O(n log n)
# SPACE_COMPLEXITY: O(n)
# DIFFICULTY: 5
"""
┌─ FRACTIONAL KNAPSACK ───────────────────────────────────────────────────────┐
│  1. Sort items by value/weight ratio (highest density first)                │
│  2. Take as much of each item as fits (can take a fraction)                 │
│  3. Unlike 0/1 knapsack, greedy is OPTIMAL here                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['capacity'] : float/int
# data['items']    : list[(name, weight, value)]
# Return: {'total_value': float, 'taken': [(name, amount),...]}
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Fractional knapsack — maximise value, fractions allowed."""
    capacity     = data['capacity']
    items_sorted = sorted(data['items'], key=lambda x: x[2] / x[1], reverse=True)
    total  = 0.0
    taken  = []

    for name, w, v in items_sorted:
        if capacity <= 0:
            break
        # TODO: amount = min(w, capacity)  — take all or just a fraction
        amount = min(w, capacity)
        total += amount * (v / w)
        taken.append((name, amount))
        capacity -= amount

    return {'total_value': round(total, 2), 'taken': taken}


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ sum of taken amounts <= original capacity
#   ✅ total_value is maximum possible
# ─────────────────────────────────────────────────────────────────────────────
