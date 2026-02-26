# MISSION: 09 | Binary Search | general
# TITLE: Radar Detection — Lower/Upper Bound
# DESC: Count enemies within a range in O(log n) using sorted detection logs
# ALGO: Binary Search (lower/upper bound)
# MODULE: mission_09_binary
def solve(data):
    arr   = sorted(data['positions'])
    lo_v  = data['range_lo']
    hi_v  = data['range_hi']

    def lower_bound(target):
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] < target: lo = mid + 1
            else:                 hi = mid
        return lo

    def upper_bound(target):
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = (lo + hi) // 2
            # TODO: arr[mid] <= target If lo = mid+1
            if arr[mid] <= target: lo = mid + 1
            else:                  hi = mid
        return lo

    lb = lower_bound(lo_v)
    ub = upper_bound(hi_v)
    return {'count': ub - lb, 'positions': arr[lb:ub]}

# --- Execution Block ---
