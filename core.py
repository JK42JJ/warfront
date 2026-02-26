"""WARFRONT — Algorithm Engine"""
from typing import List, Tuple, Any, Dict
import heapq
from collections import deque
from map import GameMap, Terrain, Cell

def snapshot(gmap: GameMap):
    """Utility: Deep copy map for snapshots"""
    import copy
    return copy.deepcopy(gmap)

# 1. BFS — Withdrawal Operation (Shortest Path Escape)
def bfs_sim(gmap: GameMap, start: Tuple[int, int], goal: Tuple[int, int]):
    queue = deque([(start, [start])])
    visited = {start}
    steps = []
    
    steps.append((snapshot(gmap), "BFS Started — Insert start position into queue", f"Queue: {[start]}"))
    
    while queue:
        (r, c), path = queue.popleft()
        gmap.grid[r][c].visited = True
        
        if (r, c) == goal:
            # Mark path
            for pr, pc in path:
                gmap.grid[pr][pc].in_path = True
            steps.append((snapshot(gmap), f"🎯 Escape Path Found! Length: {len(path)-1}", f"Path: {path}"))
            return steps
            
        for nr, nc in gmap.get_neighbors(r, c):
            if (nr, nc) not in visited and gmap.grid[nr][nc].terrain != Terrain.WALL:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
        
        desc = f"({r},{c}) Exploring — Adding neighbors to queue"
        extra = f"Queue Size: {len(queue)} | Visited: {len(visited)} cells"
        steps.append((snapshot(gmap), desc, extra))
        
    steps.append((snapshot(gmap), "❌ No Escape Path", "All routes blocked"))
    return steps

# 2. DFS — Infiltration Operation (Stealth Path, Backtracking)
def dfs_sim(gmap: GameMap, start: Tuple[int, int], goal: Tuple[int, int]):
    stack = [(start, [start])]
    visited = {start}
    steps = []
    
    while stack:
        (r, c), path = stack.pop()
        gmap.grid[r][c].visited = True
        
        if (r, c) == goal:
            for pr, pc in path:
                gmap.grid[pr][pc].in_path = True
            steps.append((snapshot(gmap), f"🎯 Infiltration Path Found! Depth: {len(path)-1}", f"Path: {path}"))
            return steps
            
        found_next = False
        for nr, nc in gmap.get_neighbors(r, c):
            if (nr, nc) not in visited and gmap.grid[nr][nc].terrain != Terrain.WALL:
                visited.add((nr, nc))
                stack.append(((nr, nc), path + [(nr, nc)]))
                found_next = True
        
        if found_next:
            steps.append((snapshot(gmap), f"({r},{c}) Entering — Depth {len(path)}", f"Stack Depth: {len(path)} Visited: {len(visited)}"))
        else:
            # Backtracking
            steps.append((snapshot(gmap), f"({r},{c}) Backtracking — Blocked path", f"Stack Depth: {len(path)}"))
            
    return steps

# 3. Dijkstra — UAV Reconnaissance Optimal Route
def dijkstra_sim(gmap: GameMap, start: Tuple[int, int], goal: Tuple[int, int]):
    heap = [(0, start, [start])]
    visited = {}
    steps = []
    
    steps.append((snapshot(gmap), "Dijkstra Started — Start point distance=0", f"Heap: {heap}"))
    
    while heap:
        cost, (r, c), path = heapq.heappop(heap)
        
        if (r, c) in visited and visited[(r, c)] <= cost:
            continue
        visited[(r, c)] = cost
        gmap.grid[r][c].visited = True
        gmap.grid[r][c].distance = cost
        
        if (r, c) == goal:
            for pr, pc in path:
                gmap.grid[pr][pc].in_path = True
            steps.append((snapshot(gmap), f"🎯 Optimal Path Found! Total Cost: {cost}", f"Path Length: {len(path)}"))
            return steps
            
        for nr, nc in gmap.get_neighbors(r, c):
            new_cost = cost + gmap.grid[nr][nc].terrain.value[1]
            if (nr, nc) not in visited or visited[(nr, nc)] > new_cost:
                heapq.heappush(heap, (new_cost, (nr, nc), path + [(nr, nc)]))
                
        steps.append((snapshot(gmap), 
                      f"({r},{c}) Processing — Current Cost {cost}",
                      f"Heap Size: {len(heap)} | Nodes Processed: {sum(1 for row in gmap.grid for cell in row if cell.visited)}"))
                      
    steps.append((snapshot(gmap), "❌ No Reachable Path", "All routes are blocked."))
    return steps

