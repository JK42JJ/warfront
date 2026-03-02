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
    from core import snapshot, bfs_sim

    start = goal = None
    for r in range(gmap.rows):
        for c in range(gmap.cols):
            u = gmap.grid[r][c].unit
            if u and u.name == "ALLY":   start = (r, c)
            if u and u.name == "TARGET": goal  = (r, c)

    if not (start and goal):
        return [(snapshot(gmap), "❌ Map error", "No start/goal found")]

    gmap.reset_simulation_state()
    return bfs_sim(gmap, start, goal)
