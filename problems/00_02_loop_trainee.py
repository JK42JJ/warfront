# MISSION: 00-02 | Python Basics | trainee
# TITLE: Building Encirclement — Loops
# DESC: Count enemies and traverse the grid using for/while loops
# ALGO: Loop
# MODULE: mission_00_trainee

def solve(data):
    """
    data = {
      'enemies': [3, 7, 2, 9, 1, 5],   # Zoneby   Count
      'grid':    [[0,1,0],[1,1,0],[0,1,1]]  # 1=   
    }
    Return: {
      'total':    enemies Total,
      'max_zone':       Index,
      'occupied': grid to  occupied cell count
    }
    """
    enemies = data['enemies']
    grid    = data['grid']

    # TODO 1: for  with enemies Total
    total = 0

    # TODO 2: Maximum Value Index (max() + index() using)
    max_zone = 0

    # TODO 3:  Among for  with grid to  occupied cell count
    occupied = 0

    return {'total': total, 'max_zone': max_zone, 'occupied': occupied}

# --- Execution Block ---
