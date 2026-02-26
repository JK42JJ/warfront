# MISSION: 08 | Greedy | nco
# TITLE: Artillery Priority Up — Greedy Basics
# DESC: Neutralize high-threat enemies with minimum resources (activity selection)
# ALGO: Greedy
# MODULE: mission_08_greedy
def solve(data):
    targets = data['targets']  # [(start, end, threat), ...] Operation Time
    # End Time based on Sort   without overlapping Select
    targets_sorted = sorted(targets, key=lambda x: x[1])
    selected, last_end = [], -1
    for start, end, threat in targets_sorted:
        if start >= last_end:
            selected.append((start, end, threat))
            last_end = end
            # TODO: last_end Update
    return {'selected': selected, 'count': len(selected)}

# --- Execution Block ---
