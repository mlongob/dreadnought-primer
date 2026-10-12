import pytest

from builder.outline import OutlineError, load


def make(tmp_path, chapters=("intro", "matchups"), matchups=("mirror",), files=None, extra=""):
    (tmp_path / "content" / "matchups").mkdir(parents=True)
    (tmp_path / "outline.toml").write_text(
        'title = "T"\nsubtitle = "S"\ndateline = "October 2026"\n'
        f"chapters = {list(chapters)!r}\nmatchups = {list(matchups)!r}\n{extra}".replace("'", '"'))
    files = files if files is not None else {
        "intro.md": "## Intro\n\nText.\n",
        "matchups.md": "## Matchups\n\nIntro.\n",
        "matchups/mirror.md": '+++\n[[map]]\nlabel = "Mirror (61)"\nplan = "Freeze"\n+++\n### The mirror\n\nText.\n',
    }
    for rel, text in files.items():
        (tmp_path / "content" / rel).write_text(text)
    return tmp_path


def test_loads_in_order_with_matchups_after_their_chapter(tmp_path):
    o = load(make(tmp_path))
    assert [(s.kind, s.slug) for s in o.sources] == [("chapter", "intro"), ("chapter", "matchups"), ("matchup", "mirror")]
    assert (o.title, o.subtitle, o.dateline) == ("T", "S", "October 2026")


def test_front_matter_is_parsed_and_stripped(tmp_path):
    m = load(make(tmp_path)).sources[2]
    assert m.meta["map"][0] == {"label": "Mirror (61)", "plan": "Freeze"}
    assert m.text.startswith("### The mirror")
    assert m.line_offset == 5


def test_stats_ok(tmp_path):
    o = load(make(tmp_path, extra='stats_ok = ["intro"]\n'))
    assert o.stats_ok == {"intro"}


def test_missing_file(tmp_path):
    with pytest.raises(OutlineError, match="outline lists 'history' but content/history.md does not exist"):
        load(make(tmp_path, chapters=("intro", "history", "matchups")))


def test_unlisted_file(tmp_path):
    root = make(tmp_path)
    (root / "content" / "stray.md").write_text("## Stray\n")
    with pytest.raises(OutlineError, match="content/stray.md is not in outline.toml"):
        load(root)


def test_duplicate_entry(tmp_path):
    with pytest.raises(OutlineError, match="'intro' appears twice"):
        load(make(tmp_path, chapters=("intro", "intro", "matchups")))


def test_chapter_must_start_with_h2(tmp_path):
    root = make(tmp_path)
    (root / "content" / "intro.md").write_text("### Wrong level\n")
    with pytest.raises(OutlineError, match="content/intro.md must start with a '## ' heading"):
        load(root)


def test_matchup_must_start_with_h3(tmp_path):
    root = make(tmp_path)
    (root / "content" / "matchups" / "mirror.md").write_text("## Wrong level\n")
    with pytest.raises(OutlineError, match="content/matchups/mirror.md must start with a '### ' heading"):
        load(root)


def test_matchups_need_the_matchups_chapter(tmp_path):
    with pytest.raises(OutlineError, match="'matchups' chapter"):
        load(make(tmp_path, chapters=("intro",), files={"intro.md": "## Intro\n", "matchups/mirror.md": "### M\n"}))
