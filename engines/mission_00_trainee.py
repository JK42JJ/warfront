import random

def get_test_data():
    """Trainee Integrated Data"""
    return {
        "code_int": 42, "code_float": 3.14, "code_str": "ALPHA_SQUAD",
        "enemies": [3, 7, 2, 9, 1, 5],
        "grid": [[0, 1, 0], [1, 1, 0], [0, 1, 1]],
        "message": "  RECON_COMPLETE_AT_BASE_ALPHA  ",
        "keyword": "BASE",
        "soldiers": ["Alpha", "Bravo", "Charlie", "Delta", "Echo"],
        "cutoff": 3,
        "bases": {"Alpha": 100, "Bravo": 200, "Charlie": 150},
        "units": [{"name": "Ghost", "atk": 50}, {"name": "Marine", "atk": 30}],
        "enemy_def": 40,
        "hp": 85, "ammo": 12,
        "waypoints": [(0,0), (5,5), (10,10)],
        "our_zones": {"Alpha", "Bravo", "Charlie"},
        "enemy_zones": {"Bravo", "Delta"},
        "recruits": [
            {'name': 'KIM', 'atk': 60, 'def': 40},
            {'name': 'LEE', 'atk': 80, 'def': 30},
            {'name': 'PARK', 'atk': 50, 'def': 70}
        ],
        "candidates": ["Sniper_A", "Rookie_B", "Scout_C", "Sniper_D"],
        "pass_score": 80
    }

def build_map():
    from map import GameMap
    return GameMap(12, 12), (0, 0), (11, 11)

def visualize_result(gmap, result):
    from core import snapshot
    return [(snapshot(gmap), "✔ Training data validation complete", f"Result: {result}")]
