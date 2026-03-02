"""warfront/core/algorithms.py — Pure algorithm logic (port of core.py).

All 10 algorithm simulation functions return:
    List[Tuple[state, description, extra_info]]

For map-based algorithms (bfs, dfs, dijkstra), state is a DiffSnapshot
(Dict[Tuple[int,int], CellState]) produced by warfront.core.snapshot.

For non-map algorithms (kruskal, topo, knapsack, union_find, greedy,
binary_search, bitmask), state is a plain Python data structure.

Terrain/Unit comparisons use string name comparison (e.g., terrain.name == "WALL")
to avoid Enum identity bugs across module reloads.
"""
from __future__ import annotations

import heapq
from collections import deque
from typing import Any, Dict, List, Optional, Tuple

from warfront.data.models import GameMap, Terrain
from warfront.core.snapshot import snapshot, diff_snapshot, DiffSnapshot


# ---------------------------------------------------------------------------
# 1. BFS — Withdrawal Operation (Shortest Path Escape)
# ---------------------------------------------------------------------------

def bfs_sim(
    gmap: GameMap,
    start: Tuple[int, int],
    goal: Tuple[int, int],
) -> List[Tuple[Any, str, str]]:
    """BFS shortest-path search on *gmap* from *start* to *goal*.

    Returns steps as (DiffSnapshot, description, extra_info).
    """
    queue: deque = deque([(start, [start])])
    visited = {start}
    steps: List[Tuple[Any, str, str]] = []

    # Capture baseline before any mutations
    baseline = snapshot(gmap)

    steps.append((
        snapshot(gmap),
        "BFS Started — Insert start position into queue",
        f"Queue: {[start]}",
    ))

    while queue:
        (r, c), path = queue.popleft()
        gmap.grid[r][c].visited = True

        if (r, c) == goal:
            for pr, pc in path:
                gmap.grid[pr][pc].in_path = True
            steps.append((
                snapshot(gmap),
                f"Escape Path Found! Length: {len(path) - 1}",
                f"Path: {path}",
            ))
            return steps

        for nr, nc in gmap.get_neighbors(r, c):
            # String comparison to avoid Enum identity bug
            if (nr, nc) not in visited and gmap.grid[nr][nc].terrain.name != "WALL":
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))

        desc = f"({r},{c}) Exploring — Adding neighbors to queue"
        extra = f"Queue Size: {len(queue)} | Visited: {len(visited)} cells"
        steps.append((snapshot(gmap), desc, extra))

    steps.append((snapshot(gmap), "No Escape Path", "All routes blocked"))
    return steps


# ---------------------------------------------------------------------------
# 2. DFS — Infiltration Operation (Stealth Path, Backtracking)
# ---------------------------------------------------------------------------

def dfs_sim(
    gmap: GameMap,
    start: Tuple[int, int],
    goal: Tuple[int, int],
) -> List[Tuple[Any, str, str]]:
    """DFS path search on *gmap* from *start* to *goal*.

    Returns steps as (DiffSnapshot, description, extra_info).
    """
    stack = [(start, [start])]
    visited = {start}
    steps: List[Tuple[Any, str, str]] = []

    baseline = snapshot(gmap)

    while stack:
        (r, c), path = stack.pop()
        gmap.grid[r][c].visited = True

        if (r, c) == goal:
            for pr, pc in path:
                gmap.grid[pr][pc].in_path = True
            steps.append((
                snapshot(gmap),
                f"Infiltration Path Found! Depth: {len(path) - 1}",
                f"Path: {path}",
            ))
            return steps

        found_next = False
        for nr, nc in gmap.get_neighbors(r, c):
            if (nr, nc) not in visited and gmap.grid[nr][nc].terrain.name != "WALL":
                visited.add((nr, nc))
                stack.append(((nr, nc), path + [(nr, nc)]))
                found_next = True

        if found_next:
            steps.append((
                snapshot(gmap),
                f"({r},{c}) Entering — Depth {len(path)}",
                f"Stack Depth: {len(path)} Visited: {len(visited)}",
            ))
        else:
            steps.append((
                snapshot(gmap),
                f"({r},{c}) Backtracking — Blocked path",
                f"Stack Depth: {len(path)}",
            ))

    return steps


# ---------------------------------------------------------------------------
# 3. Dijkstra — UAV Reconnaissance Optimal Route
# ---------------------------------------------------------------------------

