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
    from core import snapshot, dfs_sim

    start = goal = None
    for r in range(gmap.rows):
        for c in range(gmap.cols):
            u = gmap.grid[r][c].unit
            if u and u.name == "ALLY":   start = (r, c)
            if u and u.name == "TARGET": goal  = (r, c)

    if not (start and goal):
        return [(snapshot(gmap), "❌ Map error", "No start/goal found")]

    gmap.reset_simulation_state()
    return dfs_sim(gmap, start, goal)
