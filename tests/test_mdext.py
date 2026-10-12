import re

import pytest

from builder.cards import UnknownCard
from builder.mdext import convert


def links(html):
    return html.count('class="cardref"')


def test_first_mention_only(reg):
    html, _ = convert("## A\n\nDreadnought and Dreadnought.\n\nPhyrexian Dreadnought again.", reg, ["a"])
    assert links(html) == 1


def test_new_section_resets(reg):
    html, _ = convert("## A\n\nStifle.\n\n### B\n\nStifle.", reg, ["a"])
    assert links(html) == 2


def test_link_markup(reg):
    html, _ = convert("## A\n\nStifle.", reg, ["a"])
    c = reg.get("Stifle")
    a = re.search(r'<a [^>]*>Stifle</a>', html).group(0)
    for attr in ('class="cardref"', f'href="{c.page}"', 'data-card="Stifle"', f'data-img="{c.id}"'):
        assert attr in a


def test_longest_name_wins(reg):
    html, _ = convert("## A\n\nVision Charm.", reg, ["a"])
    assert ">Vision Charm</a>" in html


def test_plural(reg):
    html, _ = convert("## A\n\nStifles.", reg, ["a"])
    assert ">Stifles</a>" in html


def test_possessive(reg):
    html, _ = convert("## A\n\nthe Dreadnought's trigger", reg, ["a"])
    assert ">Dreadnought</a>'s" in html


def test_not_inside_words(reg):
    html, _ = convert("## A\n\nOptional Gushing", reg, ["a"])
    assert links(html) == 0


def test_lowercase_is_not_a_card(reg):
    html, _ = convert("## A\n\na flash of insight", reg, ["a"])
    assert links(html) == 0


def test_not_in_headings(reg):
    html, _ = convert("## Stifle\n\n### Gush (4)\n\ntext", reg, ["a"])
    assert links(html) == 0


def test_not_in_table_header_but_in_cells(reg):
    html, _ = convert("## A\n\n| Opt | x |\n|---|---|\n| Peek | y |", reg, ["a"])
    assert "cardref" not in html.split("</thead>")[0]
    assert ">Peek</a>" in html


def test_inside_list_items_and_emphasis(reg):
    html, _ = convert("## A\n\n- with **Foil** up\n- *Daze* too", reg, ["a"])
    assert ">Foil</a>" in html and ">Daze</a>" in html


def test_nolink(reg):
    html, _ = convert("## A\n\nThe {nolink: Gush} deck. Gush the card.", reg, ["a"])
    assert '<span class="nolink">Gush</span>' in html
    assert links(html) == 1


def test_forced_link_counts_as_mention(reg):
    html, _ = convert("## A\n\nan [Edict]{Chainer's Edict} and Chainer's Edict", reg, ["a"])
    assert links(html) == 1 and ">Edict</a>" in html


def test_forced_link_unknown_card(reg):
    with pytest.raises(UnknownCard):
        convert("## A\n\nan [Edict]{Nonexistent Edict}", reg, ["a"])


def test_markdown_links_untouched(reg):
    html, _ = convert("## A\n\nsee [the Stifle guide](https://example.com)", reg, ["a"])
    assert links(html) == 0


def test_raw_html_untouched(reg):
    html, _ = convert('## A\n\n<div class="cardrow"><img alt="Stifle"></div>\n\nStifle.', reg, ["a"])
    assert links(html) == 1


def test_heading_ids_and_toc(reg):
    html, toc = convert("## What this deck is\n\n### Opt (4), Impulse (2), Peek (1)\n\n## Matchups\n\n### The mirror", reg,
                        ["what-this-deck-is", "matchups"])
    assert '<h2 id="what-this-deck-is">' in html and '<h3 id="opt-impulse-peek">' in html
    assert [(t.id, t.label) for t in toc] == [("what-this-deck-is", "What this deck is"), ("matchups", "Matchups")]
    assert toc[0].children[0].label == "Opt, Impulse, Peek"
    assert toc[1].children[0].id == "the-mirror"


def test_duplicate_h3_ids(reg):
    _, toc = convert("## A\n\n### Brain Freeze (1 main, 2 side)\n\n## B\n\n### Brain Freeze (2)", reg, ["a", "b"])
    assert [c.id for t in toc for c in t.children] == ["brain-freeze", "brain-freeze-2"]
    assert toc[0].children[0].label == "Brain Freeze"


def test_parenthetical_without_digits_kept_in_label(reg):
    _, toc = convert("## A\n\n### Survival shells (GW, BG Rock, Welder/Tradewind)", reg, ["a"])
    assert toc[0].children[0].label == "Survival shells (GW, BG Rock, Welder/Tradewind)"
    assert toc[0].children[0].id == "survival-shells"


def test_more_h2_than_chapters_is_an_error(reg):
    with pytest.raises(ValueError, match="more '## ' headings than chapters"):
        convert("## A\n\n## B", reg, ["a"])


def test_deck_names_are_not_auto_linked(reg):
    html, _ = convert("## A\n\nAgainst Stasis and Replenish lists.", reg, ["a"])
    assert links(html) == 0


def test_deck_names_can_be_forced(reg):
    html, _ = convert("## A\n\nunder [Stasis]{Stasis}", reg, ["a"])
    assert links(html) == 1


def test_heading_label_resolves_entities_and_escapes(reg):
    _, toc = convert("## A\n\n### 1\\. Stifle &mdash; Daze", reg, ["a"])
    entry = toc[0].children[0]
    assert entry.label == "1. Stifle — Daze"
    assert "\x02" not in entry.id and "wzxhzdk" not in entry.id


def test_h3_id_never_takes_a_chapter_or_page_id(reg):
    _, toc = convert("## A\n\n### B\n\n### Top\n\n## B", reg, ["a", "b"])
    assert [c.id for c in toc[0].children] == ["b-2", "top-2"]
    assert toc[1].id == "b"


def test_convert_many_reports_each_chunks_first_heading(reg):
    from builder.mdext import convert_many
    htmls, toc, first_ids = convert_many(["## Matchups\n\n### How to read these", "### The mirror\n\ntext", "### Sligh"],
                                         reg, ["matchups"])
    assert first_ids == ["matchups", "the-mirror", "sligh"]
    assert len(htmls) == 3 and [c.id for c in toc[0].children] == ["how-to-read-these", "the-mirror", "sligh"]


def test_forced_link_after_a_mention_stays_plain(reg):
    html, _ = convert("## A\n\nOath of Druids, then an [Oath]{Oath of Druids} trigger.", reg, ["a"])
    assert links(html) == 1 and "an Oath trigger" in html


def test_headings_carry_a_copy_link_anchor(reg):
    html, toc = convert("## A\n\n### The mirror", reg, ["a"])
    assert '<h3 id="the-mirror">The mirror<a aria-label="Link to this section" class="anchor" href="#the-mirror">#</a></h3>' in html
    assert toc[0].children[0].label == "The mirror"
