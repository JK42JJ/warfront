# MISSION: 00-02 | Python Basics | trainee
# TITLE: Building Encirclement — Loops
# DESC: Count enemies and traverse the grid using for/while loops
# ALGO: Loop
# MODULE: mission_00_trainee
# TIME_COMPLEXITY: O(n²)
# SPACE_COMPLEXITY: O(1)
# DIFFICULTY: 1
"""
┌─ LOOPS ─────────────────────────────────────────────────────────────────────┐
│  1. for x in list: — iterate over each element                              │
│  2. sum(list) shortcut; enumerate() for index+value at once                 │
│  3. Nested loops: for row in grid: for cell in row: — scans 2D grids        │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['enemies'] : list[int]       — enemy count per zone e.g. [3, 7, 2, 9]
# data['grid']    : list[list[int]] — 2D grid, 1=occupied 0=empty
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Analyse the battlefield grid and return combat statistics."""
    enemies = data['enemies']
    grid    = data['grid']

    # TODO 1: total = sum of all enemies using a for loop (or sum())
    total = 0

    # TODO 2: max_zone = index of the zone with the most enemies
    #         Hint: use max() with a key, or find the max value first then .index()
    max_zone = 0

    # TODO 3: occupied = count of cells in grid that equal 1
    #         Hint: nested for loop over grid rows and cells
    occupied = 0

    return {'total': total, 'max_zone': max_zone, 'occupied': occupied}


# ─────────────────────────────────────────────────────────────────────────────
# Expected output:
#   {'total': 22, 'max_zone': 3, 'occupied': 5}  ← for enemies=[3,7,2,9], grid as shown
# ─────────────────────────────────────────────────────────────────────────────
