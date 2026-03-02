import random

def build_map():
    from map import GameMap, Terrain, UnitType
    gmap = GameMap(12, 12)
    # DFS maze: periodic walls on 12x12
    for r in range(12):
        for c in range(12):
            if (r+c) % 4 == 0 and (r,c) != (0,0) and (r,c) != (11,11):
                gmap.grid[r][c].terrain = Terrain.WALL

    start, goal = (0, 0), (11, 11)
    gmap.grid[0][0].terrain = Terrain.PLAIN
    gmap.grid[11][11].terrain = Terrain.PLAIN
    gmap.place_unit(*start, UnitType.ALLY)
    gmap.place_unit(*goal, UnitType.TARGET)
    return gmap, start, goal

def get_test_data():
    return {"max_depth": 50}

def visualize_result(gmap, result):
    """Animate the user's solve() result on the map.

    DESIGN CONTRACT: visualize ONLY what the user's solve() returned.
    Never call dfs_sim() or any reference algorithm here — that would
    display a working animation even when the user's code is incomplete.
    """
    from core import snapshot

    if not result:
        return None

    gmap.reset_simulation_state()
    steps = []
    total = len(result)

    for i, (r, c) in enumerate(result):
        gmap.grid[r][c].in_path = True
        gmap.grid[r][c].visited = True
        label = "🎯 Infiltrated!" if i == total - 1 else f"→ ({r},{c})"
        steps.append((
            snapshot(gmap),
            f"{label}  [{i + 1}/{total}]",
            f"DFS path depth: {total} steps",
        ))

    return steps or None
