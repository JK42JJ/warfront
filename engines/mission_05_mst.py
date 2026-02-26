def get_test_data():
    """MST Data - Restored Schema"""
    nodes = [(0,0), (0,5), (5,0), (5,5)]
    # Use dict for adj to support adj.get(v, [])
    adj = {
        (0,0): [(10, (0,5)), (20, (5,0))],
        (0,5): [(10, (0,0)), (15, (5,5))],
        (5,0): [(20, (0,0)), (30, (5,5))],
        (5,5): [(15, (0,5)), (30, (5,0))]
    }
    # Expected format for Kruskal problems: (cost, u, v)
    edges = [
        (10, (0,0), (0,5)), 
        (20, (0,0), (5,0)), 
        (15, (0,5), (5,5)), 
        (30, (5,0), (5,5))
    ]
    return {
        "nodes": nodes,
        "adj": adj,
        "edges": edges
    }

def build_map():
    from map import GameMap
    return GameMap(12, 12), (0, 0), (11, 11)

def visualize_result(gmap, result):
    from core import snapshot
    mst = result.get('mst', []) if isinstance(result, dict) else result
    return [(snapshot(gmap), "✔ MST construction complete", f"Result: {mst}")]
