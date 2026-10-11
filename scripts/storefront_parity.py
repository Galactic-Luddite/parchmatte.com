#!/usr/bin/env python3
"""Check that the app version the site describes matches the Mac App Store.

The site declares one version in three places that must agree on major.minor:

- `release/site-version.json` (`version`, plus `receipt`, the path of the media receipt),
- `softwareVersion` in the home page's JSON-LD,
- the `build` field of the media receipt named there (for example "1.0.0 (21)").

`--declared-only` checks only that these agree. Without it the declared version must
also equal the version Apple's public lookup reports (major.minor, so 1.1 equals
1.1.0); an unreachable or empty lookup fails. Standard library only.

The pure functions take file contents as text so a caller can pass data read from
anywhere (a local checkout, or a pull request's files fetched through the API)
without running any code from that source.
"""

import argparse
import json
from pathlib import Path
import re
import sys
import urllib.request

APP_ID = 6815385110
LOOKUP_URL = f"https://itunes.apple.com/lookup?id={APP_ID}&country=us&entity=macSoftware"
ROOT = Path(__file__).resolve().parents[1]
NUM = r"(?:0|[1-9][0-9]{0,3})"
VERSION_RE = re.compile(rf"{NUM}\.{NUM}(\.{NUM}){{0,2}}")
BUILD_RE = re.compile(rf"({NUM}\.{NUM}(?:\.{NUM}){{0,2}})(?: \([0-9]{{1,6}}\))?")
LD_VERSION_RE = re.compile(r'"softwareVersion"\s*:\s*"([^"]*)"')
RECEIPT_RE = re.compile(r"docs/[A-Za-z0-9._-]+\.json")


def major_minor(version):
    """Return (major, minor) for a dotted version string, else None."""
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        return None
    major, minor = version.split(".")[:2]
    return int(major), int(minor)


def parse_live_version(text):
    """Return the store version from a lookup response, or None when unusable."""
    try:
        data = json.loads(text)
    except (TypeError, ValueError):
        return None
    results = data.get("results") if isinstance(data, dict) else None
    if not isinstance(results, list) or len(results) != 1 or not isinstance(results[0], dict):
        return None
    entry = results[0]
    if entry.get("trackId") != APP_ID or entry.get("kind") != "mac-software":
        return None
    version = entry.get("version")
    return version if major_minor(version) else None


def fetch_live_version():
    try:
        with urllib.request.urlopen(LOOKUP_URL, timeout=30) as response:
            return parse_live_version(response.read(1_000_000).decode("utf-8", "replace"))
    except (OSError, ValueError):
        return None


def parse_site_version(text):
    """Return (version, receipt_path) from release/site-version.json, or (None, None)."""
    try:
        data = json.loads(text)
    except (TypeError, ValueError):
        return None, None
    if not isinstance(data, dict):
        return None, None
    version, receipt = data.get("version"), data.get("receipt")
    if major_minor(version) is None or not isinstance(receipt, str) or not RECEIPT_RE.fullmatch(receipt):
        return None, None
    return version, receipt


def parse_ld_version(index_html):
    """Return softwareVersion from the home page when it appears exactly once."""
    if not isinstance(index_html, str):
        return None
    found = LD_VERSION_RE.findall(index_html)
    return found[0] if len(found) == 1 else None


def parse_receipt_version(text):
    """Return the version part of the receipt's `build` field (for example 1.0.0)."""
    try:
        data = json.loads(text)
    except (TypeError, ValueError):
        return None
    build = data.get("build") if isinstance(data, dict) else None
    found = BUILD_RE.fullmatch(build) if isinstance(build, str) else None
    return found.group(1) if found else None


def declared_problems(site_version_text, index_html, receipt_text):
    """Return (declared_version, problems). Empty problems means all three agree."""
    version, _receipt = parse_site_version(site_version_text)
    if version is None:
        return None, ["release/site-version.json is missing or malformed"]
    problems = []
    declared = major_minor(version)
    ld = parse_ld_version(index_html)
    if major_minor(ld) != declared:
        problems.append(f"home page softwareVersion {ld!r} does not match declared {version}")
    build = parse_receipt_version(receipt_text)
    if major_minor(build) != declared:
        problems.append(f"media receipt build {build!r} does not match declared {version}")
    return version, problems


def triple(version):
    """Return (major, minor, patch) with a missing patch read as 0, else None."""
    if major_minor(version) is None:
        return None
    parts = [int(p) for p in version.split(".")]
    return tuple((parts + [0, 0, 0])[:3])


def compare_live(declared, live):
    """Return 'match', 'behind' (store older than the site), 'ahead' (store newer) or 'unknown'.

    A declared 1.1 equals a store 1.1.0; a store 1.1.1 is ahead of a declared 1.1.
    """
    a, b = triple(declared), triple(live)
    if a is None or b is None:
        return "unknown"
    if a == b:
        return "match"
    return "behind" if b < a else "ahead"


def check_local(root, live, declared_only):
    """Return a list of problems for the checkout at `root`."""
    try:
        site_text = (root / "release/site-version.json").read_text(encoding="utf-8")
        _version, receipt = parse_site_version(site_text)
        if receipt is None:
            return ["release/site-version.json is missing or malformed"]
        index = (root / "index.html").read_text(encoding="utf-8")
        receipt_text = (root / receipt).read_text(encoding="utf-8")
    except OSError as error:
        return [f"could not read declaration files: {error}"]
    version, problems = declared_problems(site_text, index, receipt_text)
    if problems or declared_only:
        return problems
    if live is None:
        return ["the store lookup is unreachable or returned no usable result"]
    relation = compare_live(version, live)
    if relation != "match":
        return [f"site declares {version} but the store has {live} ({relation})"]
    return []


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-root", type=Path, default=ROOT)
    parser.add_argument("--declared-only", action="store_true", help="check only that the declarations agree")
    args = parser.parse_args()
    live = None if args.declared_only else fetch_live_version()
    problems = check_local(args.site_root.resolve(), live, args.declared_only)
    for problem in problems:
        print(f"FAIL: {problem}")
    if problems:
        return 1
    print("PASS: declarations agree" + ("" if args.declared_only else f" and match the store ({live})"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
