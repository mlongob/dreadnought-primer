"""Sideboard rows: `**Sideboarding (61):** −1 Dreadnought, −2 Daze / +3 Annul, +2 Brain Freeze.`

A row line may hold several labelled rows (`**Sideboarding:** ZIMS: … . Madness: …`), a delta on the row above
(`as above plus −1 Flash / +2 Blue Elemental Blast`), or only prose (`the Terrageddon row, with …`).
"""
from __future__ import annotations

import html
import re
from collections import Counter
from dataclasses import dataclass, field

from .cards import Register, card_img
from .deck import Deck

LINE_RE = re.compile(r"^\*\*(Sideboarding\b[^*]*?|Welder/Tradewind)\s*:?\*\*:?\s*(.*)$")
TOKEN_RE = re.compile(r"([+\-−])\s*(\d+)\s+([A-Za-z][A-Za-z' ]*?)(?=\s*(?:[,;./]|$))")
SEGMENT_SPLIT = re.compile(r"(?<=\.)\s+(?=[A-Z])")
DELTA_RE = re.compile(r"\b(as )?above\b")


class RowError(Exception):
    pass


@dataclass
class Row:
    label: str = ""
    outs: list[tuple[int, str]] = field(default_factory=list)
    ins: list[tuple[int, str]] = field(default_factory=list)
    delta: bool = False
    prose: bool = False
    size: int = 60


def _header_label(header: str) -> tuple[str, int]:
    if header == "Welder/Tradewind":
        return header, 60
    m = re.search(r"\(([^)]*)\)", header)
    if not m:
        return "", 60
    inner = m.group(1).strip()
    return ("", int(inner)) if inner.isdigit() else (inner, 60)


def _tokens(text: str, register: Register) -> list[tuple[str, int, str]]:
    found = []
    for sign, n, name in TOKEN_RE.findall(text):
        n, name = int(n), name.strip()
        if name.lower() == "blasts":
            found += [(sign, n // 2, "Blue Elemental Blast"), (sign, n - n // 2, "Hydroblast")]
        else:
            found.append((sign, n, register.get(name).name))
    return found


def parse_line(line: str, register: Register) -> list[Row] | None:
    m = LINE_RE.match(line.strip())
    if not m:
        return None
    label, size = _header_label(m.group(1).strip())
    rows = []
    for seg in SEGMENT_SPLIT.split(m.group(2)):
        if "/" not in seg or not TOKEN_RE.search(seg):
            continue
        first = TOKEN_RE.search(seg).start()
        lead = seg[:first]
        seg_label = label
        lm = re.match(r"^\s*([^:]+?):\s*$", lead)
        if lm:
            seg_label = lm.group(1).strip()
        toks = _tokens(seg, register)
        rows.append(Row(
            label=seg_label,
            outs=[(n, name) for s, n, name in toks if s != "+"],
            ins=[(n, name) for s, n, name in toks if s == "+"],
            delta=bool(DELTA_RE.search(lead)),
            size=size,
        ))
    return rows or [Row(label=label, prose=True, size=size)]


def problems(rows: list[Row], deck: Deck) -> list[tuple[Row, str]]:
    """Every row that doesn't fit the 75; a delta row is checked together with the row above it."""
    found: list[tuple[Row, str]] = []
    base: Row | None = None
    for row in rows:
        if row.prose:
            continue
        name = f"row {row.label!r}" if row.label else "row"
        if row.delta:
            if base is None:
                found.append((row, f"{name} says 'as above' but there is no row above it"))
                continue
            outs, ins = base.outs + row.outs, base.ins + row.ins
        else:
            outs, ins, base = row.outs, row.ins, row
        out_count, in_count = Counter(), Counter()
        for n, card in outs:
            out_count[card] += n
        for n, card in ins:
            in_count[card] += n
        msg = None
        for card, n in out_count.items():
            if n > deck.main.get(card, 0):
                msg = msg or f"{name} takes out {n} {card}, main has {deck.main.get(card, 0)}"
        for card, n in in_count.items():
            if n > deck.side.get(card, 0):
                msg = msg or f"{name} brings in {n} {card}, sideboard has {deck.side.get(card, 0)}"
        total = 60 - sum(out_count.values()) + sum(in_count.values())
        if not msg and total != row.size:
            msg = f"{name} leaves {total} cards, expected {row.size}"
        if msg:
            found.append((row, msg))
    return found


def validate(rows: list[Row], deck: Deck) -> None:
    """Raise RowError for the first row that doesn't fit the 75."""
    found = problems(rows, deck)
    if found:
        raise RowError(found[0][1])


def stack_html(name: str, n: int, register: Register, sizes: str = "7rem", alt: str | None = None) -> str:
    card = register.get(name)
    # piles over four tighten, but every copy keeps a sliver past the card border
    off = f' style="--off:{max(3.45 / (n - 1), 0.5):.3f}rem"' if n > 4 else ""
    first = f"{n} × {card.name}" if alt is None else alt
    imgs = "".join(card_img(card, sizes, alt=first if i == 0 else "") for i in range(n))
    return f'<div class="stack" title="{n} × {html.escape(card.name)}"{off}>{imgs}</div>'


def piles_html(name: str, n: int, register: Register) -> str:
    """A big count (the Islands) as piles of four, the remainder in a last, smaller pile."""
    if n <= 8:
        return stack_html(name, n, register)
    sizes = [4] * (n // 4) + ([n % 4] if n % 4 else [])
    total = f"{n} × {register.get(name).name}"
    return "".join(stack_html(name, k, register, alt=total if i == 0 else "") for i, k in enumerate(sizes))


def figure_html(row: Row, register: Register, out_label: str = "Out", in_label: str = "In") -> str:
    if row.prose:
        return ""

    def half(cls: str, label: str, items: list[tuple[int, str]]) -> str:
        total = sum(n for n, _ in items)
        stacks = "".join(stack_html(name, n, register, sizes="5.4rem") for n, name in items)
        return (f'<div class="half {cls}"><div class="lbl"><span>{label}</span><span>{total}</span></div>'
                f'<div class="stacks">{stacks}</div></div>')

    cap = f"<figcaption>{html.escape(row.label)}</figcaption>" if row.label else ""
    return (f'<figure class="sbrow">{cap}<div class="pair">'
            f'{half("out", out_label, row.outs)}{half("in", in_label, row.ins)}</div></figure>')
