# MISSION: 00-09 | Python Basics | trainee
# TITLE: Force Structure — Classes and Objects
# DESC: Complete the Soldier class and organize your unit units
# ALGO: Class & OOP
# MODULE: mission_00_trainee

def solve(data):
    """
    data = {
      'recruits': [
        {'name': 'KIM', 'atk': 60, 'def': 40},
        {'name': 'LEE', 'atk': 80, 'def': 30},
        {'name': 'PARK','atk': 50, 'def': 70},
      ]
    }
    Return: {
      'names':      Name List,
      'powers':     Combat Power(atk-def) List,
      'best':       Combat Power Maximum Soldier Name,
      'avg_atk':    Average Attack  ( Count  1 )
    }
    """
    recruits = data['recruits']

    # TODO:   Soldier Class  Completeplease
    class Soldier:
        def __init__(self, name, atk, def_):
            self.name = name
            self.atk  = atk
            self.def_ = def_

        def power(self):
            # TODO: Combat Power = atk - def_ Return
            return 0

        def __repr__(self):
            return f"Soldier({self.name}, pwr={self.power()})"

    soldiers = [Soldier(r['name'], r['atk'], r['def']) for r in recruits]

    names  = [s.name for s in soldiers]
    powers = []   # TODO: Each Soldierof power() List
    best   = ""   # TODO: power      Soldier Name
    avg_atk = 0.0 # TODO: Average atk, round(, 1)

    return {'names': names, 'powers': powers,
            'best': best, 'avg_atk': avg_atk}

# --- Execution Block ---
