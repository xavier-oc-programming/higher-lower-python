# higher_lower.py — pure game logic. No print(), no input(), no UI imports.
# Keeping the logic here isolated means it can be tested independently of
# the terminal, and the display layer can change freely without breaking the rules.

from __future__ import annotations

import random
from dataclasses import dataclass

from config import DATA


# A frozen dataclass is used instead of a plain dict for two reasons:
#   1. Attribute access (account.name) is clearer than key access (account["name"]).
#   2. frozen=True makes instances immutable and hashable, so they can be
#      compared with == and used in sets if needed (e.g. to prevent duplicates).
@dataclass(frozen=True)
class Account:
    name: str
    follower_count: int   # in millions
    description: str
    country: str


def load_accounts() -> list[Account]:
    # Converts the raw list of dicts from config.DATA into typed Account objects.
    # **entry unpacks each dict as keyword arguments matching the dataclass fields.
    return [Account(**entry) for entry in DATA]


def pick_pair(
    accounts: list[Account],
    carry: Account | None = None,
) -> tuple[Account, Account]:
    # Selects two different accounts to show as A and B.
    #
    # The carry parameter implements the "B becomes next A" mechanic:
    # after a correct guess, the caller passes the previous B in as carry
    # so it becomes the new A, and only a fresh B is randomly chosen.
    # If carry is None (start of game or after a loss), both are random.
    a = carry if carry is not None else random.choice(accounts)

    # Keep re-rolling B until it's a different account from A.
    # This prevents "Instagram vs Instagram" comparisons with identical counts.
    b = random.choice(accounts)
    while b == a:
        b = random.choice(accounts)

    return a, b


def check_answer(guess: str, a: Account, b: Account) -> bool:
    # Returns True if the player's guess is correct.
    #
    # Tie case: if both accounts have exactly the same follower count,
    # the player can't lose — any guess is accepted as correct.
    if a.follower_count == b.follower_count:
        return True

    # Compact boolean comparison:
    #   (guess == "a") produces True/False
    #   (a.follower_count > b.follower_count) produces True/False
    # They're equal only when the guess matches reality:
    #   - guess "a" AND a has more  → True == True  → correct
    #   - guess "b" AND b has more  → False == False → correct
    #   - guess "a" AND b has more  → True == False  → wrong
    return (guess == "a") == (a.follower_count > b.follower_count)


def format_account(account: Account) -> str:
    # Returns the human-readable label shown for each account during gameplay.
    # Example: "Taylor Swift, a Musician, from United States"
    return f"{account.name}, a {account.description}, from {account.country}"
