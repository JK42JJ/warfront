# MISSION: 09 | Binary Search | nco
# TITLE: Radar Detection —   Search Basics
# DESC: Rapidly detect specific coordinates in a sorted enemy position list
# ALGO: Binary Search
# MODULE: mission_09_binary
def solve(data):
    positions = data['positions']  # Sorted List
    target    = data['target']
    lo, hi    = 0, len(positions) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if positions[mid] == target:
            return {'found': True, 'index': mid}
        elif positions[mid] < target:
            break # TODO: lo Update
        else:
            break # TODO: hi Update
    return {'found': False, 'index': -1}

# --- Execution Block ---
