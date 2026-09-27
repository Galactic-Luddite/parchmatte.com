#!/usr/bin/env python3
"""Verify the build-bound release-media receipt against retained files."""

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--site-root", type=Path, default=Path("."))
    parser.add_argument("--raw-dir", type=Path)
    parser.add_argument("--store-dir", type=Path)
    parser.add_argument("--app-binary", type=Path)
    parser.add_argument("--site-only", action="store_true")
    args = parser.parse_args()
    receipt = json.loads(args.receipt.read_text())
    if receipt.get("schema") != 1:
        parser.error("unsupported receipt schema")
    if not args.site_only and not all((args.raw_dir, args.store_dir, args.app_binary)):
        parser.error("full verification requires --raw-dir, --store-dir and --app-binary")

    roots = {"site": args.site_root}
    if not args.site_only:
        roots.update(raw=args.raw_dir, store=args.store_dir)
    failures = []
    checked = 0
    for kind, root in roots.items():
        for name, expected in receipt["files"][kind].items():
            path = root / name
            if not path.is_file():
                failures.append(f"missing {kind}/{name}")
                continue
            if sha256(path) != expected:
                failures.append(f"hash mismatch {kind}/{name}")
            checked += 1
    if not args.site_only:
        if sha256(args.app_binary) != receipt["build"]["installed_binary_sha256"]:
            failures.append("installed TestFlight binary hash mismatch")
        checked += 1
    for failure in failures:
        print(f"FAIL: {failure}")
    if failures:
        return 1
    print(f"PASS: {checked} build-6 receipt hashes match")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
