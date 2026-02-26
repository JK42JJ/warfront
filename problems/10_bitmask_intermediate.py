# MISSION: 10 | Bitmask | general
# TITLE: Security Communication — Bitmasking Subset
# DESC: Find unit combinations satisfying conditions using bitmasks
# ALGO: Bitmask (subset enumeration)
# MODULE: mission_10_bitmask
def solve(data):
    units    = data['units']     # Unit List (Maximum 20items)
    required = data['required']  # Required Minimum Power
    n        = len(units)
    best     = None

    for mask in range(1 << n):
        total_power = 0
        selected    = []
        for i in range(n):
            if mask >> i & 1:
                selected.append(units[i]['name'])
                total_power += units[i]['power']
        if total_power >= required:
            # TODO: Condition Satisfy Among fewest Personnel Select
            if best is None or len(selected) < len(best['selected']):
                best = {'selected': selected, 'power': total_power}

    return best or {'selected': [], 'power': 0}

# --- Execution Block ---
