# menu.py — root-level version selector for the Higher or Lower project.
# Launches either the original (course) version or the advanced (OOP) version
# in a subprocess so each version runs in its own clean Python process.
# After either version exits, this menu reappears — no need to re-run menu.py.

from __future__ import annotations

import os
import subprocess   # used to launch the chosen version as a child process
import sys
from pathlib import Path

# ROOT is the directory containing this file (the project root).
# Using Path(__file__).parent means this works regardless of where you run it from.
ROOT = Path(__file__).parent

# ASCII logo printed at the top of the menu on every loop.
# Inlined here so menu.py has no imports from either version's modules.
LOGO = """
    __  ___       __
   / / / (_)___ _/ /_  ___  _____
  / /_/ / / __ `/ __ \\/ _ \\/ ___/
 / __  / / /_/ / / / /  __/ /
/_/ ///_/\\__, /_/ /_/\\___/_/
   / /  /____/_      _____  _____
  / /   / __ \\ | /| / / _ \\/ ___/
 / /___/ /_/ / |/ |/ /  __/ /
/_____/\\____/|__/|__/\\___/_/
"""

# Maps a menu key to (display label, path to the version's main.py).
# The path is resolved relative to ROOT so it's always absolute.
VERSIONS: dict[str, tuple[str, Path]] = {
    "1": ("Original  (course version — procedural)", ROOT / "original" / "main.py"),
    "2": ("Advanced  (modular OOP)", ROOT / "advanced" / "main.py"),
}


def main() -> None:
    # Loop so the menu reappears after a version exits (e.g. original game ends).
    # The only way out is typing 'q'.
    while True:
        # Clear the terminal before drawing the menu for a clean look.
        os.system("cls" if os.name == "nt" else "clear")
        print(LOGO)
        print("  Version Selector\n")

        # Print each version option from the VERSIONS dict
        for key, (label, _) in VERSIONS.items():
            print(f"  [{key}] {label}")
        print("  [q] Quit\n")

        choice = input("  Enter your choice: ").strip().lower()

        if choice == "q":
            break  # exit the loop, end the program

        if choice not in VERSIONS:
            print("  Invalid choice.")
            input("  Press Enter to continue...")  # pause so the error is readable
            continue  # redraw the menu

        _, path = VERSIONS[choice]

        # subprocess.run launches the selected main.py as a separate Python process.
        # cwd is set to the script's parent directory (original/ or advanced/) so
        # that relative imports like "import art" and "from config import ..." work
        # correctly from within each version's folder.
        subprocess.run([sys.executable, str(path)], cwd=str(path.parent))
        # After the subprocess exits, the while loop continues → menu reappears.


if __name__ == "__main__":
    main()
