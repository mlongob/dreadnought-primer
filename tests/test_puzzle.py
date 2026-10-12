import html
import re

import pytest

from builder.puzzle import PuzzleError, parse_entry, render
from conftest import ROOT
from builder.cards import Register

reg = Register.load(ROOT / "data" / "cards.toml")

BOARD = """
turn = 6
active = "them"
phase = "end"
[them]
life = 14
library = 31
hand = ["?", "?", "Counterspell"]
lands = ["Island (tapped)", "Underground River"]
permanents = ["Psychatog", "Powder Keg [1]"]
graveyard = ["Gush", "Opt"]
[you]
life = 17
library = 28
hand = ["Phyrexian Dreadnought", "Stifle (seen)", "Island"]
lands = ["Island", "Island (tapped)"]
graveyard = ["Flash of Insight"]
"""


def test_entry_annotations():
    e = parse_entry("Powder Keg [2] (tapped)", reg)
    assert (e.card.name, e.counters, e.tapped, e.seen) == ("Powder Keg", 2, True, False)
    assert parse_entry("Stifle (seen)", reg).seen
    assert parse_entry("?", reg).card is None


def test_unknown_card_fails():
    with pytest.raises(Exception):
        parse_entry("Not A Card", reg)


def test_opponent_hand_shows_backs_and_revealed_cards_with_an_eye():
    out = render(BOARD, reg)
    them = re.search(r'<div class="pz-side pz-them">.*?<div class="pz-side pz-you">', out, re.S).group(0)
    hand = re.search(r'<div class="pz-hand">.*?</div>', them, re.S).group(0)
    assert hand.count('class="pz-back"') == 2
    assert 'data-card="Counterspell"' in hand and "pz-seen" in hand


def test_your_seen_card_has_the_eye():
    out = render(BOARD, reg)
    you = out[out.index('<div class="pz-side pz-you">'):]
    stifle = re.search(r'<span class="pz-card[^"]*"[^>]*>(?:(?!</span>).)*data-card="Stifle"', you, re.S).group(0)
    assert "pz-seen" in stifle


def test_tapped_counters_and_counts():
    out = render(BOARD, reg)
    assert 'pz-tapped' in out
    assert '<span class="pz-counter">1</span>' in out
    assert ">31<" in out and ">28<" in out and ">14<" in out and ">17<" in out


def test_turn_bar_sits_between_the_battlefields_and_points_at_the_active_player():
    out = render(BOARD, reg)
    assert out.index('pz-side pz-them') < out.index('<div class="pz-turn') < out.index('pz-side pz-you')
    bar = re.search(r'<div class="pz-turn[^"]*">.*?</ol>', out, re.S).group(0)
    assert bar.startswith('<div class="pz-turn pz-active-them">')
    assert re.search(r"Turn</small><b>6</b>", bar) and "pz-player" not in bar
    assert re.search(r'<li class="pz-phase current"[^>]*>End', bar)
    assert '<div class="pz-turn pz-active-you">' in render(BOARD.replace('active = "them"', 'active = "you"'), reg)


def test_bad_phase_fails():
    with pytest.raises(PuzzleError):
        render(BOARD.replace('phase = "end"', 'phase = "lunch"'), reg)


def test_phased_out_entry():
    e = parse_entry("Phyrexian Dreadnought (phased out)", reg)
    assert e.phased and not e.tapped
    out = render(BOARD.replace('lands = ["Island", "Island (tapped)"]', 'lands = ["Island"]\npermanents = ["Phyrexian Dreadnought (phased out)"]'), reg)
    assert "pz-phased" in out and "Phased out" in out


def test_big_graveyard_shows_every_card_in_overlapping_rows_of_six():
    big = BOARD.replace('graveyard = ["Flash of Insight"]', "graveyard = [" + ", ".join(['"Opt"'] * 34 + ['"Gush"']) + "]")
    out = render(big, reg)
    you = out[out.index('<div class="pz-side pz-you">'):]
    grave = re.search(r'<div class="pz-graveyard">.*?</div></div></div>', you, re.S).group(0)
    rows = re.findall(r'<div class="pz-pilerow">(.*?)</div>', grave, re.S)
    assert [r.count('class="pz-card') for r in rows] == [6, 6, 6, 6, 6, 5]
    assert "<details" not in grave and "Graveyard (35)" in grave
    assert rows[-1].rstrip().endswith("</span>") and 'data-card="Gush"' in rows[-1]


