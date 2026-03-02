def get_test_data():
    """MST Data — grid-coordinate nodes form a 6×6 diamond layout."""
    nodes = [(0, 0), (0, 5), (5, 0), (5, 5)]
    adj = {
        (0, 0): [(10, (0, 5)), (20, (5, 0))],
        (0, 5): [(10, (0, 0)), (15, (5, 5))],
        (5, 0): [(20, (0, 0)), (30, (5, 5))],
        (5, 5): [(15, (0, 5)), (30, (5, 0))],
    }
    edges = [
        (10, (0, 0), (0, 5)),
        (20, (0, 0), (5, 0)),
        (15, (0, 5), (5, 5)),
        (30, (5, 0), (5, 5)),
    ]
    return {"nodes": nodes, "adj": adj, "edges": edges}


def build_map():
    from map import GameMap
    return GameMap(12, 12), (0, 0), (11, 11)


def visualize_result(gmap, result):
    """Animate the MST being built edge by edge on the grid map.

    Nodes are grid coordinates (r, c). Each MST edge is drawn as a
    straight line (horizontal, vertical, or L-shaped) on the map.
    Cells are marked in_path=True one by one for a live animation.
    """
    from core import snapshot

    if not result:
        return None

    mst   = result.get("mst", []) if isinstance(result, dict) else []
    total = result.get("total", 0) if isinstance(result, dict) else 0

    if not mst:
        return None

    gmap.reset_simulation_state()
    steps = []

    def _edge_cells(u, v):
        """Return ordered list of grid cells along the edge u→v."""
        r1, c1 = tuple(u)
        r2, c2 = tuple(v)
        cells = []
        if r1 == r2:
            # Horizontal
            step = 1 if c2 >= c1 else -1
            for c in range(c1, c2 + step, step):
                cells.append((r1, c))
        elif c1 == c2:
            # Vertical
            step = 1 if r2 >= r1 else -1
            for r in range(r1, r2 + step, step):
                cells.append((r, c1))
        else:
            # L-shaped: travel along row first, then column
            step_c = 1 if c2 >= c1 else -1
            for c in range(c1, c2 + step_c, step_c):
                cells.append((r1, c))
            step_r = 1 if r2 >= r1 else -1
            for r in range(r1 + step_r, r2 + step_r, step_r):
                cells.append((r, c2))
        return cells

    running_total = 0
    for i, edge in enumerate(mst):
        u, v, cost = edge
        running_total += cost
        cells = _edge_cells(u, v)

        # Animate cell-by-cell along this edge
        for r, c in cells:
            if 0 <= r < gmap.rows and 0 <= c < gmap.cols:
                gmap.grid[r][c].in_path = True
            steps.append((
                snapshot(gmap),
                f"Edge {i + 1}/{len(mst)}: {tuple(u)} → {tuple(v)}  weight={cost}",
                f"MST total so far: {running_total}",
            ))

    # Final confirmation frame
    steps.append((
        snapshot(gmap),
        "✔  Maximum Spanning Tree complete",
        f"Total weight: {total}",
    ))

    return steps or None
