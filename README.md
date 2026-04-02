# Day 14 — Higher or Lower

A terminal game based on the [Higher Lower Game](https://www.higherlowergame.com/). Two Instagram accounts are shown side by side — guess which one has more followers. Correct guess keeps the streak alive; wrong guess ends the game.

This repo contains two versions of the same game: the original course solution and a fully rebuilt advanced version, plus a root menu to launch either one.

---

## Quick Start

```bash
python menu.py            # version selector (recommended entry point)
python original/main.py   # run the course version directly
python advanced/main.py   # run the advanced version directly
```

No external dependencies — standard library only.

---

## How to Play

- Two Instagram accounts appear on screen labelled **A** and **B**
- Press **A** or **B** to guess who has more followers
- **Correct** — your score goes up; account B becomes the new A, and a fresh B is drawn
- **Wrong** — game over, your final score is shown
- **Tie** — if both accounts have the same count, any guess is accepted as correct

---

## Project Structure

```
menu.py               — root version selector, launches original/ or advanced/ via subprocess
requirements.txt      — no external dependencies (standard library only)
README.md             — this file

original/
  main.py             — complete course solution: data, functions, and game loop in one file
  art.py              — ASCII logo and VS separator

advanced/
  main.py             — entry point: typewriter logo, menu loop, MODES dispatcher
  higher_lower.py     — pure game logic: Account dataclass, pick_pair, check_answer
  display.py          — all terminal UI: colors, clear, typewriter, divider, get_keypress
  config.py           — all constants (delays, widths) and the full account dataset

docs/
  COURSE_NOTES.md     — original course exercise description and concepts covered
```

---

## Versions

### Original

Close to what was written during the course. Single-file, procedural style.

**Key features:**
- All data, functions, and game loop in `main.py`
- `art.py` holds the logo and VS separator as plain strings
- Input validated with a nested `while` loop
- Screen cleared by printing 25 blank lines
- `random.choice()` to select accounts each round

**Concepts practiced:** functions, return values, while loops, module imports, f-strings, input validation.

---

### Advanced

A complete ground-up rebuild using modular design and Python best practices. Same game mechanics, very different architecture.

**Key features:**
- **Frozen dataclass** (`Account`) instead of raw dicts — typed, immutable, comparable with `==`
- **Strict layer separation** — `higher_lower.py` has zero UI imports; `display.py` has zero game logic
- **ANSI color UI** — cyan headers, green correct, red wrong, yellow score/keys, dim instructions
- **Typewriter animation** on logo launch using `sys.stdout.write` + `sys.stdout.flush`
- **Single-keypress input** via `termios`/`tty` raw mode — no Enter needed to submit a guess
- **Arrow key navigation** — Up arrow returns to the menu from anywhere in the game
- **MODES dict dispatcher** — adding a new game variant only requires a new dict entry and a `run_*()` function
- **Rules screen** shown once before the game loop starts
- **Score visible in header** at all times, not just after a result
- Full **type hints** throughout (`str`, `list[Account]`, `tuple[Account, Account]`, `Callable`)

---

## Architecture: Advanced Version

```
menu.py  ──subprocess──▶  advanced/main.py
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
             config.py   higher_lower.py  display.py
             (data +      (pure logic,    (all output
             constants)   no print())     + input)
```

**Rule:** `higher_lower.py` may import from `config.py`. `display.py` may import from `config.py`. `main.py` may import from all three. Nothing imports from `main.py`. This keeps the logic testable and the UI swappable.

---

## File-by-File: Advanced

### `config.py`
Holds every constant and the full account dataset. No logic, no imports. Changing animation speed or adding accounts is done here and nowhere else.

| Constant | Value | Purpose |
|---|---|---|
| `TYPEWRITER_DELAY` | `0.004s` | Milliseconds per character in the logo animation |
| `PAUSE_AFTER_LOGO` | `0.8s` | Pause after logo before the menu appears |
| `DIVIDER_WIDTH` | `50` | Width of `─────` separator lines |
| `DATA` | list of 50 dicts | All Instagram accounts (follower counts in millions) |

### `higher_lower.py`
Pure logic — no `print()`, no `input()`, no terminal imports.

- **`Account`** — frozen dataclass. `frozen=True` makes it immutable and hashable; `**entry` unpacking converts each dict from `DATA` directly into a typed object.
- **`pick_pair(accounts, carry)`** — selects A and B. The `carry` parameter is how "B becomes the new A" is implemented: pass the previous B in and it becomes A without being re-rolled.
- **`check_answer(guess, a, b)`** — uses a compact boolean comparison: `(guess == "a") == (a.follower_count > b.follower_count)`. Both sides evaluate to `True`/`False`; they match only when the guess is correct.

### `display.py`
All terminal output and input. Nothing else calls `print()` directly.

- **`Colors`** — class of ANSI escape code strings. Convention: CYAN = headers, GREEN = win, RED = loss/error, YELLOW = score/keys, DIM = instructions.
- **`typewriter()`** — `sys.stdout.write` + `flush` per character with `time.sleep` between them. Unlike `print()`, this doesn't add a newline and outputs immediately without line-buffering.
- **`get_keypress()`** — switches the terminal into raw mode (`tty.setraw`) so keypresses are sent directly to the program without waiting for Enter. Detects arrow keys by reading the 3-byte escape sequence `ESC [ A`. Always restores terminal settings in a `finally` block.

### `main.py`
Orchestrates the other three modules. Contains no game logic and no raw `print()` calls.

- Plays the typewriter logo on launch, then enters a `while True` menu loop.
- **`MODES`** dict maps key strings to `(name, description, run_function)` tuples. `show_menu()` iterates over it to build the menu automatically — no hardcoded labels.
- Each `run_*()` function shows a rules screen once, then runs the game loop. Up arrow `return`s to `main()`; Q calls `sys.exit()`.

---

## UX Conventions (Advanced)

| Key | Action |
|---|---|
| A / B | Submit guess |
| Up arrow | Return to menu |
| Q | Quit immediately |
| Enter | Play again (after game over) |

Every screen follows the same structure:
```
clear() → divider() → CYAN BOLD header → DIM instructions → divider() → content
```
