# Mono-Blue Dreadnought (Stiflenought) — a Premodern primer

A living primer for Mono-U Stiflenought, published as a one-page static site on GitHub Pages.
The author dictates ideas and corrections in chat; Claude edits the content files. The author does not
edit files by hand.

## How the primer teaches (why it is ordered the way it is)

The author's view: there are very few hard-and-fast rules with this deck; you learn it in layers. First what
each card does (card analysis), then the deck's plans (how it plays, mulligans), then the opponents — how to
position yourself in each matchup and how to sideboard. Puzzles will come last, so a reader who has done the
reading can practise applying it by deduction. The document is long on purpose. Keep the chapter order;
improve each layer rather than reshuffling them.

## What's next

`docs/ROADMAP.md` holds the planned work, proposals and open questions for the author. Update it when
the author adds, settles or finishes something.

## Reviewing changes with the author

New matchup sections (and other wholly new writing) skip the review edition: write them straight into the
content, rebuild, and point the author at the normal page (`http://127.0.0.1:8000/#<section>`); they give
feedback in chat. Use the review edition for edits to text the author has already read.

Work in batches (one chapter group at a time). After a batch, build the review edition —
`.venv/bin/python -m builder review` writes `site/review.html` with every change since the last approved
state marked in place — and ask the author to read it. Apply their keep/revert/reword answers, then
`.venv/bin/python -m builder approve` marks the current state as the new baseline (git tag `approved`). When the author reads on
mobile, send a PDF of just the changed sections instead: build the review, then print
`http://127.0.0.1:8000/review.html?changed` with headless Chrome (`--print-to-pdf`, `--virtual-time-budget=40000`)
to `private/exports/` and send that file.

## Where things live

| What | File |
|---|---|
| Page title, chapter and matchup order, chapters allowed numbers, site and repo URLs | `outline.toml` |
| One chapter per file, starting with its `## ` heading | `content/<chapter>.md` |
| One matchup per file, starting with its `### ` heading, front matter for the sideboard map | `content/matchups/<deck>.md` |
| The 75 (main, side, grouping of the deck picture) | `data/deck.toml` |
| Every card shown or linked: Scryfall id, set, number; aliases; deck names | `data/cards.toml` |
| The combo figure text | `data/combo.toml` |
| Style checks (spelling, numbers in prose, corrected claims) | `data/lint.toml` |
| The build | `builder/` (templates and CSS/JS in `builder/templates`, `builder/static`) |
| Land-keep maths, stats scripts, card lookup | `tools/` |
| Private material, never committed: source primers, the drafting transcript, DB extracts | `private/` |

A new chapter or matchup is a new file plus its slug in `outline.toml`; the build refuses a file that
isn't listed and a listed file that doesn't exist.

## Commands

    .venv/bin/python -m builder check      # after every edit: validation + style warnings
    .venv/bin/python -m pytest -q          # before every commit
    .venv/bin/python -m builder serve      # build and preview at http://127.0.0.1:8000
    .venv/bin/python -m builder pdf        # build, then print site/mono-blue-dreadnought.pdf (the download link)
    .venv/bin/python tools/add_card.py "Card Name"   # add a card to the register

Setup in a fresh checkout: `python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"`.
Pushing to `main` runs the tests, builds and deploys to GitHub Pages (`.github/workflows/pages.yml`).

## Markup

| Syntax | Renders |
|---|---|
| `{card: Name}` | one card beside the next paragraph (right margin on wide screens) |
| `{cards: A \| B \| C \| D}` | a row of up to four cards |
| `{hand: A \| … }` | a seven-card example hand (exactly seven) |
| `{decklist}` | the 75 as stacks, from `data/deck.toml` |
| `{combo}` | the three-card combo figure |
| `{sideboard-map}` | the quick-reference table, generated from the matchup rows |
| `**Sideboarding (61):** −1 Dreadnought, −2 Daze / +3 Annul, +2 Brain Freeze.` | the row, plus Out/In stacks |
| `{nolink: Text}` | text never linked |
| `{puzzle}` … `{/puzzle}` | a practice board drawn MTGO-style from a TOML block (turn, active, phase; `[them]` and `[you]` with life, library, hand, lands, permanents, graveyard; entries take `(tapped)`, `(seen)`, `(phased out)`, `(attacking)`, `(naming Card Name)` for a Meddling Mage, `[N]` counters; `"?"` is an unseen card; optional `[[stack]]` items, bottom first, with `card`, `by`, and for an ability its `ability` text and `kind` (`"triggered"` or `"activated"`), or a `target` note — a target that names a player (`Opponent`, `You`), a spell or ability below it on the stack (`Stifle`, `Powder Keg's ability`) or a permanent gets an arrow drawn to it; optional `storm` count; optional `library_top`, cards revealed from the top of a library, top first; optional `[choice]` with a `label` and `cards` or `piles`, a choice in progress such as an Impulse or a Fact or Fiction) — see `builder/puzzle.py` |
| `{answer}` … `{/answer}` | the puzzle's answer, a click-to-reveal spoiler on screen, always shown in print |
| `[Edict]{Chainer's Edict}` | text linked to a named card |

Card lists use `|` between names, so names with commas need nothing special. Rows keep their notation:
shorthand Dreadnought, Flash, Keg, Chain, Charm, Freeze, B2B, Flare, BEB; "4 blasts" = 2 Blue Elemental
Blast + 2 Hydroblast; `(61)` in the label sets the deck size; several labelled rows can share a line;
"as above plus …" adds to the row above. The build checks every row against the 75.

