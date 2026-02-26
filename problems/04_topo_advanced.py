# MISSION: 04 | Topological Sort | general
# TITLE: Operation Plan — DFS Based Topological Sort
# DESC: Implement topological sort using DFS post-order traversal
# ALGO: Topological Sort
# MODULE: mission_04_topo
def solve(data):
    graph  = data['graph']
    nodes  = list(data['indegree'].keys())
    visited, result = set(), []

    def dfs(node):
        visited.add(node)
        for nxt in graph.get(node, []):
            if nxt not in visited:
                dfs(nxt)
        # TODO: result to node Add ( UpTraverse)

    for n in nodes:
        if n not in visited:
            dfs(n)
    return result[::-1]  #   Topological Sort Order

# --- Execution Block ---
