# display.py — owns all terminal output for the advanced version.
# Nothing outside this file should call print() or read stdin directly.
# Keeping all UI here means the logic layer (higher_lower.py) stays testable
# and the presentation can be restyled without touching game code.

from __future__ import annotations

import os
import sys
import time
import tty
import termios

from config import TYPEWRITER_DELAY, DIVIDER_WIDTH

# ANSI cyan wraps the logo so it renders in blue on launch.
# The codes are inlined directly since LOGO is defined before the Colors class below.
LOGO = (
    "\033[96m"  # cyan start
    """
    __  ___       __
   / / / (_)___ _/ /_  ___  _____
  / /_/ / / __ `/ __ \/ _ \/ ___/
 / __  / / /_/ / / / /  __/ /
/_/ ///_/\__, /_/ /_/\___/_/
   / /  /____/_      _____  _____
  / /   / __ \ | /| / / _ \/ ___/
 / /___/ /_/ / |/ |/ /  __/ /
/_____/\____/|__/|__/\___/_/
"""
    "\033[0m"   # reset
)

# VS separator shown between account A and account B during gameplay.
VS = """
 _    __
| |  / /____
| | / / ___/
| |/ (__  )
|___/____(_)
"""


# Color convention used throughout the UI:
#   CYAN   — headers and labels (e.g. "A:", section titles)
#   GREEN  — correct answer / positive feedback
#   RED    — wrong answer / errors
#   YELLOW — key values the player should notice (score, key hints)
#   DIM    — secondary text, instructions, hints (lower visual weight)
#   BOLD   — emphasis, paired with a color (e.g. CYAN + BOLD for titles)
class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    DIM = "\033[2m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def clear() -> None:
    # os.system is the standard cross-platform way to clear the terminal.
    # "cls" on Windows, "clear" on macOS/Linux.
    os.system("cls" if os.name == "nt" else "clear")


def typewriter(text: str, delay: float = TYPEWRITER_DELAY) -> None:
    # Writes one character at a time with a small delay to create an animation effect.
    # sys.stdout.write + flush is used instead of print() so there's no automatic
    # newline and the output appears immediately without buffering.
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)


def divider() -> None:
    # Prints a horizontal rule to visually separate sections on screen.
    # DIM keeps it subtle so it doesn't compete with the content around it.
    print(f"{Colors.DIM}{'─' * DIVIDER_WIDTH}{Colors.RESET}")


def print_result(is_win: bool, score: int) -> None:
    # Single function for all win/loss feedback so colors are applied consistently.
    if is_win:
        print(f"{Colors.GREEN}Correct!{Colors.RESET}  {Colors.YELLOW}Score: {score}{Colors.RESET}")
    else:
        print(f"{Colors.RED}Wrong!{Colors.RESET}  {Colors.YELLOW}Final score: {score}{Colors.RESET}")


def print_error(message: str) -> None:
    # All validation errors go through here — red text, never a raw print().
    print(f"{Colors.RED}{message}{Colors.RESET}")


def print_accounts(label_a: str, label_b: str) -> None:
    # Displays the two accounts side by side with the VS separator between them.
    # Labels are pre-formatted strings from format_account() in higher_lower.py.
    print(f"{Colors.CYAN}A:{Colors.RESET} {label_a}")
    print(VS)
    print(f"{Colors.CYAN}B:{Colors.RESET} {label_b}")


def get_keypress() -> str:
    """Read a single keypress without waiting for Enter.

    Returns 'enter', 'up', or the raw character.

    How it works:
      - termios saves the terminal's current settings (echo, line buffering, etc.)
      - tty.setraw() switches the terminal into raw mode, where every keypress is
        sent directly to the program without waiting for Enter and without echoing
        the character back to the screen.
      - Escape sequences: arrow keys send a 3-byte sequence: ESC + '[' + letter.
        Up arrow is ESC [ A, so we read 3 bytes to detect it.
      - The finally block always restores the original settings, even if an
        exception occurs, so the terminal isn't left in raw mode on crash.
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)  # save current terminal state
    try:
        tty.setraw(fd)  # enter raw mode — no echo, no line buffering
        ch = sys.stdin.read(1)

        # Enter key sends carriage return (\r) or newline (\n)
        if ch in ("\r", "\n"):
            return "enter"

        # Escape sequences start with \x1b (ESC).
        # Arrow keys are: ESC [ A/B/C/D (up/down/right/left).
        if ch == "\x1b":
            ch2 = sys.stdin.read(1)
            ch3 = sys.stdin.read(1)
            if ch2 == "[" and ch3 == "A":
                return "up"
            return "esc"

        return ch
    finally:
        # Restore terminal settings no matter what happens
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
