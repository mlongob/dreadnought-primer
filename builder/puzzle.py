"""Practice puzzles: a board state drawn MTGO-style, opponent at the top, you at the bottom.

A puzzle is a TOML block between {puzzle} and {/puzzle}:

    turn = 6
    active = "them"            # whose turn: "them" or "you"
    phase = "end"              # one of PHASES
    [them]
    life = 14
    library = 31
    hand = ["?", "?", "Counterspell"]     # "?" is a card you haven't seen; a name is one you have
    lands = ["Island (tapped)", "Underground River"]
    permanents = ["Psychatog", "Powder Keg [1]"]
    graveyard = ["Gush", "Opt"]           # oldest first; the last is on top
    [you]
    ...
    hand = ["Phyrexian Dreadnought", "Stifle (seen)"]   # (seen): the opponent knows it
    library_top = ["Opt", "Island"]    # optional: cards revealed from the top of the library, top first

A choice in progress goes in a [choice] table, drawn as its own band below the stack:

    [choice]
    label = "Impulse: put one into your hand"
    cards = ["Opt", "Gush", "Island", "Stifle"]     # or piles = [["Opt", "Gush"], ["Island"]] for Fact or Fiction

Entries take "(tapped)", "(seen)", "(phased out)", "(attacking)" and "[N]" counters, in any order after the name,
and " + Aura" to attach an aura: "Forest (tapped) + Wild Growth".

A puzzle with something on the stack lists it bottom first, one [[stack]] table per spell or ability;
"ability" makes it an ability (drawn with its source's art and the text), "target" is an optional note:

    storm = 2                  # optional: the storm count, shown only when set
    [[stack]]
    card = "Powder Keg"
    by = "them"
    ability = "Destroy each artifact and creature with mana value 1."
    kind = "activated"         # an ability says whether it is "triggered" or "activated"
    [[stack]]
    card = "Stifle"
    by = "you"
    target = "Powder Keg's ability"
"""
from __future__ import annotations

import html
import re
import tomllib
from dataclasses import dataclass

from .cards import Card, Register, card_img

PHASES = [
    ("upkeep", "Upkeep"), ("draw", "Draw"), ("main1", "Main 1"), ("begin-combat", "Beginning of combat"),
    ("attackers", "Attackers"), ("blockers", "Blockers"), ("damage", "Damage"),
    ("end-combat", "End of combat"), ("main2", "Main 2"), ("end", "End"),
]
PHASE_STARTS = {"upkeep", "main1", "begin-combat", "main2", "end"}
PLAYERS = {"them": "Opponent", "you": "You"}
CARD_BACK = "https://backs.scryfall.io/normal/0/a/0aeebaf5-8c7d-4636-9e82-8c27447861f7.jpg"
SIZES = "(max-width: 640px) 16vw, 5rem"
EYE = ('<svg class="pz-eye" viewBox="0 0 24 24" width="14" height="14" aria-hidden="true">'
       '<path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z" fill="none" stroke="currentColor" '
       'stroke-width="2.2" stroke-linejoin="round"/><circle cx="12" cy="12" r="3" fill="currentColor"/></svg>')

# a short, wide arrow under an attacking creature, pointing at the player it attacks
ATTACK = ('<svg class="pz-attack" viewBox="0 0 40 14" width="40" height="14" role="img" aria-label="Attacking">'
          '<path d="M2 2h36L20 13z" fill="currentColor"/></svg>')

ENTRY_RE = re.compile(r"^(?P<name>.+?)(?P<marks>(?:\s*(?:\((?:tapped|seen|phased out|attacking|naming [^)]+)\)|\[\d+\]))*)\s*$")
STACK = 4                      # identical lands stack in fours
GRAVE_ROW = 6                  # graveyard cards per row


class PuzzleError(Exception):
    pass


@dataclass
class Entry:
    card: Card | None          # None: a card you haven't seen
    tapped: bool = False
    seen: bool = False
    counters: int | None = None
    phased: bool = False
    attacking: bool = False
    ref: str | None = None     # names the card for stack arrows (data-pz-ref)
    auras: tuple = ()          # cards attached to it ("Forest + Wild Growth")
    naming: Card | None = None  # the card a Meddling Mage names ("(naming Phyrexian Dreadnought)")


