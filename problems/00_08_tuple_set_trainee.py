# MISSION: 00-08 | Python Basics | trainee
# TITLE: Coordinate Recon — Tuples and Sets
# DESC: Manage coordinates with tuples and analyse engagement zones using sets
# ALGO: Tuple & Set
# MODULE: mission_00_trainee
# TIME_COMPLEXITY: O(n)
# SPACE_COMPLEXITY: O(n)
# DIFFICULTY: 1
"""
┌─ TUPLES & SETS ─────────────────────────────────────────────────────────────┐
│  1. tuple: immutable sequence — coordinates, fixed data                     │
│  2. set intersection: A & B or A.intersection(B)                            │
│  3. set difference: A - B;  union: A | B;  len(A | B) for total count      │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['our_zones']   : list[int]         — zones we control e.g. [1,2,3,4,5]
# data['enemy_zones'] : list[int]         — zones enemy controls e.g. [3,4,5,6,7]
# data['waypoints']   : list[tuple[int,int]] — route coordinates
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Compute zone overlap and extract route waypoints."""
    our   = set(data['our_zones'])
    enemy = set(data['enemy_zones'])
    wps   = data['waypoints']

    # TODO 1: contested = zones controlled by BOTH sides  ← set intersection
    contested = set()

    # TODO 2: only_ours = zones we control but enemy does NOT  ← set difference
    only_ours = set()

    # TODO 3: all_zones = total unique zones (ours + enemy)  ← len of union
    all_zones = 0

    # TODO 4: mid_point = the middle waypoint tuple  ← wps[len(wps)//2]
    mid_point = (0, 0)

    return {
        'contested': sorted(contested),
        'only_ours': sorted(only_ours),
        'all_zones': all_zones,
        'mid_point': mid_point,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Expected output:
#   {'contested': [3,4,5], 'only_ours': [1,2], 'all_zones': 7, 'mid_point': (1,2)}
# ─────────────────────────────────────────────────────────────────────────────
