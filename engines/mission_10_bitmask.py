def get_test_data():
    """Bitmask Mission Data - Restored Schema"""
    # 1. Trainee/Beginner Schema
    permissions_dict = {'READ': 0, 'WRITE': 1, 'EXEC': 2, 'ADMIN': 3}
    actions_beginner = [
        ('grant', 'READ'), 
        ('grant', 'WRITE'), 
        ('check', 'READ'), 
        ('revoke', 'WRITE'), 
        ('check', 'WRITE')
    ]
    
    # 2. Intermediate/Advanced Schema
    permissions_list = ["READ", "WRITE", "EXECUTE", "ADMIN"]
    ops_advanced = [
        ("Alpha", "grant", "READ"),
        ("Alpha", "grant", "WRITE"),
        ("Alpha", "check", "READ"),
        ("Bravo", "grant", "EXECUTE"),
        ("Alpha", "revoke", "WRITE"),
        ("Alpha", "check", "WRITE")
    ]
    
    return {
        # Beginner
        "permissions": permissions_dict,
        "actions": actions_beginner,
        # Intermediate/Advanced
        "permissions_list": permissions_list, # Alias
        "ops": ops_advanced,
        "units": [
            {"name": "Recon", "power": 10},
            {"name": "Sniper", "power": 25},
            {"name": "Tank", "power": 50},
            {"name": "Artillery", "power": 40}
        ],
        "required": 60,
        # Advanced (TSP)
        "n": 4,
        "dist": [
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0]
        ]
    }

def build_map():
    from map import GameMap
    return GameMap(12, 12), (0, 0), (11, 11)

def visualize_result(gmap, result):
    from core import snapshot
    return [(snapshot(gmap), "✔ Bitmask operation complete", f"Result: {result}")]
