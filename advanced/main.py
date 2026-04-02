# main.py — entry point and orchestrator for the advanced version.
# Its only job is to wire together the three layers:
#   display.py  → all terminal output and input
#   higher_lower.py → all game logic
#   config.py   → all constants
# main.py itself contains no raw print() calls and no game logic.

from __future__ import annotations

import sys
import time
from typing import Callable

from config import PAUSE_AFTER_LOGO
from display import (
    Colors, clear, typewriter, divider,
    print_result, print_error, print_accounts, get_keypress, LOGO,
)
from higher_lower import load_accounts, pick_pair, check_answer, format_account


def run_classic() -> None:
    # Load all accounts once at the start of the game session.
    # Passing the full list to pick_pair() each round avoids re-loading from config.
    accounts = load_accounts()
    a, b = pick_pair(accounts)  # initial pair — no carry yet
    score = 0

    # --- Rules screen (shown once before the game loop starts) ---
    # Displayed outside the while loop so it only appears at game start,
    # not after every correct guess.
    clear()
    divider()
    print(f"{Colors.CYAN}{Colors.BOLD}CLASSIC{Colors.RESET}")
    divider()
    print(f"  Two Instagram accounts are shown side by side.")
    print(f"  Guess which one has more followers.")
    print()
    print(f"  {Colors.GREEN}Correct{Colors.RESET} — score goes up, account B becomes the new A")
    print(f"  {Colors.RED}Wrong{Colors.RESET}   — game over, final score is shown")
    print()
    print(f"  {Colors.YELLOW}Ties{Colors.RESET}    — both accounts count as correct")
    divider()
    print(f"{Colors.DIM}Press any key to start...{Colors.RESET}")
    get_keypress()  # wait for any key before entering the game loop

    # --- Main game loop ---
    while True:
        # Redraw the full screen on each iteration so stale output never shows.
        clear()
        divider()
        # Score is shown in the header so the player always sees it,
        # even mid-round before a result is printed.
        print(f"{Colors.CYAN}{Colors.BOLD}CLASSIC{Colors.RESET}  {Colors.YELLOW}Score: {score}{Colors.RESET}")
        print(f"{Colors.DIM}A / B = guess  |  Up = menu  |  Q = quit{Colors.RESET}")
        divider()
        print_accounts(format_account(a), format_account(b))
        divider()

        key = get_keypress()

        # Up arrow → return to the advanced menu (exit this function, back to main())
        if key == "up":
            return

        # Q → quit the entire program immediately
        if key.lower() == "q":
            clear()
            sys.exit()

        guess = key.lower()

        # Validate: only 'a' or 'b' are accepted guesses
        if guess not in ("a", "b"):
            print_error("Press A or B to make your guess.")
            time.sleep(1)  # brief pause so the error message is readable before redraw
            continue

        correct = check_answer(guess, a, b)

        if correct:
            score += 1
            print_result(True, score)
            # Pass the current B as carry so it becomes the new A next round.
            # This is the core mechanic: the chain of accounts continues.
            a, b = pick_pair(accounts, carry=b)
            time.sleep(1)  # pause so the player can read the result before redraw
        else:
            print_result(False, score)
            print(f"{Colors.DIM}Enter = play again  |  Up = menu  |  Q = quit{Colors.RESET}")
            key2 = get_keypress()

            if key2 == "up":
                return  # back to menu without restarting

            if key2.lower() == "q":
                clear()
                sys.exit()

            # Any other key (including Enter) restarts the game from score 0
            score = 0
            a, b = pick_pair(accounts)  # fresh pair, no carry


# MODES maps a key string to (display name, one-line description, function).
# main() uses this dict to build the menu and dispatch to the right game.
# Adding a new game variant only requires adding an entry here and writing
# a corresponding run_*() function — main() and show_menu() need no changes.
MODES: dict[str, tuple[str, str, Callable[[], None]]] = {
    "1": ("Classic", "Endless streak — guess until you're wrong", run_classic),
}


def show_menu() -> None:
    # Renders the game selection screen.
    # Iterates over MODES so new entries appear automatically.
    clear()
    divider()
    print(f"{Colors.CYAN}{Colors.BOLD}HIGHER OR LOWER{Colors.RESET}")
    print(f"{Colors.DIM}Instagram followers edition{Colors.RESET}")
    divider()
    for key, (name, desc, _) in MODES.items():
        # Format: [1] Classic  <dim description>
        print(f"  {Colors.YELLOW}[{key}]{Colors.RESET} {Colors.BOLD}{name}{Colors.RESET}  {Colors.DIM}{desc}{Colors.RESET}")
    print(f"  {Colors.YELLOW}[q]{Colors.RESET} Quit")
    divider()


def main() -> None:
    # Play the typewriter logo animation once on launch, then enter the menu loop.
    clear()
    typewriter(LOGO)           # character-by-character animation (see display.py)
    time.sleep(PAUSE_AFTER_LOGO)  # brief pause before the menu appears

    # Menu loop: keep showing the menu until the player quits.
    # Each game function returns when the player presses Up, dropping back here.
    while True:
        show_menu()
        key = get_keypress()

        if key == "q":
            clear()  # leave a clean terminal on exit
            break

        # Dispatch to the selected game's run function (index [2] of the tuple)
        if key in MODES:
            MODES[key][2]()


if __name__ == "__main__":
    main()
