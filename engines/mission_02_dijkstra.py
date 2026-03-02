import random
from map import Terrain, UnitType

def build_map():
    from map import GameMap
    gmap = GameMap(12, 12)

    # Random terrain placement
    for _ in range(30):
        r, c = random.randint(0, 11), random.randint(0, 11)
        gmap.set_terrain(r, c, random.choice([Terrain.FOREST, Terrain.MOUNTAIN, Terrain.RIVER]))

    # Base deployment
    start, goal = (0, 0), (11, 11)
    gmap.place_unit(start[0], start[1], UnitType.ALLY)
    gmap.place_unit(goal[0], goal[1], UnitType.TARGET)

    # Ensure start and end are plains
    gmap.set_terrain(start[0], start[1], Terrain.PLAIN)
    gmap.set_terrain(goal[0], goal[1], Terrain.PLAIN)

    gmap.place_unit(3, 3, UnitType.ENEMY)
    return gmap, start, goal

def get_test_data():
    return {}

def visualize_result(gmap, result):
    """Animate the user's solve() result on the map.

    DESIGN CONTRACT: visualize ONLY what the user's solve() returned.
    Never call dijkstra_sim() or any reference algorithm here — that would
    display a correct path animation even when the user's code is wrong.
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
        label = "🎯 Target Reached!" if i == total - 1 else f"→ ({r},{c})"
        steps.append((
            snapshot(gmap),
            f"{label}  [{i + 1}/{total}]",
            f"Min-cost path: {total} steps",
        ))

    return steps or None
