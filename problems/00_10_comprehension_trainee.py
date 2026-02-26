# MISSION: 00-10 | Python Basics | trainee
# TITLE: Special Forces Selection — Comprehension & Lambda
# DESC: Select and classify unit members using comprehensions and lambda
# ALGO: Comprehension & Lambda
# MODULE: mission_00_trainee

def solve(data):
    """
    data = {
      'candidates': [
        {'name':'A','score':88,'type':'infantry'},
        {'name':'B','score':55,'type':'support'},
        {'name':'C','score':92,'type':'infantry'},
        {'name':'D','score':73,'type':'recon'},
        {'name':'E','score':61,'type':'support'},
        {'name':'F','score':95,'type':'recon'},
      ],
      'pass_score': 70
    }
    Return: {
      'passed':     score >= pass_score in Name List (Comprehension),
      'score_map':  {Name: score} Dictionary Comprehension,
      'by_type':    {'infantry':[...], 'support':[...], ...} Grouping,
      'top2':       score based on Top 2persons Name (lambda Sort using)
    }
    """
    candidates = data['candidates']
    pass_score = data['pass_score']

    # TODO 1: List Comprehension
    passed = []

    # TODO 2: Dictionary Comprehension
    score_map = {}

    # TODO 3: type by Grouping (dict + List Comprehension)
    by_type = {}

    # TODO 4: sorted(..., key=lambda x: ..., reverse=True)[:2]
    top2 = []

    return {'passed': passed, 'score_map': score_map,
            'by_type': by_type, 'top2': top2}

# --- Execution Block ---
