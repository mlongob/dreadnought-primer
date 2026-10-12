import pytest

from builder.rows import RowError, figure_html, parse_line, stack_html, validate

MIRROR = "**Sideboarding (61):** −1 Dreadnought, −2 Daze, −1 Thwart / +3 Annul, +2 Brain Freeze."
SURVIVAL = "**Sideboarding:** −2 Daze, −1 Thwart, −1 Brain Freeze, −1 Flash, −1 Peek / +3 Annul, +3 Flare."
WELDER = "**Welder/Tradewind:** as above plus −1 Flash / +2 Blue Elemental Blast; Welder is a red permanent."


def test_mirror_parses(reg):
    [r] = parse_line(MIRROR, reg)
    assert r.size == 61
    assert r.outs == [(1, "Phyrexian Dreadnought"), (2, "Daze"), (1, "Thwart")]
    assert r.ins == [(3, "Annul"), (2, "Brain Freeze")]


def test_default_size_is_sixty(reg):
    [r] = parse_line(SURVIVAL, reg)
    assert r.size == 60 and r.label == ""


def test_blasts_expand(reg):
    [r] = parse_line("**Sideboarding:** −1 Keg, −2 Flash, −1 Thwart, −1 Brain Freeze, −1 Peek, −1 Foil / +4 blasts, +3 Flare.", reg)
    assert r.ins == [(2, "Blue Elemental Blast"), (2, "Hydroblast"), (3, "Essence Flare")]


def test_ascii_minus_accepted(reg):
    [r] = parse_line("**Sideboarding:** -2 Daze / +2 Annul.", reg)
    assert r.outs == [(2, "Daze")]


def test_label_from_parentheses(reg):
    [r] = parse_line("**Sideboarding (GR):** −1 Brain Freeze, −1 Thwart, −1 Flash, −1 Opt, −2 Foil / +3 Annul, +2 Back to Basics, +1 Chain.", reg)
    assert r.label == "GR" and r.size == 60


def test_prose_row(reg):
    [r] = parse_line("**Sideboarding (GW):** the Terrageddon row, with Keg at 2 and Flare in mind for the third of lists that bring four Mage.", reg)
    assert r.prose and r.label == "GW" and r.outs == [] and r.ins == []


def test_two_rows_with_labels(reg):
    rs = parse_line("**Sideboarding:** UG and GW Madness: −1 Brain Freeze / +1 Chain. ZIMS: −1 Thwart, −1 Brain Freeze, −1 Peek, −1 Daze / +3 Annul, +1 Chain.", reg)
    assert [r.label for r in rs] == ["UG and GW Madness", "ZIMS"]
    assert rs[1].ins == [(3, "Annul"), (1, "Chain of Vapor")]


def test_delta_row(reg):
    [r] = parse_line(WELDER, reg)
    assert r.delta and r.label == "Welder/Tradewind"
    assert r.outs == [(1, "Flash of Insight")] and r.ins == [(2, "Blue Elemental Blast")]


def test_not_a_row(reg):
    assert parse_line("**Verdict.** Even.", reg) is None
    assert parse_line("Row your boat.", reg) is None


def test_unknown_card_in_row(reg):
    from builder.cards import UnknownCard
    with pytest.raises(UnknownCard):
        parse_line("**Sideboarding:** −1 Daze / +1 Black Lotus.", reg)


def test_validate_real_row_passes(reg, deck):
    validate(parse_line(MIRROR, reg), deck)


def test_validate_size_mismatch(reg, deck):
    [r] = parse_line("**Sideboarding:** −1 Daze / +2 Annul.", reg)
    with pytest.raises(RowError, match="61 cards, expected 60"):
        validate([r], deck)


def test_validate_too_many_out(reg, deck):
    [r] = parse_line("**Sideboarding:** −3 Daze / +3 Annul.", reg)
    with pytest.raises(RowError, match="takes out 3 Daze, main has 2"):
        validate([r], deck)


def test_validate_same_card_twice_counts_both(reg, deck):
    [r] = parse_line("**Sideboarding:** −2 Daze, −1 Daze / +3 Annul.", reg)
    with pytest.raises(RowError, match="takes out 3 Daze, main has 2"):
        validate([r], deck)


def test_validate_too_many_in(reg, deck):
    [r] = parse_line("**Sideboarding:** −4 Foil / +4 Annul.", reg)
    with pytest.raises(RowError, match="brings in 4 Annul, sideboard has 3"):
        validate([r], deck)


def test_validate_bringing_in_a_main_only_card(reg, deck):
    [r] = parse_line("**Sideboarding:** −1 Foil / +1 Stifle.", reg)
    with pytest.raises(RowError, match="brings in 1 Stifle, sideboard has 0"):
        validate([r], deck)


def test_delta_validates_cumulatively(reg, deck):
    rows = parse_line(SURVIVAL, reg) + parse_line(WELDER, reg)
    with pytest.raises(RowError, match="Welder/Tradewind.*61 cards, expected 60"):
        validate(rows, deck)


def test_delta_without_base_is_an_error(reg, deck):
    with pytest.raises(RowError, match="no row above"):
        validate(parse_line(WELDER, reg), deck)


def test_prose_rows_skip_validation(reg, deck):
    validate(parse_line("**Sideboarding (GW):** the Terrageddon row.", reg), deck)


def test_figure_draws_every_copy_without_badges(reg):
    [r] = parse_line(MIRROR, reg)
    html = figure_html(r, reg)
    assert html.count("<img") == 9
    assert ">Out<" in html and ">In<" in html and ">4<" in html and ">5<" in html
    assert "count" not in html


def test_figure_label_caption(reg):
    rs = parse_line("**Sideboarding:** UG and GW Madness: −1 Brain Freeze / +1 Chain. ZIMS: −1 Thwart / +1 Annul.", reg)
    assert "<figcaption>ZIMS</figcaption>" in figure_html(rs[1], reg)


def test_prose_row_has_no_figure(reg):
    [r] = parse_line("**Sideboarding (GW):** the Terrageddon row.", reg)
    assert figure_html(r, reg) == ""


def test_big_stack_tightens_but_each_copy_clears_the_border(reg):
    html = stack_html("Island", 17, reg)
    assert html.count("<img") == 17 and "--off:0.500rem" in html


def test_medium_stack_tightens_less(reg):
    assert "--off:0.690rem" in stack_html("Island", 6, reg)


def test_small_stack_default_offset(reg):
    html = stack_html("Stifle", 4, reg)
    assert "--off" not in html and 'title="4 × Stifle"' in html and 'alt="4 × Stifle"' in html


def test_problems_lists_every_bad_row(reg, deck):
    from builder.rows import problems
    rows = parse_line("**Sideboarding:** A: −1 Daze / +2 Annul. B: −3 Daze / +3 Annul.", reg)
    found = problems(rows, deck)
    assert [r.label for r, _ in found] == ["A", "B"]
    assert "takes out 3 Daze" in found[1][1]


def test_problems_empty_for_good_rows(reg, deck):
    from builder.rows import problems
    assert problems(parse_line(MIRROR, reg), deck) == []
