from pathlib import Path

import pytest

from builder.outline import Source
from builder.rows import parse_line
from builder.sbmap import MapError, format_items, sideboard_map


def matchup(slug, meta, *lines, reg):
    rows = [r for line in lines for r in parse_line(line, reg)]
    return Source(Path(f"content/matchups/{slug}.md"), "", "matchup", slug, meta, 0), rows


def anchors(**ids):
    return ids


def test_abbreviations_and_counts(reg):
    [r] = parse_line("**Sideboarding (61):** −1 Dreadnought, −2 Daze, −1 Thwart / +3 Annul, +2 Brain Freeze.", reg)
    assert format_items(r.outs) == "1 DN, 2 Daze, 1 Thwart"
    assert format_items(r.ins) == "3 Annul, 2 BF"


def test_blasts_collapse(reg):
    [r] = parse_line("**Sideboarding:** −1 Keg / +2 Blue Elemental Blast, +2 Hydroblast, +2 Flare.", reg)
    assert format_items(r.ins) == "4 Blasts, 2 Flare"


def test_lone_beb_stays(reg):
    [r] = parse_line("**Sideboarding:** −1 Flash / +2 Blue Elemental Blast.", reg)
    assert format_items(r.ins) == "2 BEB"


def test_table_rows_link_to_matchups(reg):
    m = matchup("mirror", {"map": [{"label": "Mirror (61)"}]},
                "**Sideboarding (61):** −1 Dreadnought, −2 Daze, −1 Thwart / +3 Annul, +2 Brain Freeze.", reg=reg)
    html = sideboard_map([m], anchors(mirror="the-mirror"))
    assert '<table class="sbmap">' in html
    assert '<td><a href="#the-mirror">Mirror (61)</a></td><td>1 DN, 2 Daze, 1 Thwart</td><td>3 Annul, 2 BF</td></tr>' in html


def test_delta_and_override_rows(reg):
    s = matchup("survival", {"map": [{"label": "Survival (all)"},
                                     {"label": "Survival Welder"}]},
                "**Sideboarding:** −2 Daze / +2 Annul.",
                "**Welder/Tradewind:** as above plus −1 Flash / +2 Blue Elemental Blast.", reg=reg)
    o = matchup("oath", {"map": [{"label": "GR"},
                                 {"label": "GW", "out": "as Terrageddon", "in": "as Terrageddon"}]},
                "**Sideboarding (GR):** −1 Opt / +1 Annul.", "**Sideboarding (GW):** the Terrageddon row.", reg=reg)
    html = sideboard_map([s, o], anchors(survival="survival", oath="oath"))
    assert "<td>above + 1 Flash</td><td>above + 2 BEB</td>" in html
    assert "<td>as Terrageddon</td><td>as Terrageddon</td>" in html


def test_row_count_mismatch_is_an_error(reg):
    m = matchup("mirror", {"map": [{"label": "A"}, {"label": "B"}]},
                "**Sideboarding:** −1 Daze / +1 Annul.", reg=reg)
    with pytest.raises(MapError, match="content/matchups/mirror.md: 2 map entries but 1 row"):
        sideboard_map([m], anchors(mirror="the-mirror"))


def test_prose_row_without_override_is_an_error(reg):
    m = matchup("oath", {"map": [{"label": "GW"}]}, "**Sideboarding (GW):** the Terrageddon row.", reg=reg)
    with pytest.raises(MapError, match="prose"):
        sideboard_map([m], anchors(oath="oath"))


def test_matchup_without_rows_or_map_is_skipped(reg):
    m = matchup("new", {}, reg=reg)
    assert "<tbody></tbody>" in sideboard_map([m], anchors(new="new"))


def test_anchor_comes_from_the_matchup_not_its_position(reg):
    m = matchup("sligh", {"map": [{"label": "Sligh"}]}, "**Sideboarding:** −1 Keg / +1 Annul.", reg=reg)
    assert '<a href="#sligh-2">Sligh</a>' in sideboard_map([m], anchors(sligh="sligh-2"))


def test_omitted_entry_is_left_out_of_the_table(reg):
    s = matchup("survival", {"map": [{"label": "Survival (all)"},
                                     {"label": "Survival Welder", "omit": True}]},
                "**Sideboarding:** −2 Daze / +2 Annul.",
                "**Welder/Tradewind:** as above plus −1 Flash / +2 Blue Elemental Blast.", reg=reg)
    html = sideboard_map([s], anchors(survival="survival"))
    assert "Survival (all)" in html and "Survival Welder" not in html


def test_table_has_no_plan_column(reg):
    m = matchup("sligh", {"map": [{"label": "Sligh"}]}, "**Sideboarding:** −1 Keg / +1 Annul.", reg=reg)
    out = sideboard_map([m], anchors(sligh="sligh"))
    assert "<th>Plan</th>" not in out
    assert out.count("<th>") == 3
    assert out.count("<td>") + out.count("<td ") == 3
