# MISSION: 00-05 | Python Basics | trainee
# TITLE: Intelligence Gathering — Dictionary
# DESC: Analyze enemy base info using a dictionary and write a tactical report
# ALGO: Dictionary
# MODULE: mission_00_trainee

def solve(data):
    """
    data = {
      'bases': {
        'ALPHA': {'troops': 120, 'weapons': 30, 'active': True},
        'BETA':  {'troops': 80,  'weapons': 15, 'active': False},
        'GAMMA': {'troops': 200, 'weapons': 50, 'active': True},
      }
    }
    Return: {
      'active_bases': active=True in Base Name List,
      'total_troops': Total Troops Total,
      'strongest':    Troops   Base Name,
      'summary':      {Basepersons: troops} Formatof   Dictionary
    }
    """
    bases = data['bases']

    # TODO 1: active=True in Base  Filter
    active_bases = []

    # TODO 2: All Base troops Sum
    total_troops = 0

    # TODO 3: troops      Basepersons (max() + key Argument using)
    strongest = ""

    # TODO 4: Dictionary Comprehension with {Name: troops} Create
    summary = {}

    return {'active_bases': active_bases, 'total_troops': total_troops,
            'strongest': strongest, 'summary': summary}

# --- Execution Block ---
