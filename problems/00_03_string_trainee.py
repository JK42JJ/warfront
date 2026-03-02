# MISSION: 00-03 | Python Basics | trainee
# TITLE: Cipher Decryption — String Processing
# DESC: Analyze enemy cipher communications and extract key information
# ALGO: String
# MODULE: mission_00_trainee
# TIME_COMPLEXITY: O(n)
# SPACE_COMPLEXITY: O(n)
# DIFFICULTY: 1
"""
┌─ STRINGS ───────────────────────────────────────────────────────────────────┐
│  1. s.split(sep) → split string into list by separator                      │
│  2. keyword in s → True if keyword appears anywhere in s                    │
│  3. s[::-1] → reversed string;  s.count(ch) → count occurrences            │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['message'] : str — e.g. "WARFRONT:ALPHA:SECTOR-7:CONFIRMED"
# data['keyword'] : str — e.g. "ALPHA"
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Decode the cipher message and extract intelligence."""
    message = data['message']
    keyword = data['keyword']

    # TODO 1: parts = message split by ':'
    parts = []

    # TODO 2: has_kw = True if keyword appears in message
    has_kw = False

    # TODO 3: reversed_msg = message reversed  ← use slicing [::-1]
    reversed_msg = ""

    # TODO 4: count = how many times 'A' appears in message
    count = 0

    return {'parts': parts, 'has_kw': has_kw,
            'reversed': reversed_msg, 'count': count}


# ─────────────────────────────────────────────────────────────────────────────
# Expected output:
#   {'parts': ['WARFRONT','ALPHA','SECTOR-7','CONFIRMED'],
#    'has_kw': True, 'reversed': 'DEMRIFNOC:7-ROTCES:AHPLA:TNORFRAW',
#    'count': 3}
# ─────────────────────────────────────────────────────────────────────────────