def parse_entry(text: str, register: Register) -> Entry:
    text = text.strip()
    if text == "?":
        return Entry(None)
    text, *auras = [part.strip() for part in text.split(" + ")]
    m = ENTRY_RE.match(text)
    marks = m.group("marks")
    counters = re.search(r"\[(\d+)\]", marks)
    naming = re.search(r"\(naming ([^)]+)\)", marks)
    return Entry(register.get(m.group("name").strip()), "(tapped)" in marks, "(seen)" in marks,
                 int(counters.group(1)) if counters else None, "(phased out)" in marks, "(attacking)" in marks,
                 auras=tuple(register.get(a) for a in auras),
                 naming=register.get(naming.group(1).strip()) if naming else None)


def _card(e: Entry, seen_label: str) -> str:
    classes = ("pz-card" + (" pz-tapped" if e.tapped else "") + (" pz-seen" if e.seen else "")
               + (" pz-phased" if e.phased else "") + (" pz-attacking" if e.attacking else ""))
    if e.card is None:
        return (f'<span class="{classes} pz-hidden"><img class="pz-back" src="{CARD_BACK}" width="488" height="680" '
                f'alt="An unknown card" loading="lazy"></span>')
    title = f' title="{html.escape(seen_label)}"' if e.seen else ""
    extra = ((f'<span class="pz-counter">{e.counters}</span>' if e.counters is not None else "") + (EYE if e.seen else "")
             + ('<span class="pz-phasetag">Phased out</span>' if e.phased else "")
             + (ATTACK if e.attacking else "")
             + (f'<span class="pz-nametag">Naming: {html.escape(e.naming.name)}</span>' if e.naming else ""))
    ref = f' data-pz-ref="{e.ref}"' if e.ref else ""
    host = f'<span class="{classes}"{ref}{title}>{card_img(e.card, SIZES)}{extra}</span>'
    if not e.auras:
        return host
    # an aura peeks out from behind the permanent it enchants, upright, as MTGO draws it
    auras = "".join(f'<span class="pz-aura">{card_img(a, SIZES)}</span>' for a in e.auras)
    return f'<span class="pz-attached">{auras}{host}</span>'


def _row(cls: str, entries: list[Entry], seen_label: str, empty: str = "") -> str:
    inner = "".join(_card(e, seen_label) for e in entries) or f'<span class="pz-empty">{empty}</span>'
    return f'<div class="{cls}">{inner}</div>'


def _lands(entries: list[Entry], seen_label: str) -> str:
    """Identical lands stack in fours, fanning up and to the right; tapped stacks go after the untapped ones."""
    groups: dict[tuple[str, bool], list[Entry]] = {}
    loose: list[Entry] = []
    for e in entries:
        if e.counters is not None or e.seen or e.phased or e.auras:
            loose.append(e)
        else:
            groups.setdefault((e.card.name, e.tapped), []).append(e)
    parts = []
    for tapped in (False, True):
        for (name, t), group in groups.items():
            if t != tapped:
                continue
            for i in range(0, len(group), STACK):
                chunk = group[i:i + STACK]
                cards = "".join(_card(e, seen_label) for e in chunk)
                parts.append(f'<span class="pz-stack{" pz-stack-tapped" if tapped else ""}" data-n="{len(chunk)}">{cards}</span>')
    parts += [_card(e, seen_label) for e in loose]
    return f'<div class="pz-row pz-lands">{"".join(parts)}</div>'


def _graveyard(entries: list[Entry], seen_label: str) -> str:
    """Every card, oldest first, in rows of GRAVE_ROW: each row overlaps sideways, each row overlaps the one above,
    so the top of the graveyard sits bottom right, in full."""
    rows = [entries[i:i + GRAVE_ROW] for i in range(0, len(entries), GRAVE_ROW)]
    inner = "".join(f'<div class="pz-pilerow">{"".join(_card(e, seen_label) for e in row)}</div>' for row in rows)
    pile = f'<div class="pz-pile">{inner or "<span class=\"pz-empty\">Empty</span>"}</div>'
    return f'<div class="pz-graveyard"><span class="pz-label">Graveyard ({len(entries)})</span>{pile}</div>'


