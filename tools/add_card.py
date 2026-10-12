#!/usr/bin/env python3
"""Add cards to data/cards.toml from Scryfall.

    python tools/add_card.py "Exploration" "Seal of Removal"
    python tools/add_card.py "Stifle" --set scg --number 52      # pin a printing
    python tools/add_card.py --dry-run "Exploration"              # print, don't write

Printing rule (the author's): first paper printing, non-foil, standard border, Beta over Alpha.
Basic lands are the exception, the author's chosen printings (Island is whatever the register already has).
"""
import argparse
import json
import sys
import time
import tomllib
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REGISTER = Path(__file__).resolve().parent.parent / "data" / "cards.toml"
HEADERS = {"User-Agent": "stiflenought-primer/1.0 (card register tool)", "Accept": "application/json"}


def fetch(url: str, **params) -> dict:
    if params:
        url += "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS)) as r:
        time.sleep(0.1)  # Scryfall asks for 50–100 ms between API requests
        return json.load(r)


def eligible(c: dict) -> bool:
    return (c.get("lang") == "en" and "paper" in (c.get("games") or []) and not c.get("digital")
            and not c.get("promo") and c.get("nonfoil") is True
            and c.get("set_type") not in ("memorabilia", "token", "minigame", "funny")
            and not c.get("oversized") and c.get("border_color") in ("black", "white"))


def choose(prints: list[dict]) -> dict:
    """Pick the printing from a list sorted oldest first."""
    cands = [c for c in prints if eligible(c)] or prints
    first = cands[0]
    if first["set"] == "lea":
        first = next((c for c in cands if c["set"] == "leb"), first)
    return first


def toml_block(name: str, c: dict) -> str:
    q = lambda s: json.dumps(s, ensure_ascii=False)
    return f'\n[cards.{q(name)}]\nid = {q(c["id"])}\nset = {q(c["set"].lower())}\nnumber = {q(c["collector_number"])}\n'


BASICS = {"Mountain": ("mir", "346"), "Plains": ("usg", "331"), "Forest": ("ons", "349"), "Swamp": ("ons", "341")}


def lookup(name: str, set_: str | None, number: str | None) -> tuple[str, dict]:
    if not (set_ and number) and name in BASICS:
        set_, number = BASICS[name]
    if set_ and number:
        c = fetch(f"https://api.scryfall.com/cards/{set_.lower()}/{number}")
        return c["name"], c
    data = fetch("https://api.scryfall.com/cards/search", q=f'!"{name}"', unique="prints", order="released", dir="asc")
    prints = data["data"]
    while data.get("has_more"):
        data = fetch(data["next_page"])
        prints += data["data"]
    c = choose(prints)
    return c["name"], c


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="+")
    ap.add_argument("--set")
    ap.add_argument("--number")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    existing = tomllib.loads(REGISTER.read_text()).get("cards", {})
    blocks = []
    for name in args.names:
        try:
            canonical, c = lookup(name, args.set, args.number)
        except urllib.error.HTTPError as e:
            print(f"error: {name!r}: Scryfall {e.code}", file=sys.stderr)
            return 1
        if canonical in existing:
            print(f"skip: {canonical!r} is already in the register")
            continue
        blocks.append(toml_block(canonical, c))
        print(f"{canonical}: {c['set'].upper()} {c['collector_number']} ({c.get('set_name', '')})")
    if blocks and not args.dry_run:
        with REGISTER.open("a") as f:
            f.write("".join(blocks))
    return 0


if __name__ == "__main__":
    sys.exit(main())
