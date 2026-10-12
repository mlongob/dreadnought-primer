import importlib.util

from conftest import ROOT

spec = importlib.util.spec_from_file_location("add_card", ROOT / "tools" / "add_card.py")
add_card = importlib.util.module_from_spec(spec)
spec.loader.exec_module(add_card)


def printing(set_, number="1", **kw):
    base = {"set": set_, "collector_number": number, "id": f"id-{set_}", "lang": "en", "games": ["paper"],
            "digital": False, "promo": False, "nonfoil": True, "set_type": "core", "oversized": False,
            "border_color": "black"}
    return {**base, **kw}


def test_first_eligible_printing_wins():
    assert add_card.choose([printing("tmp", nonfoil=False), printing("sth"), printing("7ed")])["set"] == "sth"


def test_beta_preferred_over_alpha():
    assert add_card.choose([printing("lea"), printing("leb"), printing("2ed")])["set"] == "leb"


def test_falls_back_to_special_printing():
    assert add_card.choose([printing("pxyz", promo=True)])["set"] == "pxyz"


def test_toml_block_quotes_name():
    block = add_card.toml_block("Chainer's Edict", {"id": "abc", "set": "TOR", "collector_number": "57"})
    assert block == '\n[cards."Chainer\'s Edict"]\nid = "abc"\nset = "tor"\nnumber = "57"\n'
