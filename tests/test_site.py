"""Builds the real content once and checks the page as a whole."""
import re

import pytest

from builder.outline import load as load_outline
from builder.render import build
from conftest import ROOT


@pytest.fixture(scope="module")
def result():
    return build(ROOT, None)


@pytest.fixture(scope="module")
def outline():
    return load_outline(ROOT)


def toc_hrefs(html):
    nav = re.search(r'<nav class="toc".*?</nav>', html, re.S).group(0)
    return [h for h in re.findall(r'href="#([^"]+)"', nav) if h != "top"]


def test_builds(result):
    assert "<main" in result.html


def test_dark_default(result):
    assert '<html lang="en-US" data-theme="dark">' in result.html


def test_title_block(result):
    assert "<h1>Mono-Blue Dreadnought</h1>" in result.html and "Version 0.2 · October 2026" in result.html


def test_every_toc_link_resolves(result):
    ids = set(re.findall(r'\sid="([^"]+)"', result.html))
    assert [h for h in toc_hrefs(result.html) if h not in ids] == []


def test_every_heading_in_toc(result):
    assert set(re.findall(r'<h[23] id="([^"]+)"', result.html)) == set(toc_hrefs(result.html))


def test_all_chapters_and_matchups_in_toc(result, outline):
    assert len(result.toc) == sum(1 for s in outline.sources if s.kind == "chapter")
    matchups = next(e for e in result.toc if e.id == "matchups")
    assert len(matchups.children) == sum(1 for s in outline.sources if s.kind == "matchup")


def test_no_directive_left(result):
    assert not re.search(r"\{(card|cards|hand|decklist|combo|sideboard-map|nolink)\b", result.html)
    assert "<!--sideboard-map-->" not in result.html


def map_lines(outline):
    return sum(1 for src in outline.sources for e in src.meta.get("map", []) if not e.get("omit"))


def test_sideboard_map_has_every_row(result, outline):
    table = re.search(r'<table class="sbmap">.*?</table>', result.html, re.S).group(0)
    assert table.count("<tr>") == 1 + map_lines(outline)


def test_cards_are_linked(result):
    assert result.html.count('class="cardref"') > 200


def test_images_present(result):
    assert result.html.count('<img class="mtg"') > 400


def site_copy(tmp_path):
    import shutil
    for name in ("content", "data"):
        shutil.copytree(ROOT / name, tmp_path / name)
    shutil.copy(ROOT / "outline.toml", tmp_path / "outline.toml")
    return tmp_path


def test_unverified_row_is_a_warning(tmp_path):
    root = site_copy(tmp_path)
    mirror = root / "content" / "matchups" / "mirror.md"
    text = mirror.read_text().replace("+++\n", '+++\nunverified_rows = ["Odd"]\n', 1)
    mirror.write_text(text + "\n**Sideboarding (Odd):** −1 Daze / +2 Annul.\n")
    meta_fix = mirror.read_text().replace('label = "Mono-Blue Dreadnought mirror (61)"\n', 'label = "Mono-Blue Dreadnought mirror (61)"\n\n[[map]]\nlabel = "Odd"\nomit = true\n', 1)
    mirror.write_text(meta_fix)
    result = build(root, None)
    assert any(w.rule == "row" and "'Odd' leaves 61 cards" in w.text for w in result.warnings)


def test_invalid_row_not_listed_fails_the_build(tmp_path):
    from builder.render import BuildError
    root = site_copy(tmp_path)
    mirror = root / "content" / "matchups" / "mirror.md"
    mirror.write_text(mirror.read_text() + "\n**Sideboarding (Odd):** −1 Daze / +2 Annul.\n")
    with pytest.raises(BuildError, match="leaves 61 cards"):
        build(root, None)


def test_footer_credits(result):
    assert "Wizards of the Coast" in result.html and "Scryfall" in result.html


def test_assets_written(tmp_path):
    build(ROOT, tmp_path)
    assert (tmp_path / "index.html").exists()
    assert (tmp_path / "assets" / "style.css").exists() and (tmp_path / "assets" / "primer.js").exists()


def test_page_escapes_labels():
    from builder.mdext import TocEntry
    from builder.render import render_page
    html = render_page("T", "S", "D", [TocEntry(2, "a", 'Say "hi" <b>', [TocEntry(3, "b", "x")])], "<p>body</p>")
    assert 'Say &#34;hi&#34; &lt;b&gt;' in html or "Say &quot;hi&quot; &lt;b&gt;" in html
    assert "<p>body</p>" in html


def test_sideboard_map_links_point_at_their_matchups(result):
    table = re.search(r'<table class="sbmap">.*?</table>', result.html, re.S).group(0)
    assert '<a href="#dreadnought-mirror">Mono-Blue Dreadnought mirror (61)</a>' in table
    assert '<a href="#full-english-breakfast">Full English Breakfast</a>' in table


def test_assets_are_cache_busted_by_content(result):
    import hashlib
    css = (ROOT / "builder" / "static" / "style.css").read_bytes()
    js = (ROOT / "builder" / "static" / "primer.js").read_bytes()
    v = hashlib.sha256(css + js).hexdigest()[:10]
    assert f'href="assets/style.css?v={v}"' in result.html
    assert f'src="assets/primer.js?v={v}"' in result.html


