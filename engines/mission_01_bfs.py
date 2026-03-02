import random
from map import Terrain, UnitType

def build_map():
    from map import GameMap
    gmap = GameMap(12, 12)
    start, goal = (0, 0), (11, 11)

    # Random wall placement
    for _ in range(25):
        r, c = random.randint(0, 11), random.randint(0, 11)
        if (r, c) not in [start, goal]:
            gmap.set_terrain(r, c, Terrain.WALL)

    gmap.place_unit(start[0], start[1], UnitType.ALLY)
    gmap.place_unit(goal[0], goal[1], UnitType.TARGET)
    return gmap, start, goal

def get_test_data():
    return {}

def visualize_result(gmap, result):
    """Animate the user's solve() result on the map.

    DESIGN CONTRACT: this function must ONLY visualize what the user's solve()
    returned. Never run a reference/built-in algorithm here — doing so would
    show a "working" animation even when the user's code is incomplete or wrong,
    giving a false sense of success (regression risk).

    Returns None  → watcher shows base map + "Incomplete" status (no animation).
    Returns steps → watcher animates the user's actual path cell by cell.
    """
    from core import snapshot

    # Do not animate unless user's code produced a valid path
    if not result:
        return None

    gmap.reset_simulation_state()
    steps = []
    total = len(result)

    for i, (r, c) in enumerate(result):
        gmap.grid[r][c].in_path = True
        gmap.grid[r][c].visited = True
        label = "🎯 Escaped!" if i == total - 1 else f"→ ({r},{c})"
        steps.append((
            snapshot(gmap),
            f"{label}  [{i + 1}/{total}]",
            f"Path length: {total} steps",
        ))

    return steps or None
