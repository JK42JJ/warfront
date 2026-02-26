# MISSION: 00-04 | Python Basics | trainee
# TITLE: Unit Organization — List Manipulation
# DESC: Sort, filter, and slice the troop list to organize elite units
# ALGO: List
# MODULE: mission_00_trainee

def solve(data):
    """
    data = {
      'soldiers': [45, 72, 31, 88, 56, 93, 20, 67],  # Combat Power Score
      'cutoff':   60   # Elite based on Score
    }
    Return: {
      'sorted_asc':  Ascending Sort List,
      'elite':       cutoff  and Soldier  Filtering,
      'top3':        Sort   Top 3persons,
      'average':     Average ( Count  2   )
    }
    """
    soldiers = data['soldiers']
    cutoff   = data['cutoff']

    # TODO 1: sorted() with Ascending
    sorted_asc = []

    # TODO 2: List Comprehension with cutoff  and Filtering
    elite = []

    # TODO 3: Descending Sort     3items  
    top3 = []

    # TODO 4: sum / len  with Average, round(, 2)
    average = 0.0

    return {'sorted_asc': sorted_asc, 'elite': elite,
            'top3': top3, 'average': average}

# --- Execution Block ---
