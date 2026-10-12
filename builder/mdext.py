"""Markdown → HTML with heading ids, the sidebar tree, and first-mention card links.

Card links: the first mention of a card in each section (a section runs from one ##/### heading to
the next) links to the card; later mentions stay plain. `{nolink: text}` is never linked;
`[text]{Card Name}` always links and counts as the mention.
"""
from __future__ import annotations

import html
import re
import xml.etree.ElementTree as etree
from dataclasses import dataclass, field

import markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.treeprocessors import Treeprocessor

from .cards import Card, Register

NOLINK_RE = r"\{nolink:\s*([^}]+)\}"
FORCED_RE = r"\[([^\]]+)\]\{([^}]+)\}"
LINKABLE = {"p", "li", "td", "figcaption"}
SKIP = {"a", "code", "pre", "th", "h1", "h2", "h3", "h4", "h5", "h6"}
# ids the page template uses; headings must not take them
RESERVED_IDS = {"top", "toc", "where", "zoom"}
ESCAPE_RE = re.compile("\x02(\\d+)\x03")
STASH_RE = re.compile("\x02wzxhzdk:(\\d+)\x03")


@dataclass
class TocEntry:
    level: int
    id: str
    label: str
    children: list[TocEntry] = field(default_factory=list)


def toc_label(text: str) -> str:
    """Drop parentheticals that hold counts: 'Opt (4), Impulse (2), Peek (1)' -> 'Opt, Impulse, Peek'."""
    return re.sub(r"\s*\([^)]*\d[^)]*\)", "", text).strip()


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"\([^)]*\)", "", text).lower()).strip("-")


def card_link(card: Card, text: str) -> etree.Element:
    a = etree.Element("a", {"class": "cardref", "href": card.page, "data-card": card.name, "data-img": card.id})
    a.text = text
    return a


class NolinkProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        el = etree.Element("span", {"class": "nolink"})
        el.text = m.group(1).strip()
        return el, m.start(0), m.end(0)


class ForcedLinkProcessor(InlineProcessor):
    def __init__(self, pattern, md, register: Register):
        super().__init__(pattern, md)
        self.register = register

    def handleMatch(self, m, data):
        return card_link(self.register.get(m.group(2)), m.group(1)), m.start(0), m.end(0)


