from __future__ import annotations

import random
from dataclasses import dataclass

from config import DATA


@dataclass(frozen=True)
class Account:
    name: str
    follower_count: int
    description: str
    country: str


def load_accounts() -> list[Account]:
    return [Account(**entry) for entry in DATA]


def pick_pair(
    accounts: list[Account],
    carry: Account | None = None,
) -> tuple[Account, Account]:
    a = carry if carry is not None else random.choice(accounts)
    b = random.choice(accounts)
    while b == a:
        b = random.choice(accounts)
    return a, b


def check_answer(guess: str, a: Account, b: Account) -> bool:
    if a.follower_count == b.follower_count:
        return True
    return (guess == "a") == (a.follower_count > b.follower_count)


def format_account(account: Account) -> str:
    return f"{account.name}, a {account.description}, from {account.country}"
