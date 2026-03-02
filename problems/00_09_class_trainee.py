# MISSION: 00-09 | Python Basics | trainee
# TITLE: Force Structure — Classes and Objects
# DESC: Complete the Soldier class and organise your unit roster
# ALGO: Class & OOP
# MODULE: mission_00_trainee
# TIME_COMPLEXITY: O(n)
# SPACE_COMPLEXITY: O(n)
# DIFFICULTY: 1
"""
┌─ CLASSES ───────────────────────────────────────────────────────────────────┐
│  1. class Foo:  def __init__(self, x):  self.x = x  — constructor          │
│  2. Instance method: def method(self): return self.x                        │
│  3. Access via object: obj.method(), obj.x                                  │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['recruits'] : list[dict] — [{'name': str, 'atk': int, 'def': int}, ...]
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Build a squad from recruits and compute statistics."""
    recruits = data['recruits']

    class Soldier:
        def __init__(self, name: str, atk: int, def_: int):
            self.name = name
            self.atk  = atk
            self.def_ = def_

        def power(self) -> int:
            # TODO: return combat power = atk - def_
            return 0

        def __repr__(self) -> str:
            return f"Soldier({self.name}, pwr={self.power()})"

    soldiers = [Soldier(r['name'], r['atk'], r['def']) for r in recruits]

    names = [s.name for s in soldiers]

    # TODO 1: powers = list of each soldier's power()
    powers = []

    # TODO 2: best = name of the soldier with the highest power()
    #         Hint: max(soldiers, key=lambda s: s.power()).name
    best = ""

    # TODO 3: avg_atk = average attack score, rounded to 1 decimal
    avg_atk = 0.0

    return {'names': names, 'powers': powers,
            'best': best, 'avg_atk': avg_atk}


# ─────────────────────────────────────────────────────────────────────────────
# Expected output:
#   {'names': ['KIM','LEE','PARK'], 'powers': [20,50,-20],
#    'best': 'LEE', 'avg_atk': 63.3}
# ─────────────────────────────────────────────────────────────────────────────
