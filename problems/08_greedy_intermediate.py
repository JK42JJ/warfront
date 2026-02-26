# MISSION: 08 | Greedy | officer
# TITLE: Artillery Priority Up —  of  Assignment
# DESC: Maximize goals neutralized with minimum artillery resources
# ALGO: Greedy
# MODULE: mission_08_greedy
import heapq

def solve(data):
    targets = sorted(data['targets'], key=lambda x: x[0])  # StartTime Sort
    weapons = data['weapon_count']
    heap    = []  # Use  in Weaponof EndTime
    max_concurrent = 0

    for start, end, _ in targets:
        # End  Weapon  Count
        while heap and heap[0] <= start:
            heapq.heappop(heap)
        heapq.heappush(heap, end)
        # TODO: max_concurrent Update
        max_concurrent = max(max_concurrent, len(heap))

    return {'weapons_needed': max_concurrent,
            'sufficient': max_concurrent <= weapons}

# --- Execution Block ---
