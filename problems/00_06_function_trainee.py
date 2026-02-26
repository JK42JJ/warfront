# MISSION: 00-06 | Python Basics | trainee
# TITLE: Tactical Manual — Function Design
# DESC: Write reusable tactical functions to perform complex operations
# ALGO: Function
# MODULE: mission_00_trainee

def solve(data):
    """
    data = {
      'units':  [{'name':'A', 'atk':50, 'def':30},
                 {'name':'B', 'atk':40, 'def':60},
                 {'name':'C', 'atk':70, 'def':20}],
      'enemy_def': 45
    }
    Return: {
      'power':       Each  of Combat Power(atk - def) List,
      'can_attack':  atk > enemy_def in   Name List,
      'best_unit':   Combat Power(atk-def)        Name,
      'total_power': Total Combat Power Total
    }
    """
    units     = data['units']
    enemy_def = data['enemy_def']

    # TODO 1: Each  of Combat Power = atk - def List
    def calc_power(unit):
        return 0  # unit['atk'] - unit['def']

    power = []

    # TODO 2: atk > enemy_def in   Name List
    can_attack = []

    # TODO 3: Combat Power Maximum   Name
    best_unit = ""

    # TODO 4: Total Combat Power Total
    total_power = 0

    return {'power': power, 'can_attack': can_attack,
            'best_unit': best_unit, 'total_power': total_power}

# --- Execution Block ---
