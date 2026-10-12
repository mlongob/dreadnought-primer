"""The downloadable PDF: the built page printed by headless Chrome, with the print styles and bookmarks.

The page is served over a throwaway local server and opened with `?pdf`, which makes primer.js load every
image eagerly and record on <html data-broken-images> how many failed. One Chrome session, driven over the
DevTools protocol, loads the page, waits until every image has arrived, checks the count and prints that
same page, so what was checked is what gets printed.
"""
from __future__ import annotations

import base64
import functools
import http.server
import json
import os
import re
import shutil
import socket
import subprocess
import tempfile
import threading
import time
import urllib.request
from pathlib import Path

PDF_NAME = "mono-blue-dreadnought.pdf"
LOAD_TIMEOUT = 180         # seconds for Scryfall's images and the fonts to arrive
PRINT_WIDTH = 360          # card scans are printed about four centimetres wide: 360 pixels is over 200 dpi
CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
]


class PdfError(Exception):
    pass


def find_chrome() -> str:
    """$CHROME if set, otherwise the first Chrome or Chromium found."""
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    for c in CANDIDATES:
        found = c if Path(c).exists() else shutil.which(c)
        if found:
            return found
    raise PdfError("no Chrome or Chromium found; set CHROME to its path")


def chrome_args(chrome: str, port: int, profile: str) -> list[str]:
    return [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
            f"--remote-debugging-port={port}", "--remote-allow-origins=*", f"--user-data-dir={profile}", "about:blank"]


def broken_images(dom: str) -> int | None:
    m = re.search(r'<html[^>]*\bdata-broken-images="(\d+)"', dom)
    return int(m.group(1)) if m else None


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class _Session:
    """Just enough of the DevTools protocol: send a command, wait for its reply."""

    def __init__(self, port: int):
        import websocket
        for _ in range(100):
            try:
                tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json"))
                break
            except OSError:
                time.sleep(.1)
        else:
            raise PdfError("Chrome didn't start")
        page = next(t for t in tabs if t["type"] == "page")
        self.ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=LOAD_TIMEOUT)
        self.n = 0

    def __call__(self, method: str, **params) -> dict:
        self.n += 1
        self.ws.send(json.dumps({"id": self.n, "method": method, "params": params}))
        while True:
            reply = json.loads(self.ws.recv())
            if reply.get("id") == self.n:
                if "error" in reply:
                    raise PdfError(f"{method}: {reply['error'].get('message')}")
                return reply["result"]

    def evaluate(self, expression: str):
        return self("Runtime.evaluate", expression=expression, returnByValue=True,
                    awaitPromise=True)["result"].get("value")


def make_pdf(site: Path, chrome: str | None = None) -> Path:
    """Print site/index.html to site/<PDF_NAME>."""
    chrome = chrome or find_chrome()
    out = site / PDF_NAME
    handler = functools.partial(Quiet, directory=str(site))
    port = _free_port()
    with http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler) as httpd, \
            tempfile.TemporaryDirectory() as profile:
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        proc = subprocess.Popen(chrome_args(chrome, port, profile), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            cdp = _Session(port)
            cdp("Page.navigate", url=f"http://127.0.0.1:{httpd.server_address[1]}/index.html?pdf")
            deadline, broken = time.time() + LOAD_TIMEOUT, None
            while broken is None and time.time() < deadline:
                time.sleep(1)
                value = cdp.evaluate("document.documentElement.dataset.brokenImages")
                broken = int(value) if value is not None else None
            if broken is None:
                raise PdfError("the page never finished loading")
            if broken:
                raise PdfError(f"{broken} images didn't load; try again")
            cdp.evaluate("document.fonts.ready.then(() => true)")
            result = cdp("Page.printToPDF", printBackground=True, preferCSSPageSize=True,
                         generateDocumentOutline=True, displayHeaderFooter=False)
            out.write_bytes(base64.b64decode(result["data"]))
        finally:
            proc.terminate()
            proc.wait(timeout=30)
            httpd.shutdown()
    if not out.exists() or out.stat().st_size < 100_000:
        raise PdfError(f"{out} is missing or too small")
    shrink(out)
    return out


def shrink(path: Path) -> None:
    """Re-encode the card scans at print size: Chrome embeds Scryfall's JPEGs as they are, which makes the
    file nearly three times heavier than it needs to be."""
    import io
    import pikepdf
    from PIL import Image

    pdf = pikepdf.open(path, allow_overwriting_input=True)
    for obj in pdf.objects:
        if not (isinstance(obj, pikepdf.Stream) and obj.get("/Subtype") == "/Image" and obj.get("/Filter") == "/DCTDecode"
                and "/SMask" not in obj and int(obj.Width) > PRINT_WIDTH):
            continue
        image = pikepdf.PdfImage(obj).as_pil_image().convert("RGB")
        height = round(image.height * PRINT_WIDTH / image.width)
        buf = io.BytesIO()
        image.resize((PRINT_WIDTH, height), Image.LANCZOS).save(buf, "JPEG", quality=70, optimize=True)
        if len(buf.getvalue()) >= len(obj.read_raw_bytes()):
            continue
        obj.write(buf.getvalue(), filter=pikepdf.Name.DCTDecode)
        obj.Width, obj.Height = PRINT_WIDTH, height
        obj.ColorSpace, obj.BitsPerComponent = pikepdf.Name.DeviceRGB, 8
        if "/DecodeParms" in obj:
            del obj.DecodeParms
    pdf.save(path, compress_streams=True)
