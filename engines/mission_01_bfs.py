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
    from core import snapshot
    if not result:
        return [(snapshot(gmap), "❌ No path found", "Check Terrain.WALL conditions")]
    
    steps = []
    for i, (r, c) in enumerate(result):
        gmap.grid[r][c].visited = True
        gmap.grid[r][c].in_path = True
        if (r, c) == result[-1]:
            steps.append((snapshot(gmap), "🎯 Goal reached", f"Escape Success! {len(result)-1} cells"))
        else:
            steps.append((snapshot(gmap), f"({r},{c}) Exploring", f"Current depth: {i}"))
    return steps
