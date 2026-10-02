#!/usr/bin/env python3
"""Check current screenshot hashes/dimensions and local links on the live pages."""

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


def verify(root):
    root = root.resolve()
    failures = []
    receipt = json.loads((root / "docs/homepage-media-build21.json").read_text())
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
        if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
            failures.append(f"invalid PNG header: {name}")
            continue
        width, height = struct.unpack(">II", data[16:24])
        if (width, height, data[25]) != (expected["width"], expected["height"], expected["color_type"]):
            failures.append(f"screenshot dimensions/color mismatch: {name}")

    for page in ("index.html", "compare/index.html", "privacy/index.html"):
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
    print("PASS: current screenshot hashes/dimensions and three pages' local references match")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
