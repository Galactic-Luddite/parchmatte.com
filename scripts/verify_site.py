#!/usr/bin/env python3
"""Check current screenshot hashes/dimensions (PNG or WebP) and local links on the live pages."""

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import struct
from urllib.parse import unquote, urlsplit


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value and name in {"href", "src"}:
                self.urls.append(value)
            elif value and name == "srcset":
                self.urls.extend(item.strip().split()[0] for item in value.split(",") if item.strip())


def image_header(data):
    """Return (format, width, height, png_color_type) from a PNG or WebP header, or None."""
    if len(data) >= 33 and data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR":
        width, height = struct.unpack(">II", data[16:24])
        return "png", width, height, data[25]
    if len(data) >= 30 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        kind = data[12:16]
        if kind == b"VP8 " and data[23:26] == b"\x9d\x01\x2a":
            width, height = struct.unpack("<HH", data[26:30])
            return "webp", width & 0x3FFF, height & 0x3FFF, None
        if kind == b"VP8L" and data[20] == 0x2F:
            bits = int.from_bytes(data[21:25], "little")
            return "webp", (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1, None
        if kind == b"VP8X":
            return "webp", int.from_bytes(data[24:27], "little") + 1, int.from_bytes(data[27:30], "little") + 1, None
    return None


def verify(root):
    root = root.resolve()
    failures = []
    receipt = json.loads((root / "docs/homepage-media.json").read_text())
    images = receipt["images"]
    if not images:
        failures.append("current screenshot receipt is empty")
    for name, expected in images.items():
        path = root / "images/shots" / name
        if not path.is_file():
            failures.append(f"missing screenshot: {name}")
            continue
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != expected["blob_sha256"]:
            failures.append(f"screenshot hash mismatch: {name}")
        header = image_header(data)
        if header is None:
            failures.append(f"invalid PNG/WebP header: {name}")
            continue
        kind, width, height, color_type = header
        if kind != expected.get("format", "png") or (width, height) != (expected["width"], expected["height"]) or (kind == "png" and color_type != expected["color_type"]):
            failures.append(f"screenshot dimensions/color mismatch: {name}")

    for page in ("index.html", "compare/index.html", "privacy/index.html", "terms/index.html", "guides/paper-texture-on-mac/index.html"):
        source = root / page
        if not source.is_file():
            failures.append(f"missing page: {page}")
            continue
        parser = References()
        parser.feed(source.read_text())
        for reference in parser.urls:
            url = urlsplit(reference)
            if url.scheme or url.netloc or not url.path:
                continue
            path = unquote(url.path)
            target = (root / path.lstrip("/") if path.startswith("/") else source.parent / path).resolve()
            if not target.is_relative_to(root):
                failures.append(f"local reference escapes site: {page}: {reference}")
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                failures.append(f"missing local reference: {page}: {reference}")
    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        failures = verify(args.site_root)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"FAIL: site validation could not complete: {error}")
        return 1
    for failure in failures:
        print(f"FAIL: {failure}")
    if failures:
        return 1
    print("PASS: current screenshot hashes/dimensions and five pages' local references match")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
