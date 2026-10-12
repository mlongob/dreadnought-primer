# Mono-U Stiflenought — a Premodern primer

A living primer for Mono-U Stiflenought in Premodern: how the deck plays, every card in the 75, the
sideboard, mulligans and matchups. Published as one page on GitHub Pages.

## Building

    python3 -m venv .venv
    .venv/bin/pip install -e ".[dev]"
    .venv/bin/python -m builder serve        # http://127.0.0.1:8000

`python -m builder pdf` also prints the downloadable PDF with headless Chrome (set `CHROME` if it isn't
found). `python -m builder check` validates the content (every card exists, every sideboard row fits the 75)
and prints style warnings; `python -m builder build` writes `site/`. Pushes to `main` run the tests and
deploy.

The content is Markdown in `content/`, in the order set by `outline.toml`; `CLAUDE.md` describes the
markup and the editing conventions.

Card images are served by [Scryfall](https://scryfall.com). Magic: The Gathering card names, text and
images are © Wizards of the Coast. This primer is unofficial Fan Content permitted under the Fan
Content Policy, not approved or endorsed by Wizards.

## Contributing

Corrections, matchup notes and new ideas are welcome. [Open an issue](https://github.com/mlongob/dreadnought-primer/issues/new) to
suggest something, or send a pull request: edit the Markdown in `content/`, run `python -m builder check`
and `pytest -q`, and open the PR. You can also find the author as Flario on
[the Shrimp](https://discord.gg/7g6nvher9H), the Premodern Dreadnought Discord.

## License

The primer's text is © 2026 Mario Longobardi and licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (see `LICENSE-CONTENT.md`): share and
adapt it freely, with credit. The build code is under the MIT license (see `LICENSE`).