# 4. MST (Kruskal) — Minimum Supply Route Design
def kruskal_sim(nodes: List[Tuple[int, int]], edges: List[Tuple[int, int, int, int, int]]):
    parent = {n: n for n in nodes}
    def find(n):
        if parent[n] == n: return n
        parent[n] = find(parent[n])
        return parent[n]
        
    def union(n1, n2):
        root1, root2 = find(n1), find(n2)
        if root1 != root2:
            parent[root1] = root2
            return True
        return False
        
    edges.sort(key=lambda x: x[0])
    selected = []
    steps = []
    
    for cost, u, v in edges:
        if union(u, v):
            selected.append((u, v, cost))
            steps.append((list(selected), 
                          f"Edge {u}↔{v} Added — Cost {cost}",
                          f"MST Edges: {len(selected)}/{len(nodes)-1}"))
        else:
            steps.append((list(selected), 
                          f"Edge {u}↔{v} Skipped — Cycle Formed",
                          f"Current MST Cost: {sum(e[2] for e in selected)}"))
                          
    total = sum(e[2] for e in selected)
    steps.append((list(selected), f"✅ MST Complete! Total Supply Cost: {total}", f"Connected Bases: {len(nodes)}"))
    return steps

# 5. Topological Sort — Operation Planning Order
def topological_sort_sim(tasks: List[str], deps: List[Tuple[str, str]]):
    adj = {t: [] for t in tasks}
    indegree = {t: 0 for t in tasks}
    for u, v in deps:
        adj[u].append(v)
        indegree[v] += 1
        
    queue = deque([t for t in tasks if indegree[t] == 0])
    order = []
    steps = []
    
    steps.append((list(order), list(queue), "Start — Inserting tasks with no dependencies into queue"))
    
    while queue:
        task = queue.popleft()
        order.append(task)
        steps.append((list(order), list(queue), f"'{task}' Execution Complete"))
        
        for nxt in adj[task]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
                steps.append((list(order), list(queue), f"'{nxt}' Dependencies Satisfied → Added to Queue"))
                
    if len(order) == len(tasks):
        steps.append((list(order), [], f"✅ Full Operation Plan Complete: {' → '.join(order)}"))
    else:
        steps.append((list(order), [], "❌ Cyclic Dependency Detected — Planning Impossible"))
    return steps

# 6. DP (Knapsack) — Logistics Optimization
def knapsack_sim(items: List[Tuple[str, int, int]], capacity: int):
    n = len(items)
    dp = [[0]*(capacity + 1) for _ in range(n + 1)]
    steps = []
    
    for i in range(1, n + 1):
        name, w, v = items[i-1]
        for j in range(capacity + 1):
            if w <= j:
                dp[i][j] = max(dp[i-1][j], dp[i-1][j-w] + v)
            else:
                dp[i][j] = dp[i-1][j]
        
        steps.append((dp, 
                      f"Processing Item '{name}' (Weight:{w}, Value:{v})",
                      f"Current Max Value: {dp[i][capacity]}"))
                      
    # Backtracking
    selected = []
    curr_w = capacity
    for i in range(n, 0, -1):
        if dp[i][curr_w] != dp[i-1][curr_w]:
            name, w, v = items[i-1]
            selected.append(name)
            curr_w -= w
            
    steps.append((dp, 
                  f"✅ Optimal Loading: {selected}",
                  f"Total Value: {dp[n][capacity]} | Capacity: {capacity}"))
    return steps

