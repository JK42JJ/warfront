# MISSION: 00-07 | Python Basics | trainee
# TITLE: Situation Assessment — Conditionals
# DESC: Classify combat situations using if/elif/else and issue commands
# ALGO: Condition
# MODULE: mission_00_trainee

def solve(data):
    """
    data = {
      'hp':      Current HP (0~100),
      'ammo':    Ammo Count (0~100),
      'enemies': Nearby   Count
    }
    Return: {
      'status':  'danger' / 'caution' / 'safe'
                 (hp<30 or enemies>5 → danger,
                  hp<60 or ammo<20  → caution,
                  otherwise                 → safe),
      'command': 'retreat' / 'hold' / 'attack'
                 (danger→retreat, caution→hold, safe→attack),
      'ammo_ok': ammo  10  If True
    }
    """
    hp      = data['hp']
    ammo    = data['ammo']
    enemies = data['enemies']

    # TODO 1: if/elif/else with status Decision
    status = ""

    # TODO 2: status to   command Decision
    command = ""

    # TODO 3: ammo >= 10 If True
    ammo_ok = False

    return {'status': status, 'command': command, 'ammo_ok': ammo_ok}

# --- Execution Block ---
