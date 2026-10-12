"""Build the page: content → validated, linked HTML → site/index.html with its assets."""
from __future__ import annotations

import hashlib
import re
import shutil
from dataclasses import dataclass, field, replace
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup

from . import lint
from .cards import Register, UnknownCard
from .deck import DeckError
from .deck import load as load_deck
from .pdf import PDF_NAME
from .directives import Context, DirectiveError, expand, load_combo
from .mdext import TocEntry, convert_many
from .outline import OutlineError
from .outline import load as load_outline
from .outline import split_front_matter
from .review import Change, mark
from .strings import strings
from .rows import problems
from .sbmap import MapError, sideboard_map

HERE = Path(__file__).resolve().parent
LEFTOVER_RE = re.compile(r"\{(card|cards|hand|decklist|combo|sideboard-map|nolink)\b|<!--sideboard-map-->")


class BuildError(Exception):
    pass


@dataclass
class BuildResult:
    html: str
    toc: list[TocEntry]
    warnings: list[lint.LintWarning] = field(default_factory=list)
    changes: list[Change] | None = None


def asset_version() -> str:
    """Changes whenever the stylesheet or script changes, so browsers never keep a stale copy."""
    data = (HERE / "static" / "style.css").read_bytes() + (HERE / "static" / "primer.js").read_bytes()
    return hashlib.sha256(data).hexdigest()[:10]


def inline_assets(html: str) -> str:
    """One self-contained file: the stylesheet and script inlined (card images still load from Scryfall)."""
    css = (HERE / "static" / "style.css").read_text()
    js = (HERE / "static" / "primer.js").read_text()
    html = re.sub(r'<link rel="stylesheet" href="assets/style\.css[^"]*">', lambda m: f"<style>{css}</style>", html)
    html = re.sub(r'<script src="assets/primer\.js[^"]*" defer></script>', lambda m: f"<script defer>{js}</script>", html)
    favicon = (HERE / "static" / "favicon.svg").read_text().replace('"', "'").replace("\n", "")
    return html.replace('href="assets/favicon.svg"', f'href="data:image/svg+xml,{favicon}"')


PENCIL = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
          'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20h4L19 9l-4-4L4 16v4z"/>'
          '<path d="M14 6l4 4"/></svg>')


def edit_link(html_text: str, heading_id: str, url: str, label: str) -> str:
    """A pencil after the section's # anchor, opening its Markdown file in GitHub's editor."""
    anchor = re.search(r'<a [^>]*class="anchor" href="#' + re.escape(heading_id) + r'"[^>]*>#</a>', html_text)
    if not anchor:
        return html_text
    pencil = (f'<a class="edit" href="{url}" aria-label="{label}" title="{label}" rel="noopener">{PENCIL}</a>')
    return html_text[:anchor.end()] + pencil + html_text[anchor.end():]


def render_page(title: str, subtitle: str, dateline: str, toc: list[TocEntry], body: str,
                description: str = "", share_image: str = "", site_url: str = "",
                changes: list[Change] | None = None, banner: bool = False,
                hero_art: str = "", hero_artist: str = "", pdf_name: str = "", repo_url: str = "") -> str:
    """The page template; everything but the body HTML is escaped."""
    env = Environment(loader=FileSystemLoader(HERE / "templates"), autoescape=True, keep_trailing_newline=True)
    return env.get_template("page.html.j2").render(
        title=title, subtitle=subtitle, dateline=dateline, toc=toc, body=Markup(body), version=asset_version(),
        description=description, share_image=share_image, site_url=site_url, changes=changes,
        t=strings(), banner=banner, hero_art=hero_art, hero_artist=hero_artist, pdf_name=pdf_name, repo_url=repo_url)


def build(root: Path, out: Path | None, review: dict[str, str] | None = None, *, preview: bool = False) -> BuildResult:
    """Build the page. With `review` (content path -> text at the approved state), build the review
    edition instead: every change marked in place, written to review.html."""
    root = Path(root)
    t = strings()
    changes: list[Change] | None = [] if review is not None else None
    try:
        register = Register.load(root / "data" / "cards.toml")
        deck = load_deck(root / "data" / "deck.toml", register)
        outline = load_outline(root)
        ctx = Context(register, deck, load_combo(root / "data" / "combo.toml"), t)
        rules = lint.load_rules(root / "data" / "lint.toml")

        warnings: list[lint.LintWarning] = []
        texts, matchups = [], []
        for source in outline.sources:
            warnings += lint.check(source, rules, source.slug in outline.stats_ok, register.names())
            if review is not None:
                base = review.get(str(source.path))
                base_body = split_front_matter(base, str(source.path))[1] if base is not None else None
                marked, found = mark(base_body, source.text, str(source.path), start=len(changes) + 1)
                changes += found
                source = replace(source, text=marked)
            expanded = expand(source, ctx)
            unverified = set(source.meta.get("unverified_rows", []))
            for row, message in problems(expanded.rows, deck):
                if row.label in unverified:
                    warnings.append(lint.LintWarning(source.path, 0, "row", f"{message} (listed in unverified_rows)"))
                else:
                    raise BuildError(f"{source.path}: {message}")
            if source.kind == "matchup":
                matchups.append((source, expanded.rows))
            texts.append(expanded.text)

        chapter_ids = [s.slug for s in outline.sources if s.kind == "chapter"]
        htmls, toc, first_ids = convert_many(texts, register, chapter_ids, t["link_to_section"])
        anchors = {s.slug: fid for s, fid in zip(outline.sources, first_ids) if s.kind == "matchup"}
        if outline.repo_url and not preview and review is None:
            htmls = [edit_link(h, fid, f"{outline.repo_url}/edit/main/{s.path}", t["edit_section"]) if fid else h
                     for h, s, fid in zip(htmls, outline.sources, first_ids)]
        body = "\n".join(htmls).replace("<!--sideboard-map-->", sideboard_map(matchups, anchors, t["map_headers"]))
    except (OutlineError, DeckError, DirectiveError, UnknownCard, MapError, ValueError) as e:
        raise BuildError(str(e)) from e

    leftover = LEFTOVER_RE.search(body)
    if leftover:
        raise BuildError(f"unrendered directive in the output: {body[leftover.start():leftover.start() + 60]!r}")

    if review is not None:
        current = {str(s.path) for s in outline.sources}
        changes += [Change("", "removed-file", path, "taken off the page") for path in sorted(review) if path not in current]
    share_image = register.get(outline.share_card).image("large") if outline.share_card else ""
    hero_art = register.get(outline.share_card).image("art_crop") if outline.share_card else ""
    html = render_page(outline.title, outline.subtitle, outline.dateline, toc, body,
                       outline.description, share_image, outline.site_url, changes, banner=preview,
                       hero_art=hero_art, hero_artist=outline.share_card_artist,
                       pdf_name="" if preview or review is not None else PDF_NAME,
                       repo_url="" if preview or review is not None else outline.repo_url)

    if out is not None:
        out = Path(out)
        out.mkdir(parents=True, exist_ok=True)
        name = "review" if review is not None else "preview" if preview else "index"
        (out / (name + ".html")).write_text(html)
        shutil.copytree(HERE / "static", out / "assets", dirs_exist_ok=True)
    return BuildResult(html, toc, warnings, changes)
