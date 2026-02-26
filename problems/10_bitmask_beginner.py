# MISSION: 10 | Bitmask | nco
# TITLE: Security Communication — Bitmasking Basics
# DESC: Quickly set, check, and manage permission flags using bitwise operations
# ALGO: Bitmask
# MODULE: mission_10_bitmask
def solve(data):
    permissions = data['permissions']  # {'READ':0, 'WRITE':1, 'EXEC':2, ...}
    actions     = data['actions']      # [('grant','READ'), ('check','EXEC'), ...]
    flags = 0
    results = []
    for action, perm in actions:
        bit = 1 << permissions[perm]
        if action == 'grant':
            # TODO: Bit On
            pass
        elif action == 'revoke':
            # TODO: Bit Off
            pass
        elif action == 'check':
            results.append({'perm': perm, 'granted': bool(flags & bit)})
        elif action == 'toggle':
            # TODO: Bit Invert
            pass
    return {'final_flags': bin(flags), 'checks': results}

# --- Execution Block ---