def dijkstra_sim(
    gmap: GameMap,
    start: Tuple[int, int],
    goal: Tuple[int, int],
) -> List[Tuple[Any, str, str]]:
    """Dijkstra weighted shortest-path on *gmap* from *start* to *goal*.

    Returns steps as (DiffSnapshot, description, extra_info).
    """
    heap = [(0, start, [start])]
    visited: Dict[Tuple[int, int], float] = {}
    steps: List[Tuple[Any, str, str]] = []

    baseline = snapshot(gmap)

    steps.append((
        snapshot(gmap),
        "Dijkstra Started — Start point distance=0",
        f"Heap: {[(0, start)]}",
    ))

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
            steps.append((
                snapshot(gmap),
                f"Optimal Path Found! Total Cost: {cost}",
                f"Path Length: {len(path)}",
            ))
            return steps

        for nr, nc in gmap.get_neighbors(r, c):
            new_cost = cost + gmap.grid[nr][nc].terrain.value[1]
            if (nr, nc) not in visited or visited[(nr, nc)] > new_cost:
                heapq.heappush(heap, (new_cost, (nr, nc), path + [(nr, nc)]))

        visited_count = sum(
            1 for row in gmap.grid for cell in row if cell.visited
        )
        steps.append((
            snapshot(gmap),
            f"({r},{c}) Processing — Current Cost {cost}",
            f"Heap Size: {len(heap)} | Nodes Processed: {visited_count}",
        ))

    steps.append((snapshot(gmap), "No Reachable Path", "All routes are blocked."))
    return steps


# ---------------------------------------------------------------------------
# 4. MST (Kruskal) — Minimum Supply Route Design
# ---------------------------------------------------------------------------

def kruskal_sim(
    nodes: List[Tuple[int, int]],
    edges: List[Tuple[int, int, int]],
) -> List[Tuple[Any, str, str]]:
    """Kruskal MST algorithm.

    Args:
        nodes: List of node identifiers (e.g., integer tuples).
        edges: List of (cost, u, v) tuples representing undirected edges.

    Returns steps as (selected_edges_list, description, extra_info).
    """
    parent: Dict = {n: n for n in nodes}

    def find(n):
        if parent[n] == n:
            return n
        parent[n] = find(parent[n])
        return parent[n]

    def union(n1, n2) -> bool:
        root1, root2 = find(n1), find(n2)
        if root1 != root2:
            parent[root1] = root2
            return True
        return False

    edges_sorted = sorted(edges, key=lambda x: x[0])
    selected: List[Tuple] = []
    steps: List[Tuple[Any, str, str]] = []

    for cost, u, v in edges_sorted:
        if union(u, v):
            selected.append((u, v, cost))
            steps.append((
                list(selected),
                f"Edge {u}↔{v} Added — Cost {cost}",
                f"MST Edges: {len(selected)}/{len(nodes) - 1}",
            ))
        else:
            steps.append((
                list(selected),
                f"Edge {u}↔{v} Skipped — Cycle Formed",
                f"Current MST Cost: {sum(e[2] for e in selected)}",
            ))

    total = sum(e[2] for e in selected)
    steps.append((
        list(selected),
        f"MST Complete! Total Supply Cost: {total}",
        f"Connected Bases: {len(nodes)}",
    ))
    return steps


# ---------------------------------------------------------------------------
# 5. Topological Sort — Operation Planning Order
# ---------------------------------------------------------------------------

def topological_sort_sim(
    tasks: List[str],
    deps: List[Tuple[str, str]],
) -> List[Tuple[Any, str, str]]:
    """Kahn's algorithm topological sort.

    Args:
        tasks: List of task name strings.
        deps:  List of (prerequisite, dependent) string pairs.

    Returns steps as ((order_list, queue_list), description, extra_info).
    """
    adj: Dict[str, List[str]] = {t: [] for t in tasks}
    indegree: Dict[str, int] = {t: 0 for t in tasks}
    for u, v in deps:
        adj[u].append(v)
        indegree[v] += 1

    queue: deque = deque([t for t in tasks if indegree[t] == 0])
    order: List[str] = []
    steps: List[Tuple[Any, str, str]] = []

    steps.append((
        (list(order), list(queue)),
        "Start — Inserting tasks with no dependencies into queue",
        f"Ready tasks: {list(queue)}",
    ))

    while queue:
        task = queue.popleft()
        order.append(task)
        steps.append((
            (list(order), list(queue)),
            f"'{task}' Execution Complete",
            f"Completed: {len(order)}/{len(tasks)}",
        ))

        for nxt in adj[task]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
                steps.append((
                    (list(order), list(queue)),
                    f"'{nxt}' Dependencies Satisfied — Added to Queue",
                    f"Queue: {list(queue)}",
                ))

    if len(order) == len(tasks):
        steps.append((
            (list(order), []),
            f"Full Operation Plan Complete: {' -> '.join(order)}",
            f"Total tasks: {len(order)}",
        ))
    else:
        steps.append((
            (list(order), []),
            "Cyclic Dependency Detected — Planning Impossible",
            f"Completed: {len(order)}/{len(tasks)}",
        ))
    return steps


