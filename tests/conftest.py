from pathlib import Path

import pytest

from builder.cards import Register

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def root():
    return ROOT


@pytest.fixture(scope="session")
def register():
    return Register.load(ROOT / "data" / "cards.toml")


@pytest.fixture(scope="session")
def reg(register):
    return register


@pytest.fixture(scope="session")
def deck(register):
    from builder.deck import load
    return load(ROOT / "data" / "deck.toml", register)