# 7. Union-Find — Frontline Reorganization
def union_find_sim(units: List[str], ops: List[Tuple[str, str, str]]):
    parent = {u: u for u in units}
    def find(u):
        if parent[u] == u: return u
        parent[u] = find(parent[u])
        return parent[u]
        
    def groups():
        g = {}
        for u in units:
            root = find(u)
            g.setdefault(root, []).append(u)
        return g
        
    steps = []
    # Initial state
    steps.append(({u: find(u) for u in units}, f"Initial State — {len(units)} Independent Units"))
    
    for op, a, b in ops:
        if op == "union":
            root_a, root_b = find(a), find(b)
            if root_a != root_b:
                parent[root_a] = root_b
                steps.append(({u: find(u) for u in units}, f"'{a}' ∪ '{b}' Merged — Unified into {len(groups())} frontlines"))
            else:
                steps.append(({u: find(u) for u in units}, f"'{a}', '{b}' already on same frontline — Skipping"))
                
    steps.append(({u: find(u) for u in units}, f"✅ Finalized Reorganization into {len(groups())} frontlines"))
    return steps

# 8. Greedy — Artillery Priority
def artillery_greedy_sim(targets: List[Tuple[str, int, int]], ammo: int):
    """targets: [(name, threat, ammo_cost), ...]"""
    sorted_t = sorted(targets, key=lambda x: x[1]/x[2], reverse=True)
    selected = []
    remaining = ammo
    total_threat = 0
    steps = []
    
    steps.append(([], sorted_t, f"Sorting complete based on Threat/Ammo ratio | Current Ammo: {ammo}"))
    
    for name, threat, cost in sorted_t:
        if cost <= remaining:
            remaining -= cost
            total_threat += threat
            selected.append(name)
            steps.append((list(selected), sorted_t, 
                          f"Selecting '{name}' for Artillery (Threat:{threat}, Cost:{cost}) | Remaining Ammo: {remaining}"))
        else:
            steps.append((list(selected), sorted_t, 
                          f"Skipping '{name}' — Insufficient Ammo (Required:{cost}, Remaining:{remaining})"))
                          
    steps.append((list(selected), [], f"✅ Neutralization Complete | Total Threat Removed: {total_threat} | Ammo Used: {ammo-remaining}"))
    return steps

# 9. Binary Search — Building DB / Radar Detection
def binary_search_sim(arr: List[int], target: int):
    lo, hi = 0, len(arr) - 1
    steps = []
    
    steps.append((lo, hi, -1, f"Search Started | Range: [{lo}, {hi}] | Target: {target}"))
    
    while lo <= hi:
        mid = (lo + hi) // 2
        steps.append((lo, hi, mid, f"Checking median arr[{mid}]={arr[mid]}"))
        
        if arr[mid] == target:
            steps.append((mid, mid, mid, f"✅ Target {target} Found! Index: {mid}"))
            return steps
        elif arr[mid] < target:
            lo = mid + 1
            steps.append((lo, hi, mid, f"Searching Right | New Range: [{lo}, {hi}]"))
        else:
            hi = mid - 1
            steps.append((lo, hi, mid, f"Searching Left | New Range: [{lo}, {hi}]"))
            
    steps.append((lo, hi, -1, f"❌ Target {target} Not Found"))
    return steps

# 10. Bitmasking — Security Communication Permissions
def bitmask_sim(permissions: List[str], ops: List[Tuple[str, str, str]]):
    perm_to_bit = {p: 1 << i for i, p in enumerate(permissions)}
    unit_masks = {op[0]: 0 for op in ops}
    steps = []
    
    steps.append((dict(unit_masks), None, "Security System Initialized — All units have no permissions"))
    
    for unit, action, perm in ops:
        bit = perm_to_bit[perm]
        if action == "grant":
            unit_masks[unit] |= bit
            steps.append((dict(unit_masks), (unit, perm), 
                          f"'{unit}' ← '{perm}' Permission Granted | Mask: {bin(unit_masks[unit])}"))
        elif action == "revoke":
            unit_masks[unit] &= ~bit
            steps.append((dict(unit_masks), (unit, perm), 
                          f"'{unit}' → '{perm}' Permission Revoked | Mask: {bin(unit_masks[unit])}"))
        elif action == "check":
            has = bool(unit_masks[unit] & bit)
            steps.append((dict(unit_masks), (unit, perm), 
                          f"'{unit}' '{perm}' Permission Check: {'✅ Authorized' if has else '❌ Denied'}"))
                          
    steps.append((dict(unit_masks), None, "✅ Permission Processing Complete"))
    return steps