def _side(who: str, data: dict, register: Register, refs: dict[str, str]) -> str:
    def entries(key: str) -> list[Entry]:
        return [parse_entry(t, register) for t in data.get(key, [])]
    hand, lands, perms, grave = entries("hand"), entries("lands"), entries("permanents"), entries("graveyard")
    for kind, group in (("perm", perms), ("land", lands)):     # what a stack item can point at, by name
        for i, e in enumerate(group):
            e.ref = f"{who}-{kind}-{i}"
            if e.card is not None:
                refs.setdefault(e.card.name.lower(), e.ref)
    if who == "them":
        for e in hand:
            e.seen = e.card is not None    # a named card in their hand is one you have seen
        seen_label = "You have seen this card"
    else:
        seen_label = "Your opponent has seen this card"
    library = int(data["library"])
    player = (f'<div class="pz-player"><span class="pz-name">{PLAYERS[who]}</span>'
              f'<span class="pz-life" data-pz-ref="{who}-life" title="Life total"><b>{int(data["life"])}</b> life</span>'
              f'<span class="pz-label">Hand ({len(hand)})</span></div>')   # the label sits beside the cards, not above them
    backs = "".join(f'<img class="pz-back" src="{CARD_BACK}" width="488" height="680" alt="" loading="lazy">'
                    for _ in range(min(library, 3)))
    top = entries("library_top")           # cards revealed from the top (a Portent, say), top card first
    for e in top:
        e.seen = True
    revealed = (f'<div class="pz-revealed"><span class="pz-label">Top {len(top)}, top card first</span>'
                f'{_row("pz-toprow", top, "Revealed from the top of the library")}</div>' if top else "")
    library_html = (f'<div class="pz-library"><span class="pz-label">Library</span><span class="pz-deck">{backs}'
                    f'<span class="pz-count" title="{library} cards in library">{library}</span></span>{revealed}</div>')
    hand_html = f'<div class="pz-handzone">{player}{_row("pz-hand", hand, seen_label, "No cards in hand")}</div>'
    field = [_lands(lands, seen_label), _row("pz-row pz-perms", perms, seen_label)]
    if who == "you":
        field.reverse()                # permanents face the middle of the table on both sides
    grave_html = _graveyard(grave, seen_label)
    piles = [library_html, grave_html] if who == "them" else [grave_html, library_html]
    board = (f'<div class="pz-zones"><div class="pz-battlefield">{"".join(field)}</div>'
             f'<div class="pz-piles">{"".join(piles)}</div></div>')
    parts = [hand_html, board] if who == "them" else [board, hand_html]
    return f'<div class="pz-side pz-{who}">{"".join(parts)}</div>'


