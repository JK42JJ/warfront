def get_test_data():
    """DP Mission Integrated Data (Beginner/Intermediate/Advanced)"""
    return {
        "items": [
            ("WeaponA", 10, 60), ("WeaponB", 20, 100), ("WeaponC", 30, 120)
        ],
        "capacity": 50,
        "seq1": "ABCDEFG",
        "seq2": "ABDCEFG",
        "grid": [
            [1, 3, 1],
            [1, 5, 1],
            [4, 2, 1]
        ]
    }

def build_map():
    from map import GameMap
    return GameMap(12, 12), (0, 0), (11, 11)

def visualize_result(gmap, result):
    from core import snapshot
    return [(snapshot(gmap), "✔ Dynamic programming processing complete", f"Result: {result}")]
