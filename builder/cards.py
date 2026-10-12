"""The card register: every card the primer shows or links, with its Scryfall printing."""
from __future__ import annotations

import html
import tomllib
from dataclasses import dataclass
from pathlib import Path

IMAGE_HOST = "https://cards.scryfall.io"


class UnknownCard(Exception):
    pass


@dataclass(frozen=True)
class Card:
    name: str
    id: str
    set: str
    number: str

    def image(self, size: str) -> str:
        return f"{IMAGE_HOST}/{size}/front/{self.id[0]}/{self.id[1]}/{self.id}.jpg"

    @property
    def page(self) -> str:
        return f"https://scryfall.com/card/{self.set}/{self.number}"


class Register:
    def __init__(self, cards: dict[str, Card], aliases: dict[str, str], deck_names: frozenset[str] = frozenset()):
        self.cards = cards
        self.aliases = aliases
        self.deck_names = deck_names

    @classmethod
    def load(cls, path: Path) -> Register:
        data = tomllib.loads(Path(path).read_text())
        cards = {name: Card(name, c["id"], c["set"], str(c["number"])) for name, c in data.get("cards", {}).items()}
        aliases = dict(data.get("aliases", {}))
        for alias, target in aliases.items():
            if target not in cards:
                raise UnknownCard(f"alias {alias!r} points to {target!r}, which is not in the register")
        return cls(cards, aliases, frozenset(data.get("deck_names", [])))

    def get(self, name: str) -> Card:
        name = name.strip()
        card = self.cards.get(self.aliases.get(name, name))
        if card is None:
            raise UnknownCard(f"{name!r} is not in data/cards.toml; add it with: python tools/add_card.py {name!r}")
        return card

    def names(self) -> dict[str, str]:
        """Every linkable name (card names and aliases) mapped to its canonical card name."""
        return {**{n: n for n in self.cards}, **self.aliases}

    def linkable_names(self) -> dict[str, str]:
        """Names linked automatically: everything except card names that are also deck names."""
        return {n: c for n, c in self.names().items() if n not in self.deck_names}


def card_img(card: Card, sizes: str, eager: bool = False, alt: str | None = None) -> str:
    """One card image: Scryfall small/normal srcset, fixed aspect, data for the preview and lightbox."""
    e = html.escape
    return (
        f'<img class="mtg" src="{card.image("normal")}" '
        f'srcset="{card.image("small")} 146w, {card.image("normal")} 488w" sizes="{sizes}" '
        f'width="488" height="680" loading="{"eager" if eager else "lazy"}" decoding="async" '
        f'alt="{e(card.name if alt is None else alt)}" data-card="{e(card.name)}" '
        f'data-img="{card.id}" data-page="{card.page}">'
    )