# ---------------------------------------------------------------------------
# 6. DP (0-1 Knapsack) — Logistics Optimization
# ---------------------------------------------------------------------------

def knapsack_sim(
    items: List[Tuple[str, int, int]],
    capacity: int,
) -> List[Tuple[Any, str, str]]:
    """0-1 Knapsack DP simulation.

    Args:
        items:    List of (name, weight, value) tuples.
        capacity: Maximum knapsack capacity.

    Returns steps as (dp_table, description, extra_info).
    """
    n = len(items)
    dp: List[List[int]] = [[0] * (capacity + 1) for _ in range(n + 1)]
    steps: List[Tuple[Any, str, str]] = []

    for i in range(1, n + 1):
        name, w, v = items[i - 1]
        for j in range(capacity + 1):
            if w <= j:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - w] + v)
            else:
                dp[i][j] = dp[i - 1][j]

        steps.append((
            [row[:] for row in dp],  # shallow copy of rows
            f"Processing Item '{name}' (Weight:{w}, Value:{v})",
            f"Current Max Value: {dp[i][capacity]}",
        ))

    # Backtracking to find selected items
    selected: List[str] = []
    curr_w = capacity
    for i in range(n, 0, -1):
        if dp[i][curr_w] != dp[i - 1][curr_w]:
            name, w, v = items[i - 1]
            selected.append(name)
            curr_w -= w

    steps.append((
        [row[:] for row in dp],
        f"Optimal Loading: {selected}",
        f"Total Value: {dp[n][capacity]} | Capacity: {capacity}",
    ))
    return steps


# ---------------------------------------------------------------------------
# 7. Union-Find — Frontline Reorganization
# ---------------------------------------------------------------------------

def union_find_sim(
    units: List[str],
    ops: List[Tuple[str, str, str]],
) -> List[Tuple[Any, str, str]]:
    """Union-Find (disjoint set union) simulation.

    Args:
        units: List of unit name strings.
        ops:   List of ("union", a, b) operation tuples.

    Returns steps as (parent_dict_snapshot, description, extra_info).
    """
    parent: Dict[str, str] = {u: u for u in units}

    def find(u: str) -> str:
        if parent[u] == u:
            return u
        parent[u] = find(parent[u])
        return parent[u]

    def groups() -> Dict[str, List[str]]:
        g: Dict[str, List[str]] = {}
        for u in units:
            root = find(u)
            g.setdefault(root, []).append(u)
        return g

    steps: List[Tuple[Any, str, str]] = []
    steps.append((
        {u: find(u) for u in units},
        f"Initial State — {len(units)} Independent Units",
        f"Groups: {len(groups())}",
    ))

    for op, a, b in ops:
        if op == "union":
            root_a, root_b = find(a), find(b)
            if root_a != root_b:
                parent[root_a] = root_b
                g = groups()
                steps.append((
                    {u: find(u) for u in units},
                    f"'{a}' U '{b}' Merged — Unified into {len(g)} frontlines",
                    f"Groups: {list(g.keys())}",
                ))
            else:
                steps.append((
                    {u: find(u) for u in units},
                    f"'{a}', '{b}' already on same frontline — Skipping",
                    f"Groups: {len(groups())}",
                ))

    steps.append((
        {u: find(u) for u in units},
        f"Finalized Reorganization into {len(groups())} frontlines",
        f"Final groups: {list(groups().keys())}",
    ))
    return steps


# ---------------------------------------------------------------------------
# 8. Greedy — Artillery Priority
# ---------------------------------------------------------------------------

def artillery_greedy_sim(
    targets: List[Tuple[str, int, int]],
    ammo: int,
) -> List[Tuple[Any, str, str]]:
    """Fractional-knapsack-style greedy for artillery target selection.

    Args:
        targets: List of (name, threat_value, ammo_cost) tuples.
        ammo:    Total available ammo.

    Returns steps as ((selected_list, sorted_targets), description, extra_info).
    """
    sorted_t = sorted(targets, key=lambda x: x[1] / x[2], reverse=True)
    selected: List[str] = []
    remaining = ammo
    total_threat = 0
    steps: List[Tuple[Any, str, str]] = []

    steps.append((
        ([], sorted_t),
        "Sorting complete based on Threat/Ammo ratio",
        f"Current Ammo: {ammo}",
    ))

    for name, threat, cost in sorted_t:
        if cost <= remaining:
            remaining -= cost
            total_threat += threat
            selected.append(name)
            steps.append((
                (list(selected), sorted_t),
                f"Selecting '{name}' for Artillery (Threat:{threat}, Cost:{cost})",
                f"Remaining Ammo: {remaining}",
            ))
        else:
            steps.append((
                (list(selected), sorted_t),
                f"Skipping '{name}' — Insufficient Ammo (Required:{cost}, Remaining:{remaining})",
                f"Selected so far: {selected}",
            ))

    steps.append((
        (list(selected), []),
        f"Neutralization Complete | Total Threat Removed: {total_threat}",
        f"Ammo Used: {ammo - remaining}",
    ))
    return steps