def test_lands_stack_in_fours_by_name_with_tapped_stacks_on_the_right():
    lands = ['"Island"'] * 9 + ['"Island (tapped)"'] * 5 + ['"Plains"'] * 2 + ['"Mishra\'s Factory (tapped)"'] + ['"Adarkar Wastes"'] * 3
    out = render(BOARD.replace('lands = ["Island", "Island (tapped)"]', "lands = [" + ", ".join(lands) + "]"), reg)
    you = out[out.index('<div class="pz-side pz-you">'):]
    row = re.search(r'<div class="pz-row pz-lands">(.*?)</div>', you, re.S).group(1)
    stacks = re.findall(r'<span class="pz-stack( pz-stack-tapped)?" data-n="(\d)">.*?data-card="([^"]+)"', row, re.S)
    assert [(bool(t), int(n), html.unescape(name)) for t, n, name in stacks] == [
        (False, 4, "Island"), (False, 4, "Island"), (False, 1, "Island"), (False, 2, "Plains"), (False, 3, "Adarkar Wastes"),
        (True, 4, "Island"), (True, 1, "Island"), (True, 1, "Mishra's Factory")]


STACK = BOARD.replace("[them]", '''
storm = 3
[[stack]]
card = "Powder Keg"
by = "them"
ability = "Destroy each artifact and creature with mana value 1."
kind = "activated"
[[stack]]
card = "Stifle"
by = "you"
target = "Powder Keg's ability"
[[stack]]
card = "Counterspell"
by = "them"
target = "Stifle"

[them]''', 1)


def test_no_stack_and_no_storm_unless_the_puzzle_has_them():
    out = render(BOARD, reg)
    assert "pz-stackzone" not in out and "Storm" not in out


def test_stack_runs_bottom_to_top_left_to_right_and_leans_towards_whoever_put_it_there():
    out = render(STACK, reg)
    zone = re.search(r'<div class="pz-stackzone[^"]*">.*?</ol></div>', out, re.S).group(0)
    items = re.findall(r'<li class="pz-item pz-by-(them|you)( pz-ability)?"', zone)
    assert items == [("them", " pz-ability"), ("you", ""), ("them", "")]
    assert out.index("pz-stackzone") < out.index('<div class="pz-turn')
    assert "Stifle" in zone and "Powder Keg&#x27;s ability" in zone


def test_an_ability_shows_its_source_art_and_its_text():
    out = render(STACK, reg)
    keg = re.search(r'<li class="pz-item pz-by-them pz-ability".*?</li>', out, re.S).group(0)
    assert "/art_crop/" in keg and "Powder Keg" in keg
    assert "Destroy each artifact and creature with mana value 1." in keg


def test_storm_count_sits_in_the_turn_bar():
    out = render(STACK, reg)
    bar = re.search(r'<div class="pz-turn[^"]*">.*?</div>', out, re.S).group(0)
    assert re.search(r'<small>Storm</small><b>3</b>', bar)


def test_stack_entry_needs_a_player():
    with pytest.raises(PuzzleError):
        render(STACK.replace('by = "you"', 'by = "me"'), reg)


def test_room_for_target_notes_only_when_an_item_has_a_target():
    assert '<div class="pz-stackzone pz-has-targets">' in render(STACK, reg)
    plain = STACK.replace('target = "Powder Keg\'s ability"\n', "").replace('target = "Stifle"\n', "")
    assert '<div class="pz-stackzone">' in render(plain, reg)


def test_attacking_creatures_get_an_arrow():
    e = parse_entry("Goblin Piledriver (tapped) (attacking)", reg)
    assert e.attacking and e.tapped
    out = render(BOARD.replace('permanents = ["Psychatog", "Powder Keg [1]"]', 'permanents = ["Psychatog (tapped) (attacking)", "Powder Keg [1]"]'), reg)
    tog = re.search(r'<span class="pz-card[^"]*"[^>]*>(?:(?!</span>).)*data-card="Psychatog".*?</span>', out, re.S).group(0)
    assert "pz-attacking" in tog and 'class="pz-attack"' in out
    assert out.count('class="pz-attack"') == 1


def test_an_ability_says_whether_it_is_triggered_or_activated():
    out = render(STACK, reg)
    keg = re.search(r'<li class="pz-item pz-by-them pz-ability".*?</li>', out, re.S).group(0)
    assert "Activated ability" in keg
    assert "Triggered ability" in render(STACK.replace('kind = "activated"', 'kind = "triggered"'), reg)
    with pytest.raises(PuzzleError):
        render(STACK.replace('kind = "activated"\n', ""), reg)


