import random

def build_map():
    from map import GameMap, Terrain, UnitType
    # 🎯     12x12   
    gmap = GameMap(12, 12)
    # DFS            (12x12     )
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

def visualize_result(gmap_original, user_path):
    """Use  Return  Path    DFS Search   Visualization"""
    from map import GameMap, Cell, Terrain
    from core import snapshot
        
    gmap = snapshot(gmap_original)
    
    if not user_path:
        return [(snapshot(gmap), "❌ No path found", "solve()      Return")]
        
    start, goal = user_path[0], user_path[-1]
    visited = set()
    steps = [(snapshot(gmap), "DFS Search Started", f"Start: {start}")]
    
    def _dfs(r, c, depth):
        if (r, c) in visited or gmap.grid[r][c].terrain == Terrain.WALL:
            return False
            
        visited.add((r, c))
        gmap.grid[r][c].visited = True
        gmap.grid[r][c].distance = depth # DFS     Display
        
        if (r, c) == goal:
            for pr, pc in user_path:
                gmap.grid[pr][pc].in_path = True
            steps.append((snapshot(gmap), "🎯 Target Reached! (DFS)", f"Final Depth: {depth}"))
            return True
            
        steps.append((snapshot(gmap), f"({r},{c}) Entering", f"Current Depth: {depth}"))
        
        for nr, nc in gmap.get_neighbors(r, c):
            if _dfs(nr, nc, depth + 1):
                return True
                
        #   (   )
        gmap.grid[r][c].highlight = "red"
        steps.append((snapshot(gmap), f"({r},{c}) Blocked - Backtracking", "Going back"))
        gmap.grid[r][c].highlight = None
        return False
        
    _dfs(start[0], start[1], 1)
    return steps
