# MISSION: 03 | DFS | officer
# TITLE: Infiltration Operation — DFS Connected Component Search
# DESC: Determine the size of all connected regions within enemy territory
# ALGO: DFS
# MODULE: mission_03_dfs
from map import Terrain

def solve(data):
    gmap    = data['gmap']
    start   = data['start']
    visited = set()
    regions = []

    def dfs(r, c):
        stack, region = [(r,c)], []
        visited.add((r,c))
        while stack:
            cr, cc = stack.pop()
            region.append((cr,cc))
            for nr,nc in gmap.get_neighbors(cr,cc):
                if (nr,nc) not in visited and gmap.grid[nr][nc].terrain != Terrain.WALL:
                    visited.add((nr,nc))
                    # TODO: stack to Add
        return region

    for r in range(gmap.rows):
        for c in range(gmap.cols):
            if (r,c) not in visited and gmap.grid[r][c].terrain != Terrain.WALL:
                regions.append(dfs(r,c))

    largest = max(regions, key=len) if regions else []
    return largest  # Largest Connect Zone Return

# --- Execution Block ---