# ---------------------------------------------------------------------------
# 9. Binary Search — Building DB / Radar Detection
# ---------------------------------------------------------------------------

def binary_search_sim(
    arr: List[int],
    target: int,
) -> List[Tuple[Any, str, str]]:
    """Binary search simulation.

    Args:
        arr:    Sorted integer array.
        target: Value to search for.

    Returns steps as ((lo, hi, mid), description, extra_info).
    """
    lo, hi = 0, len(arr) - 1
    steps: List[Tuple[Any, str, str]] = []

    steps.append((
        (lo, hi, -1),
        f"Search Started | Range: [{lo}, {hi}] | Target: {target}",
        f"Array length: {len(arr)}",
    ))

    while lo <= hi:
        mid = (lo + hi) // 2
        steps.append((
            (lo, hi, mid),
            f"Checking median arr[{mid}]={arr[mid]}",
            f"Target: {target}",
        ))

        if arr[mid] == target:
            steps.append((
                (mid, mid, mid),
                f"Target {target} Found! Index: {mid}",
                f"arr[{mid}] = {arr[mid]}",
            ))
            return steps
        elif arr[mid] < target:
            lo = mid + 1
            steps.append((
                (lo, hi, mid),
                f"Searching Right | New Range: [{lo}, {hi}]",
                f"arr[{mid}]={arr[mid]} < target={target}",
            ))
        else:
            hi = mid - 1
            steps.append((
                (lo, hi, mid),
                f"Searching Left | New Range: [{lo}, {hi}]",
                f"arr[{mid}]={arr[mid]} > target={target}",
            ))

    steps.append((
        (lo, hi, -1),
        f"Target {target} Not Found",
        f"Search exhausted all possibilities",
    ))
    return steps


# ---------------------------------------------------------------------------
# 10. Bitmasking — Security Communication Permissions
# ---------------------------------------------------------------------------

def bitmask_sim(
    permissions: List[str],
    ops: List[Tuple[str, str, str]],
) -> List[Tuple[Any, str, str]]:
    """Bitmask permission management simulation.

    Args:
        permissions: List of permission name strings (defines bit positions).
        ops:         List of (unit_name, action, permission_name) tuples.
                     action is one of: "grant", "revoke", "check".

    Returns steps as ((unit_masks_dict, current_op_or_None), description, extra_info).
    """
    perm_to_bit: Dict[str, int] = {p: 1 << i for i, p in enumerate(permissions)}
    unit_masks: Dict[str, int] = {op[0]: 0 for op in ops}
    steps: List[Tuple[Any, str, str]] = []

    steps.append((
        (dict(unit_masks), None),
        "Security System Initialized — All units have no permissions",
        f"Permissions defined: {permissions}",
    ))

    for unit, action, perm in ops:
        bit = perm_to_bit.get(perm, 0)
        if action == "grant":
            unit_masks[unit] |= bit
            steps.append((
                (dict(unit_masks), (unit, perm)),
                f"'{unit}' <- '{perm}' Permission Granted | Mask: {bin(unit_masks[unit])}",
                f"Active permissions: {[p for p, b in perm_to_bit.items() if unit_masks[unit] & b]}",
            ))
        elif action == "revoke":
            unit_masks[unit] &= ~bit
            steps.append((
                (dict(unit_masks), (unit, perm)),
                f"'{unit}' -> '{perm}' Permission Revoked | Mask: {bin(unit_masks[unit])}",
                f"Active permissions: {[p for p, b in perm_to_bit.items() if unit_masks[unit] & b]}",
            ))
        elif action == "check":
            has = bool(unit_masks[unit] & bit)
            steps.append((
                (dict(unit_masks), (unit, perm)),
                f"'{unit}' '{perm}' Permission Check: {'Authorized' if has else 'Denied'}",
                f"Mask value: {bin(unit_masks[unit])}",
            ))

    steps.append((
        (dict(unit_masks), None),
        "Permission Processing Complete",
        f"Units processed: {list(unit_masks.keys())}",
    ))
    return steps
