def get_test_data():
    """Topological Sort Mission Data - Restored Schema"""
    tasks = ["Intelligence", "AirSupport", "Minesweeping", "BridgeSecure", "TroopAdvance"]
    deps = [
        ("Intelligence", "AirSupport"), 
        ("Intelligence", "Minesweeping"), 
        ("Minesweeping", "BridgeSecure"), 
        ("BridgeSecure", "TroopAdvance")
    ]
    
    # Construct graph and indegree to match problem files
    graph = {t: [] for t in tasks}
    indegree = {t: 0 for t in tasks}
    for u, v in deps:
        graph[u].append(v)
        indegree[v] += 1
        
    return {
        "graph": graph,
        "indegree": indegree,
        "tasks": tasks, # Keep for backup
        "deps": deps
    }

def build_map():
    from map import GameMap
    return GameMap(12, 12), (0, 0), (11, 11)

def visualize_result(gmap, result):
    from core import snapshot
    # result might be a dict or a list depending on mission level
    order = result.get('order', []) if isinstance(result, dict) else result
    return [(snapshot(gmap), "✔ Operation sequence established", f"Order: {order}")]