def test_share_previews(result):
    from builder.cards import Register
    dn = Register.load(ROOT / "data" / "cards.toml").get("Phyrexian Dreadnought")
    assert f'<meta property="og:image" content="{dn.image("art_crop")}">' in result.html
    assert '<meta property="og:title" content="Mono-Blue Dreadnought — A Premodern primer">' in result.html
    assert '<meta property="og:description" content="' in result.html and '<meta name="description" content="' in result.html
    assert '<meta name="twitter:card" content="summary_large_image">' in result.html


def test_favicon(result):
    assert '<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">' in result.html
    assert (ROOT / "builder" / "static" / "favicon.svg").exists()


def test_every_heading_has_an_anchor(result):
    heads = re.findall(r'<h([23]) id="([^"]+)">(.*?)</h\1>', result.html, re.S)
    assert heads and all(f'href="#{hid}">#</a>' in inner for lvl, hid, inner in heads)


def current_texts(root):
    return {str(p.relative_to(root)): p.read_text() for p in (root / "content").rglob("*.md")}


def test_review_edition_with_no_changes():
    result = build(ROOT, None, review=current_texts(ROOT))
    assert result.changes == []
    assert "No changes since the last approved version" in result.html


def test_review_edition_marks_an_edit(tmp_path):
    root = site_copy(tmp_path)
    base = current_texts(root)
    sligh = root / "content" / "matchups" / "sligh.md"
    sligh.write_text(sligh.read_text().replace("Very favorable in game one", "Favorable in game one", 1))
    result = build(root, None, review=base)
    assert [c.kind for c in result.changes] == ["edit"]
    assert "<del>Very favorable</del><ins>Favorable</ins>" in result.html
    assert 'href="#change-1"' in result.html


def test_review_edition_lists_removed_files(tmp_path):
    root = site_copy(tmp_path)
    base = current_texts(root)
    base["content/matchups/removed-deck.md"] = "### Removed deck\n\nText."
    result = build(root, None, review=base)
    assert any(c.kind == "removed-file" and c.path == "content/matchups/removed-deck.md" for c in result.changes)


def test_review_edition_never_leaks_directive_syntax(tmp_path):
    root = site_copy(tmp_path)
    base = current_texts(root)
    mirror = root / "content" / "matchups" / "mirror.md"
    mirror.write_text(mirror.read_text().replace("{cards: Phyrexian Dreadnought | Brain Freeze | Annul | Powder Keg}\n", "", 1))
    result = build(root, None, review=base)
    assert any(c.kind == "remove" for c in result.changes)


@pytest.fixture(scope="module")
def preview():
    return build(ROOT, None, preview=True)


def test_preview_has_the_confidential_banner(preview):
    assert "Confidential — for your eyes only" in preview.html


def test_preview_keeps_finished_matchups_and_the_map(preview, outline):
    assert "The golden rule." in preview.html
    table = re.search(r'<table class="sbmap">.*?</table>', preview.html, re.S).group(0)
    assert table.count("<tr>") == 1 + map_lines(outline)


def test_normal_build_has_no_banner(result):
    assert "Confidential" not in result.html


def test_print_contents_lists_every_chapter_and_section(result):
    toc = re.search(r'<nav class="print-toc".*?</nav>', result.html, re.S).group(0)
    hrefs = re.findall(r'href="#([^"]+)"', toc)
    assert set(hrefs) == set(toc_hrefs(result.html))


def test_standalone_page_inlines_its_assets(result):
    from builder.render import inline_assets
    page = inline_assets(result.html)
    assert 'href="assets/style.css' not in page and 'src="assets/primer.js' not in page
    assert "<style>" in page and "--measure" in page and "data-theme-toggle" in page


def test_footer_licence(result):
    assert 'href="https://creativecommons.org/licenses/by/4.0/"' in result.html
    assert "Mario Longobardi" in result.html


def test_title_shows_the_dreadnought_art_uncropped_with_credit(result):
    header = re.search(r'<header class="title">.*?</header>', result.html, re.S).group(0)
    assert re.search(r'<img [^>]*src="https://cards\.scryfall\.io/art_crop/front/7/b/7b8197b9-[^"]+\.jpg"', header)
    assert "Pete Venters" in header
    assert '<p class="standfirst">' in header


def test_unfinished_matchups_say_coming_soon(result):
    assert "Coming soon." in result.html


def test_each_chapter_and_matchup_links_to_its_file_on_github(result):
    edit = "https://github.com/mlongob/dreadnought-primer/edit/main/"
    foreword = re.search(r'<h2 id="foreword".*?</h2>', result.html, re.S).group(0)
    assert f'href="{edit}content/foreword.md"' in foreword
    sligh = re.search(r'<h3 id="sligh".*?</h3>', result.html, re.S).group(0)
    assert f'href="{edit}content/matchups/sligh.md"' in sligh


def test_the_sidebar_links_the_repository(result):
    assert 'class="repo-button" href="https://github.com/mlongob/dreadnought-primer"' in result.html


def test_preview_has_no_edit_links(preview):
    assert "/edit/main/" not in preview.html


def test_link_previews_show_the_art_not_the_whole_card(result):
    image = re.search(r'<meta property="og:image" content="([^"]+)"', result.html).group(1)
    assert "/art_crop/" in image
    assert '<meta name="twitter:card" content="summary_large_image">' in result.html


def test_board_overlays_let_clicks_through_to_the_card():
    css = (ROOT / "builder" / "static" / "style.css").read_text()
    for selector in (".pz-phased::before", ".pz-stackitems::before"):
        rule = re.search(re.escape(selector) + r"\s*\{([^}]*)\}", css).group(1)
        assert "pointer-events: none" in rule, selector
