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
    from core import snapshot, dijkstra_sim

    start = goal = None
    for r in range(gmap.rows):
        for c in range(gmap.cols):
            u = gmap.grid[r][c].unit
            if u and u.name == "ALLY":   start = (r, c)
            if u and u.name == "TARGET": goal  = (r, c)

    if not (start and goal):
        return [(snapshot(gmap), "❌ Map error", "No start/goal found")]

    gmap.reset_simulation_state()
    return dijkstra_sim(gmap, start, goal)
