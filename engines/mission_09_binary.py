def get_test_data():
    """Binary Search Mission Data - Restored Schema"""
    return {
        "positions": [10, 25, 40, 55, 70, 85, 100],
        "target": 55,
        "arr": [10, 20, 20, 30, 30, 30, 40],
        "queries": [(20, 35)],
        "range_lo": 20, # Added for intermediate
        "range_hi": 35, # Added for intermediate
        "points": [1, 2, 8, 4, 9],
        "n": 3,
        "radar_count": 3 # Added for advanced
    }

def build_map():
    from map import GameMap
    return GameMap(12, 12), (0, 0), (11, 11)

def visualize_result(gmap, result):
    from core import snapshot
    return [(snapshot(gmap), "✔ Binary search complete", f"Result: {result}")]
