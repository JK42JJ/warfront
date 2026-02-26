def get_test_data():
    """Greedy Mission Data - Restored Schema"""
    return {
        "targets": [
            # (start, end, threat)
            (1, 4, 10), (3, 5, 20), (0, 6, 30), (4, 7, 5), (8, 10, 15)
        ],
        "ammo": 50,
        "weapon_count": 2,
        "items": [
            ("SupplyA", 10, 60), ("SupplyB", 20, 100), ("SupplyC", 30, 120)
        ],
        "capacity": 50
    }

def build_map():
    from map import GameMap
    return GameMap(12, 12), (0, 0), (11, 11)

def visualize_result(gmap, result):
    from core import snapshot
    return [(snapshot(gmap), "✔ Greedy optimization complete", f"Result: {result}")]
