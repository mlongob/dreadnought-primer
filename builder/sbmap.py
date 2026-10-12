"""The quick-reference sideboard map, generated from each matchup's rows and `[[map]]` front matter."""
from __future__ import annotations

import html

from .outline import Source
from .rows import Row

ABBR = {
    "Phyrexian Dreadnought": "DN", "Vision Charm": "VC", "Brain Freeze": "BF", "Back to Basics": "B2B",
    "Flash of Insight": "Flash", "Powder Keg": "Keg", "Chain of Vapor": "Chain", "Essence Flare": "Flare",
    "Blue Elemental Blast": "BEB",
}


class MapError(Exception):
    pass


def format_items(items: list[tuple[int, str]]) -> str:
    """'1 DN, 2 Daze'; two Blue Elemental Blast with two Hydroblast read as '4 Blasts'."""
    names = {name: n for n, name in items}
    blasts = names.get("Blue Elemental Blast") == 2 and names.get("Hydroblast") == 2
    parts = []
    for n, name in items:
        if blasts and name == "Hydroblast":
            continue
        if blasts and name == "Blue Elemental Blast":
            parts.append("4 Blasts")
        else:
            parts.append(f"{n} {ABBR.get(name, name)}")
    return ", ".join(parts)


def _cells(row: Row, entry: dict, path) -> tuple[str, str]:
    if "out" in entry or "in" in entry:
        return entry.get("out", ""), entry.get("in", "")
    if row.prose:
        raise MapError(f"{path}: row {row.label!r} is prose; give its [[map]] entry 'out' and 'in'")
    prefix = "above + " if row.delta else ""
    return prefix + format_items(row.outs), prefix + format_items(row.ins)


def sideboard_map(matchups: list[tuple[Source, list[Row]]], anchors: dict[str, str],
                  headers: tuple[str, ...] = ("Matchup", "Out", "In")) -> str:
    """anchors: matchup slug -> id of the matchup's heading."""
    lines = []
    for source, rows in matchups:
        entries = source.meta.get("map", [])
        if len(entries) != len(rows):
            raise MapError(f"{source.path}: {len(entries)} map entries but {len(rows)} row{'s' if len(rows) != 1 else ''}")
        anchor = anchors.get(source.slug, source.slug)
        for row, entry in zip(rows, entries):
            if entry.get("omit"):  # the author is still working this row out
                continue
            out, in_ = _cells(row, entry, source.path)
            lines.append(f'<tr><td><a href="#{anchor}">{html.escape(entry["label"])}</a></td>'
                         f'<td>{html.escape(out)}</td><td>{html.escape(in_)}</td></tr>')
    head = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    return ('<div class="table-wrap"><table class="sbmap"><thead><tr>'
            f'{head}</tr></thead><tbody>{"".join(lines)}</tbody></table></div>')
