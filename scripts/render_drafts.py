#!/usr/bin/env python3
"""Render a standalone, self-contained draft of the homepage for review.

The output inlines style.css and embeds grain.png, icon.png, favicon.png and
the 800w gallery shots as data URIs, so the file opens anywhere with no
server and no repository checkout.

Usage:
    python3 scripts/render_drafts.py --ref main drafts/homepage-current.html
    python3 scripts/render_drafts.py drafts/homepage-seo.html   # working tree

With --ref, index.html and style.css are read from that git ref; images are
always read from the working tree.
"""

from __future__ import annotations

import argparse
import base64
import mimetypes
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read_source(rel: str, ref: str | None) -> str:
    if ref is None:
        return (ROOT / rel).read_text(encoding="utf-8")
    result = subprocess.run(
        ["git", "show", f"{ref}:{rel}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise SystemExit(f"git show {ref}:{rel} failed: {result.stderr.strip()}")
    return result.stdout


def data_uri(rel: str) -> str:
    path = ROOT / rel.lstrip("/")
    if not path.is_file():
        raise SystemExit(f"missing image: {path}")
    mime, _ = mimetypes.guess_type(path.name)
    if mime is None:
        raise SystemExit(f"unknown media type: {path}")
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def inline_css(css: str) -> str:
    def repl(match: re.Match[str]) -> str:
        return f'url("{data_uri(match.group(1))}")'

    return re.sub(r'url\("(/[^"]+)"\)', repl, css)


def inline_img_tag(tag: str) -> str:
    """Point one <img> at an embedded 800w image and drop srcset/sizes."""
    src = re.search(r'src="([^"]+)"', tag)
    if src is None:
        return tag
    original = src.group(1)
    embedded = original.replace("-1600.jpg", "-800.jpg")
    tag = tag.replace(f'src="{original}"', f'src="{data_uri(embedded)}"')
    tag = re.sub(r'\s+srcset="[^"]*"', "", tag)
    tag = re.sub(r'\s+sizes="[^"]*"', "", tag)
    return tag


def render(ref: str | None) -> str:
    html = read_source("index.html", ref)
    css = inline_css(read_source("style.css", ref))

    html, count = re.subn(
        r'<link rel="stylesheet" href="/style.css">',
        lambda _m: f"<style>\n{css}</style>",
        html,
    )
    if count != 1:
        raise SystemExit("expected exactly one stylesheet link")

    html = re.sub(
        r'<link rel="icon" href="(/[^"]+)">',
        lambda m: f'<link rel="icon" href="{data_uri(m.group(1))}">',
        html,
    )
    html = re.sub(r"<img\b[^>]*>", lambda m: inline_img_tag(m.group(0)), html)
    # Site-relative page links (e.g. /privacy/) must still work from a file.
    html = html.replace('href="/', 'href="https://parchmatte.com/')

    leftover = re.findall(r'(?:src|href)="/(?:images|icon|favicon|grain)[^"]*"', html)
    if leftover:
        raise SystemExit(f"unresolved local asset references: {leftover}")
    return html


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("output", type=Path)
    parser.add_argument("--ref", help="git ref for index.html and style.css")
    args = parser.parse_args(argv)

    html = render(args.ref)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html, encoding="utf-8")
    print(f"wrote {args.output} ({len(html.encode('utf-8')) // 1024} KiB)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
