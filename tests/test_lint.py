from pathlib import Path

import pytest

from builder.lint import check, load_rules
from builder.outline import Source
from conftest import ROOT


@pytest.fixture(scope="module")
def rules():
    return load_rules(ROOT / "data" / "lint.toml")


def warn(rules, text, stats_ok=False, offset=0):
    return check(Source(Path("content/x.md"), text, "chapter", "x", {}, offset), rules, stats_ok)


def test_british_spelling_warns_with_suggestion(rules):
    [w] = warn(rules, "## X\n\nA favourable matchup.\n")
    assert w.rule == "spelling" and w.line == 3 and "favorable" in w.text


def test_spelling_variants_and_case(rules):
    assert len(warn(rules, "Colours and Prioritised lines.\n")) == 2


def test_us_spelling_is_fine(rules):
    assert warn(rules, "A favorable matchup in color.\n") == []


def test_percentage_in_prose_warns(rules):
    [w] = warn(rules, "It wins 35% of the time.\n")
    assert w.rule == "stats"


def test_percentage_in_table_is_fine(rules):
    assert warn(rules, "| Opt | 71% |\n") == []


def test_percentage_allowed_in_stats_chapters(rules):
    assert warn(rules, "It wins 35% of the time.\n", stats_ok=True) == []


def test_counting_matchups_warns(rules):
    assert [w.rule for w in warn(rules, "Twelve of the mapped decks run it.\n")] == ["stats"]


def test_corrected_claim_warns(rules):
    [w] = warn(rules, "Portent is an instant, so hold it.\n")
    assert w.rule == "claim" and "sorcery" in w.text


def test_correct_claim_is_fine(rules):
    assert warn(rules, "Portent is a sorcery.\n") == []


def test_line_numbers_include_front_matter(rules):
    [w] = warn(rules, "A favourable matchup.\n", offset=4)
    assert w.line == 5


def test_directive_lines_skipped(rules):
    assert warn(rules, "{cards: Favourable Winds | Colour Thing}\n") == []


def test_card_names_keep_their_printed_spelling(rules):
    src = Source(Path("content/x.md"), "Colourful Grid adds three.\n", "chapter", "x", {}, 0)
    assert check(src, rules, False, card_names=["Colourful Grid"]) == []


def test_one_warning_per_word_with_full_suggestion(rules):
    [w] = warn(rules, "unfavourable, favourably\n")[:1]
    assert "'unfavorable'" in w.text
    assert len(warn(rules, "unfavourable, favourably\n")) == 2


def test_warning_without_line_omits_it():
    from builder.lint import LintWarning
    assert str(LintWarning(Path("content/a.md"), 0, "row", "msg")) == "content/a.md: row: msg"
    assert str(LintWarning(Path("content/a.md"), 3, "row", "msg")) == "content/a.md:3: row: msg"
