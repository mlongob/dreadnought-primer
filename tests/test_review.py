from builder.review import mark, plain, word_diff


def test_plain_strips_markup():
    assert plain("**Verdict.** an [Edict]{Diabolic Edict} and {nolink: Stasis}") == "Verdict. an Edict and Stasis"


def test_word_diff_marks_only_the_change():
    html = word_diff("Keg at 4 kills Wurm.", "Keg at 4 kills Negator.")
    assert html == "Keg at 4 kills <del>Wurm</del><ins>Negator</ins>."


def test_word_diff_escapes():
    assert "&lt;b&gt;" in word_diff("a", "a <b>")


def test_unchanged_text_is_untouched():
    text = "## A\n\nOne.\n\nTwo."
    marked, changes = mark(text, text, "content/a.md")
    assert marked == text and changes == []


def test_edited_paragraph_becomes_a_diff_block():
    marked, changes = mark("## A\n\nOne **bold** word.", "## A\n\nOne **bold** phrase.", "content/a.md")
    assert '<div class="rv rv-edit" id="change-1"><p>One bold <del>word</del><ins>phrase</ins>.</p></div>' in marked
    assert [(c.id, c.kind) for c in changes] == [("change-1", "edit")]


def test_added_and_removed_paragraphs():
    marked, changes = mark("## A\n\nOld one.\n\nKept.", "## A\n\nKept.\n\nNew one.", "content/a.md")
    assert '<div class="rv rv-remove" id="change-1"><p><del>Old one.</del></p></div>' in marked
    assert '<div class="rv rv-add" id="change-2"><p><ins>New one.</ins></p></div>' in marked
    assert "\n\nKept.\n\n" in marked


def test_changed_heading_stays_a_heading_with_a_note():
    marked, changes = mark("### Gush (4)\n\nText.", "### Gush (4), the engine\n\nText.", "content/a.md")
    assert "\n### Gush (4), the engine\n" in "\n" + marked
    assert 'class="rv rv-note"' in marked and "<ins>, the engine</ins>" in marked


def test_changed_directive_renders_and_is_noted():
    marked, changes = mark("## A\n\n{cards: Opt | Peek}", "## A\n\n{cards: Opt | Gush}", "content/a.md")
    assert "{cards: Opt | Gush}" in marked and 'class="rv rv-note"' in marked
    assert changes[0].kind == "figure"


def test_new_file_is_all_added():
    marked, changes = mark(None, "### New\n\nHello.", "content/matchups/new.md")
    assert "### New" in marked and '<ins>Hello.</ins>' in marked


def test_change_ids_continue_across_files():
    _, c1 = mark("A.", "B.", "content/a.md", start=1)
    _, c2 = mark("C.", "D.", "content/b.md", start=2)
    assert [c1[0].id, c2[0].id] == ["change-1", "change-2"]


def test_unrelated_rewrite_is_shown_as_remove_plus_add():
    marked, changes = mark("## A\n\nThe old plan was mana denial into a midgame jam.",
                           "## A\n\nVerdict. Slightly unfavourable against their clock.", "content/a.md")
    assert [c.kind for c in changes] == ["remove", "add"]
    assert "<del>" in marked and 'rv-add' in marked


def test_small_edit_is_still_a_word_diff():
    marked, changes = mark("## A\n\nCounter the Library when you can.", "## A\n\nCounter the Library whenever you can.", "content/a.md")
    assert [c.kind for c in changes] == ["edit"]
