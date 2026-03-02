# MISSION: 00-05 | Python Basics | trainee
# TITLE: Intelligence Gathering — Dictionary
# DESC: Analyse enemy base info using a dictionary and write a tactical report
# ALGO: Dictionary
# MODULE: mission_00_trainee
# TIME_COMPLEXITY: O(n)
# SPACE_COMPLEXITY: O(n)
# DIFFICULTY: 1
"""
┌─ DICTIONARY ────────────────────────────────────────────────────────────────┐
│  1. d.items() → (key, value) pairs;  d.get(k) → safe lookup                │
│  2. [k for k,v in d.items() if cond] → filter keys by value condition      │
│  3. max(d, key=lambda k: d[k]['field']) → key of max nested value           │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['bases'] : dict — {name: {'troops': int, 'weapons': int, 'active': bool}}
#   e.g. {'ALPHA': {'troops': 120, 'weapons': 30, 'active': True}, ...}
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Compile an intelligence report on enemy bases."""
    bases = data['bases']

    # TODO 1: active_bases = list of base names where active == True
    active_bases = []

    # TODO 2: total_troops = sum of troops across all bases
    total_troops = 0

    # TODO 3: strongest = name of the base with the most troops
    #         Hint: max(bases, key=lambda name: bases[name]['troops'])
    strongest = ""

    # TODO 4: summary = {name: troops} for each base  ← dict comprehension
    summary = {}

    return {'active_bases': active_bases, 'total_troops': total_troops,
            'strongest': strongest, 'summary': summary}


# ─────────────────────────────────────────────────────────────────────────────
# Expected output:
#   {'active_bases': ['ALPHA','GAMMA'], 'total_troops': 400,
#    'strongest': 'GAMMA', 'summary': {'ALPHA':120,'BETA':80,'GAMMA':200}}
# ─────────────────────────────────────────────────────────────────────────────