Each matchup's front matter has one `[[map]]` entry per row (the label for the sideboard map; `out`
and `in` override a row written as prose; `omit = true` leaves that line out of the table while the author
works it out). `unverified_rows` turns a row's validation error into a warning until the author confirms
it.

**Card links.** The first mention of a card in each section links to it (hover preview, click to
enlarge); later mentions stay plain. Aliases (Dreadnought, Charm, Keg, …) and plurals count. Card names
that are also deck names (`deck_names` in `data/cards.toml`: Replenish, Stasis, Aluren, Opposition) never
link on their own. Judge each mention by context, as the author asked: the card ("under Stasis", "Counter
Replenish", a list of Annul targets) gets `[Stasis]{Stasis}` on its first card-sense mention in the section;
the deck ("Stasis lists", "against Landstill, Replenish and Ponza", "the Stasis matchup") stays plain.
Headings are never linked.

Unknown cards fail the build with the command to add them. Add the card, don't work around it.

## The author's conventions (follow them)

1. **The 75 is fixed.** Variants and alternatives appear only in History, Versions and Close
   candidates, to justify slots. Nowhere after that may the text suggest changing the list, except the flex slot (the main-deck Brain Freeze), which the author presents as a choice: Misdirection, a second Keg or a third Flash fit it too.
2. **No stats in prose.** Numbers date and the document is living. Say "most", "a third", "nearly
   every". The intro keeps a few positioning numbers stamped "as of October 2026". Never count matchups
   or rows ("twelve of the mapped decks"); matchups are added organically. (Land-drop probabilities in
   Mana base and Mulligans are maths on the fixed 75 and may stay.)
3. **No absolutes.** "Doesn't see a lot of competitive play", not "nobody plays it". "Most of the
   time", not "always". "Be careful Flaring a pumper", not "never".
4. **Credits:** none in the text for now, except facts: Dave Kaplan (the jam build, Reality
   Ripple/Intuition choices, the Flare + Back to Basics sideboard pedigree), SpockVidaLoka and
   LuffyDoChapeuDePalha (the Brazilian MTGO grinders whose 75 is the stock list; this list is theirs
   minus Misdirection, plus Brain Freeze), Simone Fierro (won the European Championship with Tranquil
   Domain in the side off Vision Charm's land-type mode). Claire Ackerman (5C Oath Ponza, built to beat the deck). The Foreword and Resources credit the primers and communities the author named; beyond those, no other credits.
5. **Images everywhere.** When a card is discussed, show it, even if it was shown before. Key-card rows
   show THEIR cards, not ours. Rows of up to four.
6. **Corrections already made — never reintroduce:** Portent is a sorcery; Foil pitches an Island plus any card, blue or not (only Flash of Insight needs blue cards); Impulse bottoms (Oracle),
   doesn't shuffle; Annul doesn't counter Brain Freeze; Meddling Mage has no trigger and rarely names
   Stifle; Sutured Ghoul's exile is a replacement effect (not Stifle-able); Volrath's Shapeshifter's copy
   is static, its "2: discard" is the activation; Pernicious Deed is black-green; Negator is mana value
   4; Hidden Gibbons flips to 4/4; Tendrils, Mind's Desire, Rule of Law are not Premodern-legal; Rishadan
   Port taps basics; B2B does hurt Port (it taps once and never untaps), but Port alone isn't the reason to bring B2B — Mishra's Factory and the other nonbasics are; cycling lands are stopped by Web, not an edge for B2B;
   Vision Charm's land mode only touches basics (no duals/shocks in Premodern), except the Lairs and the Urza's lands (Lair and Urza's are land types it can name); Charm your Dreadnought
   BEFORE cracking Keg at 1, never "in response"; never Peek yourself; Dreadnought is a creature so
   Duress can't take it — Cabal Therapy names it blind. When the author corrects something new, add a
   pattern to `data/lint.toml` `[[claims]]`.
7. **Full English Breakfast vs Angry Hermit:** FEB (hFEB, the Hermit Druid version, and the rarer Survival-based classic cFEB) kills with Volrath's Shapeshifter + Phyrexian Devourer/Triskelion, or a Shapeshifter-as-Karmic-Guide chain into Psychatog/Akroma (no Cloudscraper or Dragon Breath in current lists); Angry
   Hermit/Angry Ghoul uses Sutured Ghoul. Don't conflate.
8. **Tone:** respond to corrections by fixing, not apologizing at length. No condescension toward opponents ("isn't playing around it", not
   "hasn't learned"). **US spelling** throughout the document (favorable, color), as the
   author writes American in chat.
9. **Frame by the real format, not by fringe cards.** Lead with what matters against the decks people
   actually play; don't headline an interaction with a niche card. Example the author corrected: not
   "Islands that no Back to Basics can touch" but "mana that is consistent, works with the blue cards and
   is hard for denial strategies to attack".
10. **Voice:** first person ("I play…"). Whether it becomes "we" is undecided; don't change it without
   asking.

Matchup entries follow the template: Verdict · What they do · What the matchup hinges on · Game one ·
After sideboarding · Sideboarding · Why these. The author dictates; Claude drafts; the author corrects.

## Site design decisions (from the author)

Dark theme by default with a light toggle; print is always light. One long page with a sidebar.
Stacks show every copy, no count badges. Card images come straight from Scryfall's CDN: never crop,
blur, dim or color-shift them (Scryfall's terms), and keep the Wizards/Scryfall credit in the footer.
