#!/usr/bin/env python3
"""Merge a held website pull request once the version it describes is live.

A pull request is held by making the FIRST line of its description exactly:

    Hold: do not merge until Parchmatte X.Y is live on the Mac App Store.

This script reads the version on the Mac App Store from Apple's public lookup
and squash-merges a held pull request only when every condition in
`evaluate` holds. It uses the standard library only. Run with `--dry-run` to
print what it would do without changing anything.

All data from the lookup and from GitHub is treated as untrusted text: it is
parsed with regular expressions and JSON, never passed to a shell.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

APP_ID = 6815385110
LOOKUP_URL = f"https://itunes.apple.com/lookup?id={APP_ID}&country=us&entity=macSoftware"
SITE_URL = "https://parchmatte.com/"
API = "https://api.github.com"
TRUSTED_ASSOCIATIONS = frozenset({"OWNER", "MEMBER", "COLLABORATOR"})

HOLD_RE = re.compile(r"^Hold: do not merge until Parchmatte (\d+\.\d+) is live on the Mac App Store\.$")
VERSION_RE = re.compile(r"^\d+(\.\d+){0,3}$")
VERDICT_RE = re.compile(r"^(?:verdict:\s*)?(READY TO MERGE|CHANGES REQUESTED|BLOCKED|HUMAN ESCALATION REQUIRED)\b", re.IGNORECASE)
HEAD_RE = re.compile(r"^reviewed head:\s*([0-9a-f]{40})\b", re.IGNORECASE)
MARKDOWN_PREFIX_RE = re.compile(r"^[\s#>*_`-]+")


def parse_hold_line(body):
    """Return X.Y from a description whose first line is the hold line, else None."""
    if not isinstance(body, str):
        return None
    first = body.replace("\r\n", "\n").split("\n", 1)[0].rstrip()
    match = HOLD_RE.match(first)
    return match.group(1) if match else None


def _numbers(version):
    return [int(part) for part in version.split(".")]


def version_matches(held, live):
    """True when two dotted versions are equal after zero padding (1.1 == 1.1.0)."""
    if not isinstance(held, str) or not isinstance(live, str):
        return False
    if not VERSION_RE.match(held) or not VERSION_RE.match(live):
        return False
    a, b = _numbers(held), _numbers(live)
    size = max(len(a), len(b))
    return a + [0] * (size - len(a)) == b + [0] * (size - len(b))


def parse_live_version(text):
    """Return the store version from a lookup response, or None when unusable."""
    try:
        data = json.loads(text)
    except (TypeError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    results = data.get("results")
    if not isinstance(results, list) or len(results) != 1 or not isinstance(results[0], dict):
        return None
    entry = results[0]
    if entry.get("trackId") != APP_ID or entry.get("kind") != "mac-software":
        return None
    version = entry.get("version")
    if not isinstance(version, str) or not VERSION_RE.match(version):
        return None
    return version


def parse_verdict(body):
    """Return (verdict, reviewed_head) from a review comment body.

    The verdict is READY TO MERGE only when at least one verdict line exists and
    every verdict line says so. reviewed_head is None unless exactly one distinct
    full 40-character sha is stated.
    """
    if not isinstance(body, str):
        return None, None
    verdicts, heads = [], set()
    for raw in body.replace("\r\n", "\n").split("\n"):
        line = MARKDOWN_PREFIX_RE.sub("", raw).strip()
        found = VERDICT_RE.match(line)
        if found:
            verdicts.append(found.group(1).upper())
        head = HEAD_RE.match(line)
        if head:
            heads.add(head.group(1).lower())
    if not verdicts:
        return None, None
    verdict = "READY TO MERGE" if all(v == "READY TO MERGE" for v in verdicts) else "NOT READY"
    return verdict, (next(iter(heads)) if len(heads) == 1 else None)


def latest_review(comments):
    """Return (verdict, head) of the newest trusted comment that states a reviewed head."""
    chosen = None
    for comment in comments:
        if not isinstance(comment, dict) or comment.get("author_association") not in TRUSTED_ASSOCIATIONS:
            continue
        body = comment.get("body")
        if not isinstance(body, str) or not any(HEAD_RE.match(MARKDOWN_PREFIX_RE.sub("", l).strip()) for l in body.splitlines()):
            continue
        if chosen is None or comment.get("created_at", "") >= chosen.get("created_at", ""):
            chosen = comment
    if chosen is None:
        return None, None
    return parse_verdict(chosen["body"])


def checks_succeeded(check_runs, statuses):
    """True when at least one check run exists, every one completed successfully,
    and every legacy commit status (if any) is a success."""
    if not check_runs:
        return False
    if any(run.get("status") != "completed" or run.get("conclusion") != "success" for run in check_runs):
        return False
    return all(item.get("state") == "success" for item in statuses)


def evaluate(pr, repo, live, check_runs, statuses, comments):
    """Return the list of unmet conditions for a held pull request (empty means merge)."""
    unmet = []
    held = parse_hold_line(pr.get("body"))
    if held is None:
        return ["description does not start with the hold line"]
    if pr.get("author_association") not in TRUSTED_ASSOCIATIONS:
        unmet.append("author is not an owner, member or collaborator")
    if pr.get("draft"):
        unmet.append("pull request is a draft")
    base = pr.get("base") or {}
    if base.get("ref") != "main" or (base.get("repo") or {}).get("full_name") != repo:
        unmet.append("base is not main of this repository")
    head = pr.get("head") or {}
    head_repo = head.get("repo") or {}
    if head_repo.get("full_name") != repo or head_repo.get("fork"):
        unmet.append("head branch is not in this repository")
    if live is None:
        unmet.append("live version is unknown")
    elif not version_matches(held, live):
        unmet.append(f"live version is {live}, held for {held}")
    if pr.get("mergeable") is not True or pr.get("mergeable_state") != "clean":
        unmet.append(f"not mergeable and clean (mergeable={pr.get('mergeable')}, state={pr.get('mergeable_state')})")
    if not checks_succeeded(check_runs, statuses):
        unmet.append("checks on the head commit have not all succeeded")
    verdict, reviewed = latest_review(comments)
    head_sha = head.get("sha")
    if verdict != "READY TO MERGE":
        unmet.append("latest trusted review does not say READY TO MERGE")
    elif reviewed != head_sha:
        unmet.append("latest trusted review is for a different head than the current one")
    return unmet


class GitHub:
    def __init__(self, token, repo):
        self.token = token
        self.repo = repo

    def request(self, method, path, payload=None):
        data = None if payload is None else json.dumps(payload).encode()
        req = urllib.request.Request(
            f"{API}/repos/{self.repo}{path}",
            data=data,
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                **({"Authorization": f"Bearer {self.token}"} if self.token else {}),
                **({"Content-Type": "application/json"} if data else {}),
            },
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            text = response.read().decode()
        return json.loads(text) if text else None

    def paged(self, path):
        items, page = [], 1
        while True:
            sep = "&" if "?" in path else "?"
            chunk = self.request("GET", f"{path}{sep}per_page=100&page={page}")
            if not isinstance(chunk, list):
                raise ValueError("unexpected response")
            items.extend(chunk)
            if len(chunk) < 100:
                return items
            page += 1


def fetch_live_version():
    try:
        with urllib.request.urlopen(LOOKUP_URL, timeout=30) as response:
            return parse_live_version(response.read(1_000_000).decode("utf-8", "replace"))
    except (OSError, ValueError):
        return None


def home_page_digest():
    try:
        url = f"{SITE_URL}?nocache={int(time.time())}"
        with urllib.request.urlopen(url, timeout=30) as response:
            return hashlib.sha256(response.read(5_000_000)).hexdigest()
    except OSError:
        return None


def report_publication(gh, before):
    """Request a Pages build and watch the home page for a change. Never fatal."""
    try:
        gh.request("POST", "/pages/builds")
        print("Requested a GitHub Pages build.")
    except (OSError, ValueError) as error:
        print(f"Could not request a Pages build ({error}); the push itself normally triggers one.")
    for _ in range(8):
        time.sleep(30)
        after = home_page_digest()
        if before and after and after != before:
            print("Live home page changed.")
            return
    print("Live home page has not visibly changed yet; Pages or caching may still be catching up.")


def run(repo, token, dry_run, live_version=None):
    gh = GitHub(token, repo)
    live = live_version if live_version is not None else fetch_live_version()
    print(f"Live version on the Mac App Store: {live if live else 'unknown'}")
    try:
        pulls = gh.paged("/pulls?state=open&base=main")
    except (OSError, ValueError) as error:
        print(f"Could not list pull requests: {error}")
        return 1
    status = 0
    for summary in pulls:
        number = summary.get("number")
        held = parse_hold_line(summary.get("body"))
        if held is None:
            print(f"#{number}: skip, no hold line")
            continue
        try:
            pr = gh.request("GET", f"/pulls/{number}")
            sha = (pr.get("head") or {}).get("sha", "")
            runs = gh.request("GET", f"/commits/{sha}/check-runs?per_page=100").get("check_runs", [])
            statuses = gh.request("GET", f"/commits/{sha}/status").get("statuses", [])
            comments = gh.paged(f"/issues/{number}/comments")
        except (OSError, ValueError, AttributeError) as error:
            print(f"#{number}: held for {held}, could not read state ({error}); doing nothing")
            continue
        unmet = evaluate(pr, repo, live, runs, statuses, comments)
        if unmet:
            print(f"#{number}: held for {held}, not merging:")
            for item in unmet:
                print(f"  - {item}")
            continue
        title = f"{pr.get('title', '')} (#{number})"
        if dry_run:
            print(f"#{number}: dry run, would squash-merge head {sha} as {title!r} and delete branch {pr['head']['ref']}")
            continue
        before = home_page_digest()
        try:
            fresh = gh.request("GET", f"/pulls/{number}")
            if parse_hold_line(fresh.get("body")) is None or fresh["head"]["sha"] != sha:
                print(f"#{number}: changed while checking, doing nothing")
                continue
            gh.request("PUT", f"/pulls/{number}/merge", {"merge_method": "squash", "sha": sha, "commit_title": title, "commit_message": ""})
            print(f"#{number}: merged head {sha} as {title!r}")
        except (OSError, ValueError, KeyError) as error:
            print(f"#{number}: merge failed: {error}")
            status = 1
            continue
        try:
            ref = urllib.parse.quote(pr["head"]["ref"], safe="/")
            gh.request("DELETE", f"/git/refs/heads/{ref}")
            print(f"#{number}: deleted branch {pr['head']['ref']}")
        except (OSError, ValueError) as error:
            print(f"#{number}: could not delete branch ({error})")
        report_publication(gh, before)
    return status


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", "Galactic-Luddite/parchmatte.com"))
    parser.add_argument("--dry-run", action="store_true", help="print what would happen without changing anything")
    args = parser.parse_args()
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not args.dry_run and not token:
        print("A GITHUB_TOKEN is required unless --dry-run is used.")
        return 1
    return run(args.repo, token, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
