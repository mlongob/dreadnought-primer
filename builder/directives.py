"""Block directives in content files: card images, the decklist, the combo figure, row figures.

Each directive stands alone on its line and becomes a raw HTML block with blank lines around it, so
Markdown never folds it into the neighbouring paragraph. Inline syntax ({nolink: …}, [text]{Card})
is left for the Markdown extension.
"""
from __future__ import annotations

import html
import re
import tomllib
from dataclasses import dataclass, field

from .strings import strings
from pathlib import Path

from . import puzzle as puzzlemod
from . import rows as rowmod
from .cards import Register, UnknownCard, card_img
from .deck import Deck
from .outline import Source

BLOCK_RE = re.compile(r"^\{([a-z-]+)(?::\s*([^}]*))?\}\s*$")
INLINE_ONLY = {"nolink"}

SIZES_MARGIN = "(min-width: 1440px) 14rem, (max-width: 640px) 42vw, 34vw"
SIZES_ROW = "(max-width: 640px) 45vw, 11.5rem"
SIZES_HAND = "(max-width: 640px) 22vw, 6rem"


class DirectiveError(Exception):
    pass


@dataclass
class Context:
    register: Register
    deck: Deck
    combo: dict
    labels: dict = field(default_factory=lambda: strings("en"))


@dataclass
class Expanded:
    text: str
    rows: list[rowmod.Row] = field(default_factory=list)


def load_combo(path: Path) -> dict:
    return tomllib.loads(Path(path).read_text())


def _names(arg: str | None) -> list[str]:
    return [n.strip() for n in (arg or "").split("|") if n.strip()]


def _block(markup: str) -> str:
    return f"\n{markup}\n\n"


def _cards(names: list[str], ctx: Context, sizes: str) -> str:
    return "".join(card_img(ctx.register.get(n), sizes) for n in names)


def _decklist(ctx: Context) -> str:
    reg, deck = ctx.register, ctx.deck
    main = "".join(
        '<div class="rowcards">' + "".join(rowmod.piles_html(n, deck.main[n], reg) for n in row) + "</div>"
        for row in deck.rows)
    side = '<div class="rowcards">' + "".join(rowmod.stack_html(n, c, reg) for n, c in deck.side.items()) + "</div>"
    t = ctx.labels
    return (f'<div class="deck"><p class="decklabel">{t["main_deck"]}, {sum(deck.main.values())}</p>{main}'
            f'<p class="decklabel">{t["sideboard"]}, {sum(deck.side.values())}</p>{side}</div>')


def _combo(ctx: Context) -> str:
    parts = []
    for step in ctx.combo["steps"]:
        if step.get("join"):
            parts.append(f'<div class="join">{html.escape(step["join"])}</div>')
        img = card_img(ctx.register.get(step["card"]), "(max-width: 640px) 7rem, 13rem", eager=True)
        parts.append(f'<div class="step">{img}<p><b>{html.escape(step["title"])}</b>{html.escape(step["text"])}</p></div>')
    return (f'<figure class="combo"><div class="steps">{"".join(parts)}</div>'
            f'<figcaption>{html.escape(ctx.combo["caption"])}</figcaption></figure>')


def _directive(name: str, arg: str | None, ctx: Context) -> str:
    if name == "card":
        names = _names(arg)
        if len(names) != 1:
            raise DirectiveError(f"{{card:}} takes one card, got {len(names)}")
        return f'<figure class="margin-card">{_cards(names, ctx, SIZES_MARGIN)}</figure>'
    if name == "cards":
        names = _names(arg)
        if not 1 <= len(names) <= 4:
            raise DirectiveError(f"{{cards:}} takes at most four cards, got {len(names)}")
        return f'<div class="cardrow">{_cards(names, ctx, SIZES_ROW)}</div>'
    if name == "hand":
        names = _names(arg)
        if len(names) != 7:
            raise DirectiveError(f"{{hand:}} takes seven cards, got {len(names)}")
        return f'<div class="hand">{_cards(names, ctx, SIZES_HAND)}</div>'
    if name == "decklist":
        return _decklist(ctx)
    if name == "combo":
        return _combo(ctx)
    if name == "sideboard-map":
        return "<!--sideboard-map-->"
    raise DirectiveError(f"unknown directive {{{name}}}")


ANSWER_OPEN = '<details class="pz-answer" markdown="1"><summary>{label}</summary>'


def expand(source: Source, ctx: Context) -> Expanded:
    out, found = [], []
    puzzle: list[str] | None = None
    puzzle_start = ""
    for i, line in enumerate(source.text.split("\n")):
        where = f"{source.path}:{source.line_offset + i + 1}"
        if puzzle is not None:
            if line.strip() == "{/puzzle}":
                try:
                    out.append(_block(puzzlemod.render("\n".join(puzzle), ctx.register)))
                except (puzzlemod.PuzzleError, UnknownCard) as e:
                    raise DirectiveError(f"{puzzle_start}: {e}") from e
                puzzle = None
            else:
                puzzle.append(line)
            continue
        if line.strip() == "{puzzle}":
            puzzle, puzzle_start = [], where
            continue
        if line.strip() == "{answer}":
            out.append(_block(ANSWER_OPEN.format(label=html.escape(ctx.labels["show_answer"]))))
            continue
        if line.strip() == "{/answer}":
            out.append(_block("</details>"))
            continue
        try:
            m = BLOCK_RE.match(line)
            if m and m.group(1) not in INLINE_ONLY:
                out.append(_block(_directive(m.group(1), m.group(2), ctx)))
                continue
            parsed = rowmod.parse_line(line, ctx.register)
        except (DirectiveError, UnknownCard) as e:
            raise DirectiveError(f"{where}: {e}") from e
        out.append(line)
        if parsed:
            found += parsed
            figures = "".join(rowmod.figure_html(r, ctx.register, ctx.labels["out"], ctx.labels["in"]) for r in parsed)
            if figures:
                out.append(_block(figures))
    if puzzle is not None:
        raise DirectiveError(f"{puzzle_start}: {{puzzle}} has no closing {{/puzzle}}")
    return Expanded("\n".join(out), found)
