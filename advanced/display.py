from __future__ import annotations

import os
import sys
import time
import tty
import termios

from config import TYPEWRITER_DELAY, DIVIDER_WIDTH

LOGO = """
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

VS = """
 _    __
| |  / /____
| | / / ___/
| |/ (__  )
|___/____(_)
"""


class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    DIM = "\033[2m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def typewriter(text: str, delay: float = TYPEWRITER_DELAY) -> None:
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)


def divider() -> None:
    print(f"{Colors.DIM}{'─' * DIVIDER_WIDTH}{Colors.RESET}")


def print_result(is_win: bool, score: int) -> None:
    if is_win:
        print(f"{Colors.GREEN}Correct!{Colors.RESET}  {Colors.YELLOW}Score: {score}{Colors.RESET}")
    else:
        print(f"{Colors.RED}Wrong!{Colors.RESET}  {Colors.YELLOW}Final score: {score}{Colors.RESET}")


def print_error(message: str) -> None:
    print(f"{Colors.RED}{message}{Colors.RESET}")


def print_accounts(label_a: str, label_b: str) -> None:
    print(f"{Colors.CYAN}A:{Colors.RESET} {label_a}")
    print(VS)
    print(f"{Colors.CYAN}B:{Colors.RESET} {label_b}")


def get_keypress() -> str:
    """Read a single keypress without waiting for Enter.

    Returns 'enter', 'up', or the raw character.
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch in ("\r", "\n"):
            return "enter"
        if ch == "\x1b":
            ch2 = sys.stdin.read(1)
            ch3 = sys.stdin.read(1)
            if ch2 == "[" and ch3 == "A":
                return "up"
            return "esc"
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
