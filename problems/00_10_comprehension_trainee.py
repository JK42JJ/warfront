# MISSION: 00-10 | Python Basics | trainee
# TITLE: Special Forces Selection — Comprehension & Lambda
# DESC: Select and classify candidates using comprehensions and lambda
# ALGO: Comprehension & Lambda
# MODULE: mission_00_trainee
# TIME_COMPLEXITY: O(n log n)
# SPACE_COMPLEXITY: O(n)
# DIFFICULTY: 1
"""
┌─ COMPREHENSION & LAMBDA ────────────────────────────────────────────────────┐
│  1. [expr for x in lst if cond] — list comprehension with filter            │
│  2. {k: v for k, v in ...} — dict comprehension                            │
│  3. sorted(lst, key=lambda x: x['field'], reverse=True) — lambda sort      │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['candidates'] : list[dict] — [{'name':str,'score':int,'type':str}, ...]
# data['pass_score'] : int        — minimum passing score
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Select and classify special-forces candidates."""
    candidates = data['candidates']
    pass_score = data['pass_score']

    # TODO 1: passed = names of candidates with score >= pass_score
    #         Hint: [c['name'] for c in candidates if ...]
    passed = []

    # TODO 2: score_map = {name: score} for all candidates  ← dict comprehension
    score_map = {}

    # TODO 3: by_type = group names by type
    #         e.g. {'infantry': ['A','C'], 'support': [...], ...}
    #         Hint: build empty dict, then loop and .setdefault(type, []).append(name)
    by_type = {}

    # TODO 4: top2 = names of top 2 candidates by score (descending)
    #         Hint: sorted(..., key=lambda c: c['score'], reverse=True)[:2]
    top2 = []

    return {'passed': passed, 'score_map': score_map,
            'by_type': by_type, 'top2': top2}


# ─────────────────────────────────────────────────────────────────────────────
# Expected output:
#   {'passed': ['A','C','D','F'], 'score_map': {'A':88,'B':55,...},
#    'by_type': {'infantry':['A','C'],'support':['B','E'],'recon':['D','F']},
#    'top2': ['F','C']}
# ─────────────────────────────────────────────────────────────────────────────
