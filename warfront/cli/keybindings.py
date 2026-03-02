"""warfront/cli/keybindings.py — Key constants and non-blocking key reader."""
from __future__ import annotations

import select
import sys
import termios
import tty

# ── Navigation ────────────────────────────────────────────────────────────────
KEY_UP     = "\x1b[A"
KEY_DOWN   = "\x1b[B"
KEY_LEFT   = "\x1b[D"
KEY_RIGHT  = "\x1b[C"
KEY_UP2    = "\x1bOA"   # alternative up (application cursor key mode)
KEY_DOWN2  = "\x1bOB"   # alternative down
KEY_LEFT2  = "\x1bOD"
KEY_RIGHT2 = "\x1bOC"

# ── Actions ───────────────────────────────────────────────────────────────────
KEY_ENTER = "\r"
KEY_QUIT  = "q"
KEY_SLASH = "/"
KEY_SPACE = " "

# Vim-style navigation
KEY_VIM_UP    = "k"
KEY_VIM_DOWN  = "j"
KEY_VIM_LEFT  = "h"
KEY_VIM_RIGHT = "l"

KEY_NEXT  = "n"
KEY_RETRY = "r"
KEY_ESC   = "\x1b"


def get_key() -> str:
    """Blocking key read using tty/termios/select compatible with terminal raw mode.

    Reads one logical key sequence (including multi-byte escape sequences such
    as arrow keys) and returns it as a string.  Restores terminal settings even
    if an exception occurs.

    Returns an empty string on read failure.
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)

        # Block until at least one byte is available (no CPU spin)
        rlist, _, _ = select.select([sys.stdin], [], [], None)
        if not rlist:
            return ""

        key = sys.stdin.read(1)

        # If the first byte is ESC, read the remainder of the sequence
        if key == "\x1b":
            rlist, _, _ = select.select([sys.stdin], [], [], 0.05)
            if rlist:
                key += sys.stdin.read(2)  # reads '[A', 'OB', etc.

        return key
    except Exception:
        return ""
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
