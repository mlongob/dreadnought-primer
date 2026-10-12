"""Style warnings from data/lint.toml: US spelling, no stats in prose, corrected claims."""
from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

from .outline import Source

SUFFIX = r"(?:s|d|ed|ing|ly|able|ably)?"


@dataclass(frozen=True)
class LintWarning:
    path: Path
    line: int
    rule: str
    text: str

    def __str__(self) -> str:
        where = f"{self.path}:{self.line}" if self.line else str(self.path)
        return f"{where}: {self.rule}: {self.text}"


def load_rules(path: Path) -> dict:
    data = tomllib.loads(Path(path).read_text())
    return {
        "spelling": (_spelling_re(data.get("spelling", {})), {us.lower(): uk for us, uk in data.get("spelling", {}).items()}),
        "stats": [re.compile(p, re.I) for p in data.get("stats", {}).get("patterns", [])],
        "claims": [(re.compile(c["pattern"]), c["fix"]) for c in data.get("claims", [])],
    }


def _spelling_re(words: dict) -> re.Pattern:
    alternation = "|".join(re.escape(w) for w in sorted(words, key=len, reverse=True))
    return re.compile(rf"\b({alternation}){SUFFIX}\b", re.I)


def _british(word: str, stem: str, uk: str) -> str:
    fixed = uk + word[len(stem):]
    return fixed[0].upper() + fixed[1:] if word[0].isupper() else fixed


def _skip(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") or (s.startswith("{") and s.endswith("}"))


def check(source: Source, rules: dict, stats_ok: bool, card_names=()) -> list[LintWarning]:
    """Warnings for one source. Card names keep their printed spelling, so they are not spell-checked."""
    found = []
    names = sorted(card_names, key=len, reverse=True)
    spelling_re, british = rules["spelling"]
    for i, line in enumerate(source.text.split("\n")):
        if _skip(line):
            continue
        n = source.line_offset + i + 1
        prose = line
        for name in names:
            if name in prose:
                prose = prose.replace(name, " " * len(name))
        for m in spelling_re.finditer(prose):
            uk = _british(m.group(0), m.group(1), british[m.group(1).lower()])
            found.append(LintWarning(source.path, n, "spelling", f"{m.group(0)!r}: US spelling is {uk!r}"))
        if not stats_ok:
            for rx in rules["stats"]:
                for m in rx.finditer(line):
                    found.append(LintWarning(source.path, n, "stats", f"{m.group(0)!r}: no numbers in prose (they date)"))
        for rx, fix in rules["claims"]:
            if rx.search(line):
                found.append(LintWarning(source.path, n, "claim", f"{rx.pattern!r}: {fix}"))
    return found
