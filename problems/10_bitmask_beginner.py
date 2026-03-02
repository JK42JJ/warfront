# MISSION: 10 | Bitmask | nco
# TITLE: Security Communication — Bitmask Basics
# DESC: Set, check, revoke, and toggle permission flags using bitwise operations
# ALGO: Bitmask
# MODULE: mission_10_bitmask
# TIME_COMPLEXITY: O(n)
# SPACE_COMPLEXITY: O(1)
# DIFFICULTY: 3
"""
┌─ BITMASK ───────────────────────────────────────────────────────────────────┐
│  1. Grant  permission:  flags |=  bit   (set bit ON)                        │
│  2. Revoke permission:  flags &= ~bit   (set bit OFF)                       │
│  3. Check  permission:  bool(flags & bit) (test if bit is ON)               │
│  4. Toggle permission:  flags ^=  bit   (flip bit)                          │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['permissions'] : dict  — {'READ': 0, 'WRITE': 1, 'EXEC': 2, ...}
# data['actions']     : list[('grant'|'revoke'|'check'|'toggle', perm_name)]
# Return: {'final_flags': str (binary), 'checks': [{'perm':str,'granted':bool}]}
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Process permission actions using bitmask operations."""
    permissions = data['permissions']
    actions     = data['actions']
    flags   = 0
    results = []

    for action, perm in actions:
        bit = 1 << permissions[perm]
        if action == 'grant':
            # TODO: flags |= bit
            pass
        elif action == 'revoke':
            # TODO: flags &= ~bit
            pass
        elif action == 'check':
            results.append({'perm': perm, 'granted': bool(flags & bit)})
        elif action == 'toggle':
            # TODO: flags ^= bit
            pass

    return {'final_flags': bin(flags), 'checks': results}


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ granted == True after 'grant', False after 'revoke'
#   ✅ toggle flips the bit each time
# ─────────────────────────────────────────────────────────────────────────────
