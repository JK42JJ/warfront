# MISSION: 00-01 | Python Basics | trainee
# TITLE: Bootcamp Entry — Variables and Types
# DESC: Handle int, float, str, bool and decrypt the cipher message
# ALGO: Variables & Types
# MODULE: mission_00_trainee

def solve(data):
    """
    data = {
      'code_int':   Cipher Integer (e.g., 42),
      'code_float': Cipher Float (e.g., 3.14),
      'code_str':   Cipher String (e.g., "ALPHA"),
    }
    Return: {
      'sum':    Sum of code_int + int(code_float),
      'msg':    First 3 characters of code_str converted to lowercase,
      'is_big': True if code_int is greater than 100
    }
    """
    code_int   = data['code_int']
    code_float = data['code_float']
    code_str   = data['code_str']

    # TODO 1: Convert total = code_int + code_float to an Integer
    total = 0

    # TODO 2: Convert first 3 characters of code_str to lowercase
    msg = ""

    # TODO 3: Set is_big to True if code_int is greater than 100
    is_big = False

    return {'sum': total, 'msg': msg, 'is_big': is_big}

# --- Execution Block ---
