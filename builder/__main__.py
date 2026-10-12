"""python -m builder build | pdf | check [--strict] | serve [--port 8000] | review [--since REF] | approve"""
import argparse
import functools
import http.server
import subprocess
import sys
from pathlib import Path

from .pdf import PDF_NAME, PdfError, make_pdf
from .render import BuildError, build

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"


def main() -> int:
    ap = argparse.ArgumentParser(prog="python -m builder", description="Build the primer site.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build", help="build site/")
    check = sub.add_parser("check", help="validate and lint without writing anything")
    check.add_argument("--strict", action="store_true", help="treat warnings as errors")
    serve = sub.add_parser("serve", help="build, then serve site/ locally")
    serve.add_argument("--port", type=int, default=8000)
    review = sub.add_parser("review", help="build site/review.html with changes since the approved state marked")
    review.add_argument("--since", default="approved", help="git ref to compare with (default: the 'approved' tag)")
    review.add_argument("--standalone", action="store_true", help="also write one self-contained file, for reading on a phone")
    sub.add_parser("approve", help="mark the current commit as the approved state")
    sub.add_parser("pdf", help=f"build site/, then print it to site/{PDF_NAME} with headless Chrome")
    prev = sub.add_parser("preview", help="build the confidential preview edition")
    args = ap.parse_args()

    if args.cmd == "approve":
        return approve()
    if args.cmd == "review":
        return build_review(args.since, args.standalone)
    if args.cmd == "preview":
        try:
            result = build(ROOT, SITE, preview=True)
        except BuildError as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
        print(f"built {SITE / 'preview.html'}")
        return 0

    try:
        result = build(ROOT, None if args.cmd == "check" else SITE)
    except BuildError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    for w in result.warnings:
        print(f"warning: {w}", file=sys.stderr)
    if args.cmd == "check":
        print(f"ok: {len(result.toc)} chapters, {len(result.warnings)} warnings")
        return 1 if args.strict and result.warnings else 0
    print(f"built {SITE / 'index.html'} ({len(result.html) // 1024} KB, {len(result.warnings)} warnings)")
    if args.cmd == "pdf":
        for attempt in range(3):   # Scryfall's images arrive over the network; a slow fetch is worth a retry
            try:
                out = make_pdf(SITE)
                break
            except (PdfError, subprocess.SubprocessError) as e:
                print(f"{'error' if attempt == 2 else 'retrying'}: {e}", file=sys.stderr)
        else:
            return 1
        print(f"printed {out} ({out.stat().st_size // (1024 * 1024)} MB)")
    if args.cmd == "serve":
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SITE))
        with http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler) as httpd:
            print(f"serving http://127.0.0.1:{args.port}/ (Ctrl-C to stop)")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                pass
    return 0


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout


def approve() -> int:
    if git("status", "--porcelain", "--", "content", "data", "outline.toml").strip():
        print("error: content has uncommitted changes; commit them before approving", file=sys.stderr)
        return 1
    git("tag", "-f", "approved", "HEAD")
    print(f"approved: {git('rev-parse', '--short', 'HEAD').strip()}")
    return 0


def build_review(since: str, standalone: bool = False) -> int:
    try:
        paths = [p for p in git("ls-tree", "-r", "--name-only", since, "--", "content").splitlines() if p.endswith(".md")]
    except subprocess.CalledProcessError:
        print(f"error: no git ref {since!r}; run `python -m builder approve` once to set a baseline", file=sys.stderr)
        return 1
    base = {p: git("show", f"{since}:{p}") for p in paths}
    try:
        result = build(ROOT, SITE, review=base)
    except BuildError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(f"built {SITE / 'review.html'}: {len(result.changes)} changes since {since}")
    if standalone:
        from .render import inline_assets
        path = SITE / "review-standalone.html"
        path.write_text(inline_assets(result.html))
        print(f"built {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