class SectionProcessor(Treeprocessor):
    def __init__(self, md, register: Register, chapter_ids: list[str], anchor_label: str = "Link to this section"):
        super().__init__(md)
        self.anchor_label = anchor_label
        self.register = register
        self.chapter_ids = chapter_ids
        names = register.linkable_names()
        self.names = names
        alternation = "|".join(re.escape(n) for n in sorted(names, key=len, reverse=True))
        self.name_re = re.compile(rf"(?<![\w'’])({alternation})(?:e?s)?(?!\w)")
        self.toc: list[TocEntry] = []
        self.used: set[str] = set(chapter_ids) | RESERVED_IDS
        self.first_id: str | None = None

    def plain_text(self, el: etree.Element) -> str:
        """An element's text with Markdown's escape and raw-HTML placeholders resolved."""
        text = "".join(el.itertext())
        text = STASH_RE.sub(lambda m: html.unescape(re.sub(r"<[^>]+>", "", str(self.md.htmlStash.rawHtmlBlocks[int(m.group(1))]))), text)
        return ESCAPE_RE.sub(lambda m: chr(int(m.group(1))), text).strip()

    # -- headings ---------------------------------------------------------------------------------
    def heading(self, el: etree.Element) -> None:
        used = self.used
        text = self.plain_text(el)
        if el.tag == "h2":
            if len(self.toc) >= len(self.chapter_ids):
                raise ValueError("more '## ' headings than chapters in the outline")
            hid = self.chapter_ids[len(self.toc)]
            el.set("id", hid)
            self.toc.append(TocEntry(2, hid, toc_label(text)))
        else:
            base = slugify(toc_label(text)) or "section"
            hid, n = base, 1
            while hid in used:
                n += 1
                hid = f"{base}-{n}"
            el.set("id", hid)
            entry = TocEntry(3, hid, toc_label(text))
            (self.toc[-1].children if self.toc else self.toc).append(entry)
        used.add(el.get("id"))
        anchor = etree.SubElement(el, "a", {"class": "anchor", "href": f"#{el.get('id')}", "aria-label": self.anchor_label})
        anchor.text = "#"
        if self.first_id is None:
            self.first_id = el.get("id")

    # -- card links -------------------------------------------------------------------------------
    def split(self, text: str | None, seen: set[str]) -> tuple[str | None, list[etree.Element]]:
        """Split text at first mentions; return the leading text and link elements (tails set)."""
        if not text:
            return text, []
        lead, links, pos = None, [], 0
        for m in self.name_re.finditer(text):
            card = self.register.get(self.names[m.group(1)])
            if card.name in seen:
                continue
            seen.add(card.name)
            before = text[pos:m.start()]
            if links:
                links[-1].tail = (links[-1].tail or "") + before
            else:
                lead = before
            links.append(card_link(card, m.group(0)))
            pos = m.end()
        if not links:
            return text, []
        links[-1].tail = text[pos:]
        return lead, links

    @staticmethod
    def unwrap(parent: etree.Element, child: etree.Element) -> None:
        """Replace a link with its text, keeping the text that follows it."""
        text = (child.text or "") + (child.tail or "")
        idx = list(parent).index(child)
        if idx == 0:
            parent.text = (parent.text or "") + text
        else:
            prev = parent[idx - 1]
            prev.tail = (prev.tail or "") + text
        parent.remove(child)

    def linkify(self, el: etree.Element, seen: set[str], linkable: bool) -> None:
        if el.tag in SKIP or el.get("class") == "nolink":
            if el.tag == "a" and el.get("class") == "cardref":
                seen.add(el.get("data-card"))
            return
        linkable = linkable or el.tag in LINKABLE
        children = list(el)
        if linkable:
            el.text, new = self.split(el.text, seen)
            for i, a in enumerate(new):
                el.insert(i, a)
        for child in children:
            if child.tag == "a" and child.get("class") == "cardref" and child.get("data-card") in seen:
                self.unwrap(el, child)  # a marked mention after the first one: plain text
                continue
            self.linkify(child, seen, linkable)
            if linkable:
                child.tail, new = self.split(child.tail, seen)
                idx = list(el).index(child)
                for i, a in enumerate(new):
                    el.insert(idx + 1 + i, a)

    def run(self, root: etree.Element) -> None:
        seen: set[str] = set()
        self.first_id = None
        for el in list(root):
            if el.tag in ("h2", "h3"):
                self.heading(el)
                seen = set()
            else:
                self.linkify(el, seen, False)


class PrimerExtension(Extension):
    def __init__(self, register: Register, chapter_ids: list[str], anchor_label: str = "Link to this section"):
        super().__init__()
        self.register = register
        self.chapter_ids = chapter_ids
        self.anchor_label = anchor_label
        self.processor: SectionProcessor | None = None

    def extendMarkdown(self, md):
        md.inlinePatterns.register(NolinkProcessor(NOLINK_RE, md), "nolink", 176)
        md.inlinePatterns.register(ForcedLinkProcessor(FORCED_RE, md, self.register), "cardlink", 175)
        self.processor = SectionProcessor(md, self.register, self.chapter_ids, self.anchor_label)
        md.treeprocessors.register(self.processor, "primer-sections", 15)


def convert_many(chunks: list[str], register: Register, chapter_ids: list[str],
                 anchor_label: str = "Link to this section") -> tuple[list[str], list[TocEntry], list[str | None]]:
    """Convert each chunk (one content file) in order, sharing heading ids and the sidebar tree.

    Returns the HTML of each chunk, the sidebar tree, and the id of each chunk's first heading.
    """
    ext = PrimerExtension(register, chapter_ids, anchor_label)
    md = markdown.Markdown(extensions=["tables", "sane_lists", "md_in_html", ext])
    out, first_ids = [], []
    for chunk in chunks:
        md.reset()
        out.append(md.convert(chunk))
        first_ids.append(ext.processor.first_id)
    return out, ext.processor.toc, first_ids


def convert(text: str, register: Register, chapter_ids: list[str]) -> tuple[str, list[TocEntry]]:
    htmls, toc, _ = convert_many([text], register, chapter_ids)
    return htmls[0], toc
