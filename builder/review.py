"""The review edition: the page with every change since the last approved state marked in place.

Works on the Markdown, a paragraph (blank-line-separated block) at a time. A changed prose paragraph is
shown as a word-level diff (inline formatting and card links dropped, so the wording stands out). A changed
heading, figure, table or row line still renders normally, with a note above it showing what changed.
"""
from __future__ import annotations

import difflib
import html
import re
from dataclasses import dataclass

STRUCTURAL = ("#", "{", "|", "**Sideboarding", "**Welder")


@dataclass
class Change:
    id: str
    kind: str      # edit, add, remove, heading, figure
    path: str
    snippet: str


def plain(text: str) -> str:
    """Markdown → plain words: drop emphasis, card-link and nolink markup."""
    text = re.sub(r"\[([^\]]+)\]\{[^}]+\}", r"\1", text)
    text = re.sub(r"\{nolink:\s*([^}]+)\}", r"\1", text)
    return re.sub(r"\*\*?([^*]+)\*\*?", r"\1", text).strip()


def word_diff(old: str, new: str) -> str:
    tokens = re.compile(r"\s+|[\w\u2019'/-]+|[^\w\s]")
    a, b = tokens.findall(old), tokens.findall(new)
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        old_part, new_part = html.escape("".join(a[i1:i2])), html.escape("".join(b[j1:j2]))
        if op == "equal":
            out.append(new_part)
            continue
        if old_part.strip():
            out.append(f"<del>{old_part}</del>")
        if new_part.strip():
            out.append(f"<ins>{new_part}</ins>")
        elif new_part:
            out.append(new_part)
    return "".join(out)


def _block(kind: str, cid: str, inner: str) -> str:
    # braces escaped so a removed directive shown as text is never read as one
    inner = inner.replace("{", "&#123;").replace("}", "&#125;")
    return f'<div class="rv rv-{kind}" id="{cid}"><p>{inner}</p></div>'


def _structural(para: str) -> bool:
    return para.lstrip().startswith(STRUCTURAL)


def mark(base: str | None, new: str, path: str, start: int = 1) -> tuple[str, list[Change]]:
    """Return the new text with changes marked, and the list of changes (ids numbered from `start`)."""
    if base == new:
        return new, []
    old_paras = [p for p in re.split(r"\n\s*\n", base.strip())] if base else []
    new_paras = [p for p in re.split(r"\n\s*\n", new.strip())]
    out: list[str] = []
    changes: list[Change] = []

    def record(kind: str, text: str) -> str:
        cid = f"change-{start + len(changes)}"
        changes.append(Change(cid, kind, path, plain(text)[:80]))
        return cid

    def changed(old: str | None, new_p: str | None) -> None:
        if new_p is not None and old is not None and _structural(new_p) != _structural(old):
            changed(old, None)
            changed(None, new_p)
        elif new_p is not None and _structural(new_p):
            kind = "heading" if new_p.startswith("#") else "figure"
            label = "Added" if old is None else "Changed"
            note = html.escape(new_p.strip()) if old is None else word_diff(old.strip(), new_p.strip())
            cid = record(kind, new_p)
            out.append(_block("note", cid, f"{label}: {note}"))
            out.append(new_p)
        elif new_p is None:
            cid = record("remove", old)
            out.append(_block("remove", cid, f"<del>{html.escape(plain(old) if not _structural(old) else old.strip())}</del>"))
        elif old is None:
            cid = record("add", new_p)
            out.append(_block("add", cid, f"<ins>{html.escape(plain(new_p))}</ins>"))
        elif difflib.SequenceMatcher(None, plain(old), plain(new_p), autojunk=False).ratio() < 0.5:
            changed(old, None)   # a rewrite, not an edit: show the old text removed and the new text added
            changed(None, new_p)
        else:
            cid = record("edit", new_p)
            out.append(_block("edit", cid, word_diff(plain(old), plain(new_p))))

    matcher = difflib.SequenceMatcher(None, old_paras, new_paras, autojunk=False)
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            out += new_paras[j1:j2]
            continue
        olds, news = old_paras[i1:i2], new_paras[j1:j2]
        for k in range(max(len(olds), len(news))):
            changed(olds[k] if k < len(olds) else None, news[k] if k < len(news) else None)
    return "\n\n".join(out), changes
