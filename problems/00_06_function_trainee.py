# MISSION: 00-06 | Python Basics | trainee
# TITLE: Tactical Manual — Function Design
# DESC: Write reusable tactical functions to perform complex operations
# ALGO: Function
# MODULE: mission_00_trainee
# TIME_COMPLEXITY: O(n)
# SPACE_COMPLEXITY: O(n)
# DIFFICULTY: 1
"""
┌─ FUNCTIONS ─────────────────────────────────────────────────────────────────┐
│  1. def name(params): — define a function with a return value               │
│  2. Functions can be passed as arguments: max(lst, key=func)                │
│  3. List comprehension with function call: [f(x) for x in lst]             │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['units']     : list[dict] — [{'name': str, 'atk': int, 'def': int}, ...]
# data['enemy_def'] : int        — enemy defence threshold
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Evaluate each unit's combat effectiveness."""
    units     = data['units']
    enemy_def = data['enemy_def']

    # Helper — fill in the body
    def calc_power(unit: dict) -> int:
        # TODO: return atk - def_  (combat power)
        return 0

    # TODO 1: power = list of combat power for each unit using calc_power()
    power = []

    # TODO 2: can_attack = names of units where atk > enemy_def
    can_attack = []

    # TODO 3: best_unit = name of the unit with highest combat power
    #         Hint: max(units, key=calc_power)
    best_unit = ""

    # TODO 4: total_power = sum of all combat powers
    total_power = 0

    return {'power': power, 'can_attack': can_attack,
            'best_unit': best_unit, 'total_power': total_power}


# ─────────────────────────────────────────────────────────────────────────────
# Expected output:
#   {'power': [20, -20, 50], 'can_attack': ['A','C'],
#    'best_unit': 'C', 'total_power': 50}
# ─────────────────────────────────────────────────────────────────────────────