def _stack(items: list[dict], register: Register, refs: dict[str, str]) -> str:
    """The stack, bottom on the left and top on the right, slightly overlapping; each item leans towards the
    player who put it there."""
    lis = []
    for item in items:
        by = item.get("by")
        if by not in PLAYERS:
            raise PuzzleError(f'a stack item needs by = "them" or "you", got {by!r}')
        card = register.get(item["card"])
        e = html.escape
        if "ability" in item:
            kind = item.get("kind")
            if kind not in ("triggered", "activated"):
                raise PuzzleError(f'{card.name}\'s ability needs kind = "triggered" or "activated", got {kind!r}')
            face = (f'<span class="pz-abil"><img class="pz-art" src="{card.image("art_crop")}" alt="" loading="lazy">'
                    f'<span class="pz-abil-head"><b class="pz-abil-name">{e(card.name)}</b>'
                    f'<span class="pz-abil-kind">{kind.capitalize()} ability</span></span><span class="pz-abil-text">{e(item["ability"])}</span></span>')
            what = f"{e(card.name)}'s ability: {e(item['ability'])}"   # the full text, if the tile cuts it short
        else:
            face = f'<span class="pz-card">{card_img(card, SIZES)}</span>'
            what = e(card.name)
        target = f'<span class="pz-target">Targeting {e(item["target"])}</span>' if "target" in item else ""
        # an arrow is drawn to the target when it names a player, a spell or ability below this one, or a permanent
        aim = refs.get(item["target"].strip().lower()) if "target" in item else None
        aim_attr = f' data-pz-target="{aim}"' if aim else ""
        ref = f"stack-{len(lis)}"
        refs["{}'s ability".format(card.name).lower() if "ability" in item else card.name.lower()] = ref
        owner = "your opponent" if by == "them" else "you"
        lis.append(f'<li class="pz-item pz-by-{by}{" pz-ability" if "ability" in item else ""}" data-pz-ref="{ref}"{aim_attr} '
                   f'title="{what}, from {owner}">{face}{target}</li>')
    targets = " pz-has-targets" if any("target" in item for item in items) else ""
    return (f'<div class="pz-stackzone{targets}"><span class="pz-label">Stack</span>'
            f'<ol class="pz-stackitems">{"".join(lis)}</ol></div>')


def _choice(choice: dict, register: Register) -> str:
    """A choice in progress: the cards an Impulse shows, or the piles of a Fact or Fiction, face up."""
    label = html.escape(choice.get("label", "Choose"))
    if "piles" in choice:
        groups = [[parse_entry(t, register) for t in pile] for pile in choice["piles"]]
        inner = "".join(f'<div class="pz-pile-choice">{"".join(_card(e, "") for e in g) or "<span class=\"pz-empty\">Empty</span>"}</div>'
                        for g in groups)
    else:
        inner = "".join(_card(parse_entry(t, register), "") for t in choice.get("cards", []))
    return f'<div class="pz-choice"><span class="pz-label">{label}</span><div class="pz-choicecards">{inner}</div></div>'


def _turn(data: dict) -> str:
    keys = [k for k, _ in PHASES]
    if data.get("phase") not in keys:
        raise PuzzleError(f"phase must be one of {', '.join(keys)}, got {data.get('phase')!r}")
    if data.get("active") not in PLAYERS:
        raise PuzzleError(f'active must be "them" or "you", got {data.get("active")!r}')
    # the bar sits between the battlefields; the arrow on the current phase points at whoever's turn it is
    # the steps of one phase are chained; a rule separates the phases (beginning, main, combat, main, ending)
    phases = "".join(f'<li class="pz-phase{" current" if k == data["phase"] else ""}"{" data-start" if k in PHASE_STARTS else ""}>{label}</li>'
                     for k, label in PHASES)
    whose = "Your" if data["active"] == "you" else "Opponent's"
    storm = (f'<span class="pz-storm" title="Storm count"><small>Storm</small><b>{int(data["storm"])}</b></span>'
             if "storm" in data else "")
    return (f'<div class="pz-turn pz-active-{data["active"]}"><span class="pz-turnno" title="{whose} turn">'
            f'<small>Turn</small><b>{int(data["turn"])}</b></span>'
            f'<ol class="pz-phases">{phases}</ol>{storm}</div>')


def render(block: str, register: Register) -> str:
    try:
        data = tomllib.loads(block)
    except tomllib.TOMLDecodeError as e:
        raise PuzzleError(f"puzzle is not valid TOML: {e}") from e
    for who in PLAYERS:
        if who not in data or "life" not in data[who] or "library" not in data[who]:
            raise PuzzleError(f"puzzle needs a [{who}] table with life and library")
    refs = {"opponent": "them-life", "them": "them-life", "you": "you-life"}
    them, you = _side("them", data["them"], register, refs), _side("you", data["you"], register, refs)
    stack = _stack(data["stack"], register, refs) if data.get("stack") else ""
    choice = _choice(data["choice"], register) if data.get("choice") else ""
    return f'<figure class="puzzle">{them}{stack}{_turn(data)}{choice}{you}</figure>'
