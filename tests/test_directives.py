import re
from pathlib import Path

import pytest

from builder.directives import Context, DirectiveError, expand, load_combo
from builder.outline import Source
from conftest import ROOT


@pytest.fixture(scope="module")
def ctx(register, deck):
    return Context(register, deck, load_combo(ROOT / "data" / "combo.toml"))


def src(text, offset=0):
    return Source(Path("content/x.md"), text, "chapter", "x", {}, offset)


def test_single_card_becomes_margin_figure(ctx):
    out = expand(src("## X\n\n{card: Stifle}\nThe enabler.\n"), ctx).text
    assert '<figure class="margin-card"><img class="mtg"' in out
    assert 'alt="Stifle"' in out


def test_figure_directly_followed_by_paragraph_is_separated(ctx):
    out = expand(src("## X\n\n{card: Stifle}\nThe enabler.\n"), ctx).text
    assert re.search(r"</figure>\n\n+The enabler\.", out)


def test_card_row(ctx):
    out = expand(src("## X\n\n{cards: Wasteland | Dust Bowl | Rishadan Port | Back to Basics}\n"), ctx).text
    assert out.count("<img") == 4 and '<div class="cardrow">' in out


def test_card_names_with_commas(ctx):
    out = expand(src("## X\n\n{cards: Akroma, Angel of Wrath}\n"), ctx).text
    assert 'alt="Akroma, Angel of Wrath"' in out


def test_five_cards_is_an_error_with_location(ctx):
    with pytest.raises(DirectiveError, match=r"content/x.md:5: \{cards:\} takes at most four cards, got 5"):
        expand(src("## X\n\n{cards: Opt | Peek | Gush | Daze | Foil}\n", offset=2), ctx)


def test_unknown_card_is_an_error_with_location_and_hint(ctx):
    with pytest.raises(DirectiveError, match=r"content/x.md:3: .*Black Lotus.*tools/add_card.py"):
        expand(src("## X\n\n{card: Black Lotus}\n"), ctx)


def test_hand_needs_seven(ctx):
    out = expand(src("## X\n\n{hand: Peek | Island | Phyrexian Dreadnought | Daze | Island | Stifle | Opt}\n"), ctx).text
    assert '<div class="hand">' in out and out.count("<img") == 7
    with pytest.raises(DirectiveError, match="seven"):
        expand(src("## X\n\n{hand: Peek | Island}\n"), ctx)


def test_decklist_draws_the_75(ctx):
    out = expand(src("## X\n\n{decklist}\n"), ctx).text
    assert out.count("<img") == 75
    assert "Main deck, 60" in out and "Sideboard, 15" in out


def test_combo_figure_is_eager(ctx):
    out = expand(src("## X\n\n{combo}\n"), ctx).text
    assert '<figure class="combo">' in out and out.count('loading="eager"') == 3
    assert "<b>Stifle the trigger</b>" in out and ">then<" in out and ">or<" in out


def test_sideboard_map_placeholder(ctx):
    assert "<!--sideboard-map-->" in expand(src("## X\n\n{sideboard-map}\n"), ctx).text


def test_row_line_kept_and_figure_appended(ctx):
    line = "**Sideboarding (61):** −1 Dreadnought, −2 Daze, −1 Thwart / +3 Annul, +2 Brain Freeze."
    result = expand(src(f"### M\n\n{line}\n\nNext.\n"), ctx)
    assert line in result.text
    assert result.text.index(line) < result.text.index('<figure class="sbrow">')
    assert len(result.rows) == 1 and result.rows[0].size == 61


def test_unknown_directive_is_an_error(ctx):
    with pytest.raises(DirectiveError, match=r"content/x.md:3: unknown directive \{foo\}"):
        expand(src("## X\n\n{foo}\n"), ctx)


def test_inline_nolink_left_for_markdown(ctx):
    text = "## X\n\n{nolink: Replenish} is a deck.\n"
    assert expand(src(text), ctx).text == text


def test_decklist_splits_the_islands_into_piles(ctx):
    out = expand(src("## X\n\n{decklist}\n"), ctx).text
    piles = re.findall(r'<div class="stack" title="(\d+) × Island"', out)
    assert [int(n) for n in piles] == [4, 4, 4, 4, 1]
    assert out.count('alt="17 × Island"') == 1


def test_puzzle_block_becomes_a_board(ctx):
    text = ('## X\n\n{puzzle}\nturn = 3\nactive = "you"\nphase = "main1"\n[them]\nlife = 20\nlibrary = 50\n'
            'hand = ["?"]\n[you]\nlife = 20\nlibrary = 49\nhand = ["Stifle"]\n{/puzzle}\n\nWhat do you do?\n')
    out = expand(src(text), ctx).text
    assert '<figure class="puzzle">' in out and "{puzzle}" not in out and 'turn = 3' not in out


def test_answer_block_is_a_spoiler(ctx):
    out = expand(src("## X\n\n{answer}\nStifle it.\n{/answer}\n"), ctx).text
    assert '<details class="pz-answer" markdown="1">' in out and "</details>" in out and "Stifle it." in out


def test_unclosed_puzzle_fails(ctx):
    with pytest.raises(DirectiveError, match="puzzle"):
        expand(src("## X\n\n{puzzle}\nturn = 1\n"), ctx)
