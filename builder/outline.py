"""outline.toml: page metadata and the order of chapters and matchups."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


class OutlineError(Exception):
    pass


@dataclass
class Source:
    path: Path            # relative to the repo root, e.g. content/matchups/mirror.md
    text: str             # file text without front matter
    kind: str             # "chapter" or "matchup"
    slug: str
    meta: dict = field(default_factory=dict)
    line_offset: int = 0  # lines of front matter removed, for error line numbers


@dataclass
class Outline:
    title: str
    subtitle: str
    dateline: str
    sources: list[Source]
    stats_ok: set[str]
    description: str = ""
    share_card: str = ""
    site_url: str = ""
    share_card_artist: str = ""
    repo_url: str = ""


def split_front_matter(text: str, rel: str) -> tuple[dict, str, int]:
    if not text.startswith("+++\n"):
        return {}, text, 0
    end = text.find("\n+++\n", 4)
    if end < 0:
        raise OutlineError(f"{rel}: front matter opened with +++ is never closed")
    try:
        meta = tomllib.loads(text[4:end])
    except tomllib.TOMLDecodeError as e:
        raise OutlineError(f"{rel}: front matter: {e}") from e
    body = text[end + 5:]
    return meta, body, text[: end + 5].count("\n")


def _check_unique(names: list[str]) -> None:
    seen = set()
    for n in names:
        if n in seen:
            raise OutlineError(f"outline.toml: {n!r} appears twice")
        seen.add(n)


def load(root: Path) -> Outline:
    root = Path(root)
    data = tomllib.loads((root / "outline.toml").read_text())
    chapters, matchups = list(data.get("chapters", [])), list(data.get("matchups", []))
    _check_unique(chapters)
    _check_unique(matchups)
    if matchups and "matchups" not in chapters:
        raise OutlineError("outline.toml lists matchups but has no 'matchups' chapter to put them in")

    def read(slug: str, kind: str) -> Source:
        rel = f"content/{slug}.md" if kind == "chapter" else f"content/matchups/{slug}.md"
        path = root / rel
        if not path.exists():
            raise OutlineError(f"outline lists {slug!r} but {rel} does not exist")
        meta, text, offset = split_front_matter(path.read_text(), rel)
        prefix = "## " if kind == "chapter" else "### "
        if not text.startswith(prefix):
            raise OutlineError(f"{rel} must start with a {prefix!r} heading")
        return Source(Path(rel), text, kind, slug, meta, offset)

    sources = []
    for slug in chapters:
        sources.append(read(slug, "chapter"))
        if slug == "matchups":
            sources += [read(m, "matchup") for m in matchups]

    listed = {str(s.path) for s in sources}
    for path in sorted((root / "content").rglob("*.md")):
        rel = str(path.relative_to(root))
        if rel not in listed:
            raise OutlineError(f"{rel} is not in outline.toml")

    return Outline(data.get("title", ""), data.get("subtitle", ""), data.get("dateline", ""),
                   sources, set(data.get("stats_ok", [])), data.get("description", ""),
                   data.get("share_card", ""), data.get("site_url", ""),
                   data.get("share_card_artist", ""), data.get("repo_url", ""))
