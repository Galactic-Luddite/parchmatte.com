#!/usr/bin/env python3
"""Merge an armed website pull request once the version it describes is live.

Arming comes only from `release/held.json` on `main`:

    {"held": [{"pr": 24, "version": "1.1", "head_sha": "<40 hex>"}]}

Nothing else can cause a merge: not a comment, not a pull request description, not
a label. A pull request is merged only at exactly the listed head sha, and only when
every condition in `decide` holds. Run from a checkout of `main`; pull request files
are read through the API as data and no pull request code is ever run.

Exit status is non-zero for anything that needs a person to notice: a malformed
arming file, a store version newer than the held one, a failed merge, a failed
Pages build request, or a live site that does not show the new version in time.
A store outage or a store version older than the held one is simply "not yet".
Never reverts anything. Standard library only.
"""

import argparse
import base64
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import storefront_parity as parity

API = "https://api.github.com"
SITE_URL = "https://parchmatte.com/"
ROOT = Path(__file__).resolve().parents[1]
HOLD_RE = re.compile(r"^Hold: do not merge until Parchmatte ([0-9]{1,4}\.[0-9]{1,4}) is live on the Mac App Store\.$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
GATE_PREFIXES = (".github/", "release/")
GATE_FILES = ("scripts/publish_when_live.py", "scripts/storefront_parity.py")
DECLARATION_FILE = "release/site-version.json"
PARITY_CHECK = "storefront-parity"
VALIDATE_CHECK = "validate-site"
NOT_YET, DONE, ERROR = "not-yet", "done", "error"


def parse_held(text):
    """Return (entries, error) from the text of release/held.json."""
    try:
        data = json.loads(text)
    except (TypeError, ValueError):
        return [], "release/held.json is not valid JSON"
    held = data.get("held") if isinstance(data, dict) and set(data) == {"held"} else None
    if not isinstance(held, list):
        return [], 'release/held.json must be {"held": [...]}'
    entries, seen = [], set()
    for item in held:
        if not isinstance(item, dict) or set(item) != {"pr", "version", "head_sha"}:
            return [], "each held entry needs exactly pr, version and head_sha"
        number, version, sha = item["pr"], item["version"], item["head_sha"]
        if type(number) is not int or number < 1 or number in seen:
            return [], "held entry has a bad or duplicate pr number"
        if not isinstance(version, str) or not re.match(r"^[0-9]{1,4}\.[0-9]{1,4}$", version):
            return [], "held entry version must look like X.Y"
        if not isinstance(sha, str) or not SHA_RE.match(sha):
            return [], "held entry head_sha must be 40 lowercase hex characters"
        seen.add(number)
        entries.append({"pr": number, "version": version, "head_sha": sha})
    return entries, None


def parse_hold_line(body):
    """Return X.Y from a description whose first line is the hold line, else None."""
    if not isinstance(body, str):
        return None
    match = HOLD_RE.match(body.replace("\r\n", "\n").split("\n", 1)[0].rstrip())
    return match.group(1) if match else None


def touches_gate(paths):
    """Return the changed paths a held pull request may not touch.

    The publisher, its parity check, the workflows and the arming file define the
    gate; a pull request cannot change them on its way to being merged. The one
    allowed file under release/ is the site's own version declaration.
    """
    blocked = []
    for path in paths:
        if path == DECLARATION_FILE:
            continue
        if path.startswith(GATE_PREFIXES) or path in GATE_FILES:
            blocked.append(path)
    return blocked


def check_summary(check_runs, complete):
    """Return (state, detail) for the non-parity checks: 'ok', 'pending' or 'failed'."""
    runs = [run for run in check_runs if run.get("name") != PARITY_CHECK]
    if not complete or not any(run.get("name") == VALIDATE_CHECK for run in runs):
        return "failed", f"no complete set of checks including {VALIDATE_CHECK} on the head commit"
    if any(run.get("status") != "completed" for run in runs):
        return "pending", "checks are still running"
    if any(run.get("conclusion") != "success" for run in runs):
        return "failed", "a check on the head commit did not succeed"
    return "ok", ""


def decide(entry, pr, files, declared, problems, live, checks):
    """Return (action, reasons) for one armed entry.

    action is 'merge', NOT_YET (wait quietly), DONE (nothing to do) or ERROR (needs a
    person). `checks` is the (state, detail) pair from check_summary.
    """
    if pr.get("merged") or pr.get("state") != "open":
        return DONE, ["pull request is no longer open"]
    reasons = []
    head = pr.get("head") or {}
    base = pr.get("base") or {}
    head_repo = head.get("repo") or {}
    if head.get("sha") != entry["head_sha"]:
        reasons.append("pull request head is not the armed sha")
    if pr.get("draft"):
        reasons.append("pull request is a draft")
    if base.get("ref") != "main" or (base.get("repo") or {}).get("full_name") != entry["repo"]:
        reasons.append("base is not main of this repository")
    if head_repo.get("full_name") != entry["repo"] or head_repo.get("fork"):
        reasons.append("head branch is not in this repository")
    if parse_hold_line(pr.get("body")) != entry["version"]:
        reasons.append("description does not start with the matching hold line")
    blocked = touches_gate(files)
    if blocked:
        reasons.append("pull request changes the publishing gate: " + ", ".join(sorted(blocked)[:5]))
    if declared is None or problems:
        reasons.extend(problems or ["site version declaration is unreadable"])
    elif parity.major_minor(declared) != parity.major_minor(entry["version"]):
        reasons.append(f"pull request declares {declared}, armed for {entry['version']}")
    if pr.get("mergeable") is not True or pr.get("mergeable_state") == "dirty":
        reasons.append(f"not mergeable (mergeable={pr.get('mergeable')}, state={pr.get('mergeable_state')})")
    relation = parity.compare_live(entry["version"], live)
    if relation == "ahead":
        return ERROR, [f"the store has {live}, newer than the held {entry['version']}; update or disarm the entry"]
    if relation != "match":
        reasons.append(f"live version is {live if live else 'unknown'}, held for {entry['version']}")
    if reasons:
        return NOT_YET, reasons
    state, detail = checks
    if state != "ok":
        return NOT_YET, [detail]
    return "merge", []


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

    def file_text(self, path, ref):
        quoted = urllib.parse.quote(path, safe="/")
        try:
            info = self.request("GET", f"/contents/{quoted}?ref={ref}")
        except urllib.error.HTTPError as error:
            if error.code == 404:
                return None
            raise
        if not isinstance(info, dict) or info.get("encoding") != "base64":
            raise ValueError("unexpected file response")
        return base64.b64decode(info["content"]).decode("utf-8")


def live_site_version():
    """Return softwareVersion from the live home page, or None."""
    try:
        with urllib.request.urlopen(f"{SITE_URL}?nocache={int(time.time())}", timeout=30) as response:
            return parity.parse_ld_version(response.read(5_000_000).decode("utf-8", "replace"))
    except OSError:
        return None


def confirm_publication(gh, version, attempts=20, pause=30):
    """Request a Pages build and wait for the live site to declare `version`."""
    try:
        gh.request("POST", "/pages/builds")
        print("Requested a GitHub Pages build.")
    except (OSError, ValueError) as error:
        print(f"ERROR: could not request a Pages build ({error}). Pushes made with the workflow token do not start a branch-based Pages build.")
        return False
    for _ in range(attempts):
        time.sleep(pause)
        seen = live_site_version()
        if parity.major_minor(seen) == parity.major_minor(version):
            print(f"Live site now declares {seen}.")
            return True
    print(f"ERROR: the live site did not show version {version} within {attempts * pause} seconds. Check the Pages build.")
    return False


def rerun_parity(gh, runs):
    """Re-run stale failed storefront-parity checks; return True if one was started."""
    started = False
    for run in runs:
        if run.get("name") == PARITY_CHECK and run.get("status") == "completed" and run.get("conclusion") != "success":
            match = re.search(r"/actions/runs/([0-9]+)(?:/|$)", run.get("details_url") or "")
            if match:
                gh.request("POST", f"/actions/runs/{match.group(1)}/rerun-failed-jobs")
                started = True
    return started


def parity_state(runs):
    """Return 'ok', 'pending' or 'failed' for the storefront-parity check runs."""
    own = [run for run in runs if run.get("name") == PARITY_CHECK]
    if not own:
        return "missing"
    if any(run.get("status") != "completed" for run in own):
        return "pending"
    return "ok" if all(run.get("conclusion") == "success" for run in own) else "failed"


def process(gh, repo, entry, live, dry_run):
    """Handle one armed entry. Returns an exit status (0 fine, 1 needs attention)."""
    number = entry["pr"]
    entry = dict(entry, repo=repo)
    pr = gh.request("GET", f"/pulls/{number}")
    sha = (pr.get("head") or {}).get("sha", "")
    files = [item.get("filename", "") for item in gh.paged(f"/pulls/{number}/files")]
    declared = problems = None
    if sha == entry["head_sha"]:
        site_text = gh.file_text(DECLARATION_FILE, sha)
        _version, receipt = parity.parse_site_version(site_text)
        if receipt is None:
            declared, problems = None, ["release/site-version.json is missing or malformed on the head"]
        else:
            index_text, receipt_text = gh.file_text("index.html", sha), gh.file_text(receipt, sha)
            if index_text is None or receipt_text is None:
                declared, problems = None, ["the home page or the media receipt named by the declaration is missing on the head"]
            else:
                declared, problems = parity.declared_problems(site_text, index_text, receipt_text)
    page = gh.request("GET", f"/commits/{sha}/check-runs?per_page=100")
    runs = page.get("check_runs", [])
    complete = page.get("total_count", len(runs)) == len(runs)
    action, reasons = decide(entry, pr, files, declared, problems, live, check_summary(runs, complete))
    if action == DONE:
        print(f"#{number}: {reasons[0]}; the entry can be removed from release/held.json")
        return 0
    if action == ERROR:
        print(f"#{number}: ERROR: {reasons[0]}")
        return 1
    if action == NOT_YET:
        print(f"#{number}: armed for {entry['version']}, not merging:")
        for reason in reasons:
            print(f"  - {reason}")
        return 0
    state = parity_state(runs)
    if state != "ok":
        if dry_run:
            print(f"#{number}: dry run, all conditions met but the {PARITY_CHECK} check is {state}; would re-run it")
            return 0
        if state == "failed" and rerun_parity(gh, runs):
            print(f"#{number}: re-ran the {PARITY_CHECK} check; merging on a later run")
        else:
            print(f"#{number}: waiting for the {PARITY_CHECK} check ({state})")
        return 0
    title = f"{pr.get('title', '')} (#{number})"
    if dry_run:
        print(f"#{number}: dry run, would squash-merge head {sha} as {title!r} and delete branch {pr['head']['ref']}")
        return 0
    fresh = gh.request("GET", f"/pulls/{number}")
    if fresh["head"]["sha"] != entry["head_sha"] or parse_hold_line(fresh.get("body")) != entry["version"]:
        print(f"#{number}: changed while checking, doing nothing")
        return 0
    try:
        gh.request("PUT", f"/pulls/{number}/merge", {"merge_method": "squash", "sha": entry["head_sha"], "commit_title": title, "commit_message": ""})
    except (OSError, ValueError) as error:
        print(f"#{number}: ERROR: merge failed: {error}")
        return 1
    print(f"#{number}: merged head {sha} as {title!r}")
    try:
        ref = urllib.parse.quote(pr["head"]["ref"], safe="/")
        gh.request("DELETE", f"/git/refs/heads/{ref}")
        print(f"#{number}: deleted branch {pr['head']['ref']}")
    except (OSError, ValueError) as error:
        print(f"#{number}: could not delete branch ({error})")
    return 0 if confirm_publication(gh, entry["version"]) else 1


def run(repo, token, dry_run, held_path=None, live_version=None, fetch_live=True):
    held_path = held_path or ROOT / "release/held.json"
    try:
        text = held_path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"ERROR: cannot read the arming file: {error}")
        return 1
    entries, error = parse_held(text)
    if error:
        print(f"ERROR: {error}")
        return 1
    if not entries:
        print("Nothing is armed in release/held.json.")
        return 0
    live = live_version if live_version is not None else (parity.fetch_live_version() if fetch_live else None)
    print(f"Live version on the Mac App Store: {live if live else 'unknown'}")
    gh = GitHub(token, repo)
    status = 0
    for entry in entries:
        try:
            status |= process(gh, repo, entry, live, dry_run)
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
            print(f"#{entry['pr']}: ERROR: could not complete ({error})")
            status = 1
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
