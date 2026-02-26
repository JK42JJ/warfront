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
    
    gmap.place_unit(3, 3, UnitType.ENEMY) # Enemy for visualization
    return gmap, start, goal

def get_test_data():
    return {}

def visualize_result(gmap, result):
    from core import snapshot
    user_path = result
    if not user_path: 
        return [(snapshot(gmap), "❌ No path found", "solve() returned an empty list")]
    
    steps = []
    cost = 0
    for i, (r, c) in enumerate(user_path):
        gmap.grid[r][c].visited = True
        gmap.grid[r][c].in_path = True
        
        if (r, c) == user_path[-1]:
            steps.append((snapshot(gmap), "🎯 Goal reached", f"Shortest path cost: {cost}"))
        else:
            # Cost calculation (Simplified: Forest=3, Calculation=10, Plain=1, River=5)
            t = gmap.grid[r][c].terrain
            if t == Terrain.FOREST: cost += 3
            elif t == Terrain.MOUNTAIN: cost += 10
            elif t == Terrain.RIVER: cost += 5
            else: cost += 1
            
        steps.append((snapshot(gmap), f"({r},{c}) Exploring", f"Current cost: {cost}"))
    return steps
