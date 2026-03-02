# MISSION: 00-01 | Python Basics | trainee
# TITLE: Bootcamp Entry — Variables and Types
# DESC: Handle int, float, str, bool and decrypt the cipher message
# ALGO: Variables & Types
# MODULE: mission_00_trainee
# TIME_COMPLEXITY: O(1)
# SPACE_COMPLEXITY: O(1)
# DIFFICULTY: 1
"""
┌─ VARIABLES & TYPES ────────────────────────────────────────────────────────┐
│  1. Python has 4 basic types: int, float, str, bool                        │
│  2. int() converts float/str to integer (truncates decimal)                │
│  3. String slicing: s[:3] → first 3 chars;  s.lower() → lowercase         │
└────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['code_int']   : int   — e.g. 42
# data['code_float'] : float — e.g. 3.14
# data['code_str']   : str   — e.g. "ALPHA"
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Decrypt the cipher and return analysis results."""
    code_int   = data['code_int']
    code_float = data['code_float']
    code_str   = data['code_str']

    # TODO 1: total = code_int + int(code_float)  ← convert float to int first
    total = 0

    # TODO 2: msg = first 3 chars of code_str, lowercased  ← use slicing + .lower()
    msg = ""

    # TODO 3: is_big = True if code_int > 100
    is_big = False

    return {'sum': total, 'msg': msg, 'is_big': is_big}


# ─────────────────────────────────────────────────────────────────────────────
# Expected output:
#   {'sum': 45, 'msg': 'alp', 'is_big': False}   ← for code_int=42, code_float=3.7, code_str="ALPHA"
# ─────────────────────────────────────────────────────────────────────────────
