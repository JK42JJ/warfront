# MISSION: 00-08 | Python Basics | trainee
# TITLE: Coordinate Recon — Tuples and Sets
# DESC: Manage coordinates with tuples and analyze engagement zones using sets
# ALGO: Tuple & Set
# MODULE: mission_00_trainee

def solve(data):
    """
    data = {
      'our_zones':   [1,2,3,4,5],    # Ally   Zone
      'enemy_zones': [3,4,5,6,7],    # Enemy   Zone
      'waypoints':   [(0,0),(1,2),(3,4)]  #  Maintained Coordinate (Tuple List)
    }
    Return: {
      'contested':   Engagement Zone (occupied by both, Set Intersection),
      'only_ours':   Ally    (Difference),
      'all_zones':   Total Zone Count (Union Size),
      'mid_point':   waypoints of Middle index Coordinate (Tuple)
    }
    """
    our    = set(data['our_zones'])
    enemy  = set(data['enemy_zones'])
    wps    = data['waypoints']

    # TODO 1: Intersection
    contested = set()

    # TODO 2: Difference (Ally - Enemy)
    only_ours = set()

    # TODO 3: Union Size
    all_zones = 0

    # TODO 4: Middle index (len//2) of waypoint Tuple
    mid_point = (0, 0)

    return {
        'contested': sorted(contested),
        'only_ours': sorted(only_ours),
        'all_zones': all_zones,
        'mid_point': mid_point,
    }

# --- Execution Block ---
