import pytest

from builder.deck import DeckError, load
from conftest import ROOT


@pytest.fixture
def deck(register):
    return load(ROOT / "data" / "deck.toml", register)


def test_real_deck_is_sixty_and_fifteen(deck):
    assert sum(deck.main.values()) == 60
    assert sum(deck.side.values()) == 15


def test_rows_cover_the_main_deck(deck):
    assert sorted(n for row in deck.rows for n in row) == sorted(deck.main)


def test_wrong_main_count_is_an_error(tmp_path, register):
    p = tmp_path / "deck.toml"
    p.write_text('rows = [["Island"]]\n[main]\nIsland = 59\n[side]\nAnnul = 15\n')
    with pytest.raises(DeckError, match="main deck has 59 cards, expected 60"):
        load(p, register)


def test_unknown_card_is_an_error(tmp_path, register):
    p = tmp_path / "deck.toml"
    p.write_text('rows = [["Black Lotus"]]\n[main]\n"Black Lotus" = 60\n[side]\nAnnul = 15\n')
    with pytest.raises(DeckError, match="Black Lotus"):
        load(p, register)


def test_row_card_missing_from_main_is_an_error(tmp_path, register):
    p = tmp_path / "deck.toml"
    p.write_text('rows = [["Island", "Stifle"]]\n[main]\nIsland = 60\n[side]\nAnnul = 15\n')
    with pytest.raises(DeckError, match="Stifle"):
        load(p, register)
