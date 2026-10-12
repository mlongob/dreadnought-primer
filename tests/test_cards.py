import pytest

from builder.cards import UnknownCard


def test_alias_resolves(register):
    assert register.get("Charm").name == "Vision Charm"


def test_full_name_resolves(register):
    assert register.get("Stifle").name == "Stifle"


def test_unknown_card_names_the_tool(register):
    with pytest.raises(UnknownCard, match="tools/add_card.py"):
        register.get("Black Lotus")


def test_image_url(register):
    c = register.get("Phyrexian Dreadnought")
    assert c.image("normal") == f"https://cards.scryfall.io/normal/front/{c.id[0]}/{c.id[1]}/{c.id}.jpg"


def test_page_url(register):
    assert register.get("Phyrexian Dreadnought").page == "https://scryfall.com/card/mir/315"


def test_names_include_aliases_and_cards(register):
    names = register.names()
    assert names["Keg"] == "Powder Keg"
    assert names["Stifle"] == "Stifle"


def test_card_img_markup(register):
    from builder.cards import card_img
    c = register.get("Stifle")
    html = card_img(c, "14rem")
    assert f'src="{c.image("normal")}"' in html
    assert f'srcset="{c.image("small")} 146w, {c.image("normal")} 488w"' in html
    assert 'sizes="14rem"' in html and 'width="488" height="680"' in html
    assert 'loading="lazy"' in html and 'alt="Stifle"' in html
    assert f'data-img="{c.id}"' in html and f'data-page="{c.page}"' in html


def test_card_img_eager_and_alt(register):
    from builder.cards import card_img
    html = card_img(register.get("Chainer's Edict"), "7rem", eager=True, alt="")
    assert 'loading="eager"' in html and 'alt=""' in html and 'data-card="Chainer&#x27;s Edict"' in html


def test_deck_names_excluded_from_linkable_names(register):
    assert "Stasis" in register.names()
    assert "Stasis" not in register.linkable_names()
    assert "Stifle" in register.linkable_names()