def test_revealed_top_of_library_shows_in_order_beside_the_library():
    board = BOARD.replace("library = 31\n", 'library = 31\nlibrary_top = ["Swords to Plowshares", "Island", "Psychatog"]\n')
    out = render(board, reg)
    them = out[:out.index('<div class="pz-side pz-you">')]
    top = re.search(r'<div class="pz-revealed">.*?</div></div>', them, re.S).group(0)
    names = [html.unescape(n) for n in re.findall(r'data-card="([^"]+)"', top)]
    assert names == ["Swords to Plowshares", "Island", "Psychatog"]
    assert top.count("pz-seen") == 3 and "Top 3" in top
    assert "pz-revealed" not in render(BOARD, reg)


def test_stack_targets_point_at_what_they_target():
    board = STACK.replace('target = "Stifle"', 'target = "Stifle"').replace('permanents = ["Psychatog", "Powder Keg [1]"]', 'permanents = ["Psychatog", "Powder Keg [1]"]')
    board = board.replace('[[stack]]\ncard = "Counterspell"', '[[stack]]\ncard = "Vision Charm"\nby = "you"\ntarget = "Psychatog"\n[[stack]]\ncard = "Counterspell"', 1)
    board = board.replace('[them]', '[[stack]]\ncard = "Portent"\nby = "you"\ntarget = "Opponent"\n[them]', 1)
    out = render(board, reg)
    items = re.findall(r'<li class="pz-item[^"]*" data-pz-ref="(stack-\d+)"(?: data-pz-target="([^"]*)")? title="([^"]+)"', out)
    targets = {html.unescape(t).split(",")[0].split(":")[0]: ref for _, ref, t in items}
    assert targets["Stifle"] == "stack-0"                 # Stifle targets the Keg ability, the bottom item
    assert targets["Vision Charm"] == "them-perm-0"       # the Psychatog
    assert targets["Counterspell"] == "stack-1"           # the Stifle
    assert targets["Portent"] == "them-life"
    assert 'data-pz-ref="them-life"' in out and 'data-pz-ref="you-life"' in out


def test_an_aura_is_drawn_attached_to_what_it_enchants():
    e = parse_entry("Forest (tapped) + Wild Growth", reg)
    assert e.card.name == "Forest" and e.tapped and [a.name for a in e.auras] == ["Wild Growth"]
    out = render(BOARD.replace('lands = ["Island", "Island (tapped)"]', 'lands = ["Island", "Forest (tapped) + Wild Growth", "Forest (tapped)"]'), reg)
    you = out[out.index('<div class="pz-side pz-you">'):]
    attach = re.search(r'<span class="pz-attached">.*?data-card="Forest".*?</span></span>', you, re.S).group(0)
    assert 'class="pz-aura"' in attach and 'data-card="Wild Growth"' in attach


def test_a_choice_window_shows_the_cards_or_piles_to_choose_from():
    board = BOARD.replace("[them]", '[choice]\nlabel = "Impulse: put one into your hand"\ncards = ["Opt", "Gush", "Island", "Stifle"]\n\n[them]', 1)
    out = render(board, reg)
    win = re.search(r'<div class="pz-choice">.*?</div></div>', out, re.S).group(0)
    assert "Impulse: put one into your hand" in win
    assert [html.unescape(n) for n in re.findall(r'data-card="([^"]+)"', win)] == ["Opt", "Gush", "Island", "Stifle"]
    assert out.index('<div class="pz-turn') < out.index("pz-choice") < out.index('<div class="pz-side pz-you">')
    piles = render(BOARD.replace("[them]", '[choice]\nlabel = "Fact or Fiction"\npiles = [["Opt", "Gush"], ["Island"]]\n\n[them]', 1), reg)
    assert piles.count('class="pz-pile-choice"') == 2
    assert "pz-choice" not in render(BOARD, reg)


def test_a_meddling_mage_shows_the_card_it_names_under_it():
    e = parse_entry("Meddling Mage (naming Phyrexian Dreadnought)", reg)
    assert e.card.name == "Meddling Mage" and e.naming.name == "Phyrexian Dreadnought" and not e.tapped
    out = render(BOARD.replace('lands = ["Island", "Island (tapped)"]', 'lands = ["Island"]\npermanents = ["Meddling Mage (tapped) (naming Phyrexian Dreadnought)"]'), reg)
    tag = re.search(r'<span class="pz-nametag">(.*?)</span>', out).group(1)
    assert "Naming" in tag and "Phyrexian Dreadnought" in html.unescape(tag)
