# MISSION: 08 | Greedy | general
# TITLE: Artillery Priority Up —  Count Knapsack (Fractional Knapsack)
# DESC: Select items based on value density (fractional knapsack)
# ALGO: Greedy (Fractional Knapsack)
# MODULE: mission_08_greedy
def solve(data):
    capacity = data['capacity']
    items    = data['items']  # [(name, weight, value), ...]
    # Unit Value(value/weight) Descending Sort
    items_sorted = sorted(items, key=lambda x: x[2]/x[1], reverse=True)
    total, taken = 0.0, []
    for name, w, v in items_sorted:
        if capacity <= 0:
            break
        # TODO: all or part Select with 
        amount = min(w, capacity)
        total += amount * (v / w)
        taken.append((name, amount))
        capacity -= amount
    return {'total_value': round(total, 2), 'taken': taken}

# --- Execution Block ---
