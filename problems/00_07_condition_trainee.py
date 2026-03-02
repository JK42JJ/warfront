# MISSION: 00-07 | Python Basics | trainee
# TITLE: Situation Assessment — Conditionals
# DESC: Classify combat situations using if/elif/else and issue commands
# ALGO: Condition
# MODULE: mission_00_trainee
# TIME_COMPLEXITY: O(1)
# SPACE_COMPLEXITY: O(1)
# DIFFICULTY: 1
"""
┌─ CONDITIONALS ──────────────────────────────────────────────────────────────┐
│  1. if / elif / else — branching logic based on conditions                  │
│  2. Compound conditions: (hp < 30) or (enemies > 5)                         │
│  3. Order matters: check the most specific condition first                  │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['hp']      : int — current HP 0–100
# data['ammo']    : int — ammo count 0–100
# data['enemies'] : int — nearby enemy count
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Assess the battlefield situation and issue the correct command."""
    hp      = data['hp']
    ammo    = data['ammo']
    enemies = data['enemies']

    # TODO 1: determine status using if/elif/else
    #   'danger'  if hp < 30 OR enemies > 5
    #   'caution' if hp < 60 OR ammo < 20
    #   'safe'    otherwise
    status = ""

    # TODO 2: determine command from status
    #   danger  → 'retreat'
    #   caution → 'hold'
    #   safe    → 'attack'
    command = ""

    # TODO 3: ammo_ok = True if ammo >= 10
    ammo_ok = False

    return {'status': status, 'command': command, 'ammo_ok': ammo_ok}


# ─────────────────────────────────────────────────────────────────────────────
# Expected output:
#   {'status': 'safe', 'command': 'attack', 'ammo_ok': True}  ← hp=80,ammo=50,enemies=2
#   {'status': 'danger', 'command': 'retreat', 'ammo_ok': False}  ← hp=20,ammo=5,enemies=1
# ─────────────────────────────────────────────────────────────────────────────
