# MISSION: 00-03 | Python Basics | trainee
# TITLE: Cipher Decryption — String Processing
# DESC: Analyze enemy cipher communications and extract key information
# ALGO: String
# MODULE: mission_00_trainee

def solve(data):
    """
    data = {
      'message': "WARFRONT:ALPHA:SECTOR-7:CONFIRMED",
      'keyword': "ALPHA"
    }
    Return: {
      'parts':    ':' with split   List,
      'has_kw':   keyword Include   (bool),
      'reversed': message   Reversed String,
      'count':    'A'  how many times it appears
    }
    """
    message = data['message']
    keyword = data['keyword']

    # TODO 1: split(':')  with Separation
    parts = []

    # TODO 2: keyword in message
    has_kw = False

    # TODO 3: String   ( )
    reversed_msg = ""

    # TODO 4: 'A' Appearance  Count
    count = 0

    return {'parts': parts, 'has_kw': has_kw,
            'reversed': reversed_msg, 'count': count}

# --- Execution Block ---
