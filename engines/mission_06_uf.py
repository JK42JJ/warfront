def get_test_data():
    """Union-Find Integrated Data"""
    return {
        "units": ["Alpha", "Bravo", "Charlie", "Delta", "Echo"],
        "links": [("Alpha", "Bravo"), ("Charlie", "Delta")],
        "queries": [
            ("merge", "Alpha", "Charlie"),
            ("connected", "Alpha", "Delta"),
            ("connected", "Alpha", "Echo")
        ]
    }

def build_map():
    from map import GameMap
    return GameMap(12, 12), (0, 0), (11, 11)

def visualize_result(gmap, result):
    from core import snapshot
    return [(snapshot(gmap), "✔ Frontline reorganization complete", f"Result: {result}")]
