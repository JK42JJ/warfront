# MISSION: 00-04 | Python Basics | trainee
# TITLE: Unit Organization — List Manipulation
# DESC: Sort, filter, and slice the troop list to organize elite units
# ALGO: List
# MODULE: mission_00_trainee
# TIME_COMPLEXITY: O(n log n)
# SPACE_COMPLEXITY: O(n)
# DIFFICULTY: 1
"""
┌─ LIST ──────────────────────────────────────────────────────────────────────┐
│  1. sorted(lst) → ascending copy;  sorted(lst, reverse=True) → descending  │
│  2. [x for x in lst if condition] → list comprehension with filter          │
│  3. lst[-3:] or sorted(lst)[:3] → slicing for top/bottom N                 │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['soldiers'] : list[int] — combat power scores e.g. [45, 72, 31, 88]
# data['cutoff']   : int       — elite threshold e.g. 60
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Organise troops by performance and select elite units."""
    soldiers = data['soldiers']
    cutoff   = data['cutoff']

    # TODO 1: sorted_asc = soldiers sorted in ascending order
    sorted_asc = []

    # TODO 2: elite = soldiers with score >= cutoff  ← list comprehension
    elite = []

    # TODO 3: top3 = top 3 soldiers by score (descending)
    top3 = []

    # TODO 4: average = mean score, rounded to 2 decimal places
    #         Hint: sum(soldiers) / len(soldiers)
    average = 0.0

    return {'sorted_asc': sorted_asc, 'elite': elite,
            'top3': top3, 'average': average}


# ─────────────────────────────────────────────────────────────────────────────
# Expected output:
#   {'sorted_asc': [20,31,45,56,67,72,88,93],
#    'elite': [72,88,93,67], 'top3': [93,88,72], 'average': 59.0}
# ─────────────────────────────────────────────────────────────────────────────
