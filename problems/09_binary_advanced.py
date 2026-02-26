# MISSION: 09 | Binary Search | general
# TITLE: Radar Detection —   Search   (Parametric Search)
# DESC: Solve min-dist maximization using binary search for optimal value
# ALGO: Binary Search (Parametric)
# MODULE: mission_09_binary
def solve(data):
    # Radar Nitems  Mitems Zoneto Deployment, Adjacent Radar   Minimum Distance Maximum 
    positions = sorted(data['positions'])
    m         = data['radar_count']

    def can_place(min_dist):
        count, last = 1, positions[0]
        for pos in positions[1:]:
            if pos - last >= min_dist:
                count += 1
                last   = pos
        return count >= m

    lo, hi, answer = 1, positions[-1] - positions[0], 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if can_place(mid):
            answer = mid
            lo = mid + 1  # TODO: lo Update (larger distance Search)
        else:
            hi = mid - 1
    return {'max_min_distance': answer}

# --- Execution Block ---
