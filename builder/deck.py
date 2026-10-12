"""The 75, from data/deck.toml."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

from .cards import Register, UnknownCard


class DeckError(Exception):
    pass


@dataclass(frozen=True)
class Deck:
    main: dict[str, int]
    side: dict[str, int]
    rows: list[list[str]]


def load(path: Path, register: Register) -> Deck:
    data = tomllib.loads(Path(path).read_text())
    try:
        main = {register.get(n).name: c for n, c in data["main"].items()}
        side = {register.get(n).name: c for n, c in data["side"].items()}
        rows = [[register.get(n).name for n in row] for row in data["rows"]]
    except UnknownCard as e:
        raise DeckError(f"data/deck.toml: {e}") from e
    for label, cards, expected in (("main deck", main, 60), ("sideboard", side, 15)):
        total = sum(cards.values())
        if total != expected:
            raise DeckError(f"data/deck.toml: {label} has {total} cards, expected {expected}")
    in_rows = [n for row in rows for n in row]
    for n in in_rows:
        if n not in main:
            raise DeckError(f"data/deck.toml: rows list {n!r}, which is not in the main deck")
    for n in main:
        if n not in in_rows:
            raise DeckError(f"data/deck.toml: {n!r} is in the main deck but in no row")
    return Deck(main, side, rows)
