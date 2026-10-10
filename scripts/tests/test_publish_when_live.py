"""Pure-logic tests for the publish-when-live script. No network."""

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location("publish_when_live", SCRIPTS / "publish_when_live.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)

REPO = "Galactic-Luddite/parchmatte.com"
SHA = "a" * 40
OTHER = "b" * 40
HOLD = "Hold: do not merge until Parchmatte 1.1 is live on the Mac App Store."
SITE = json.dumps({"version": "1.1", "receipt": "docs/homepage-media.json"})
INDEX = '{"softwareVersion": "1.1"}'
RECEIPT = json.dumps({"build": "1.1.0 (26)"})
ENTRY = {"pr": 7, "version": "1.1", "head_sha": SHA, "repo": REPO}
RUNS = [{"name": "validate-site", "status": "completed", "conclusion": "success"},
        {"name": "storefront-parity", "status": "completed", "conclusion": "success", "details_url": f"https://github.com/{REPO}/actions/runs/55/job/1"}]
OK_CHECKS = ("ok", "")


def pr(**changes):
    value = {
        "number": 7, "title": "Site: copy for 1.1", "body": HOLD + "\n\nBody.", "state": "open", "merged": False,
        "draft": False, "mergeable": True, "mergeable_state": "clean",
        "base": {"ref": "main", "repo": {"full_name": REPO}},
        "head": {"sha": SHA, "ref": "task/x", "repo": {"full_name": REPO, "fork": False}},
    }
    value.update(changes)
    return value


def decide(entry=ENTRY, pull=None, files=("index.html",), declared="1.1", problems=(), live="1.1.0", checks=OK_CHECKS):
    return M.decide(entry, pull or pr(), list(files), declared, list(problems), live, checks)


class Arming(unittest.TestCase):
    def test_valid(self):
        entries, error = M.parse_held(json.dumps({"held": [{"pr": 7, "version": "1.1", "head_sha": SHA}]}))
        self.assertIsNone(error)
        self.assertEqual(entries, [{"pr": 7, "version": "1.1", "head_sha": SHA}])
        self.assertEqual(M.parse_held('{"held": []}'), ([], None))

    def test_malformed_is_an_error(self):
        good = {"pr": 7, "version": "1.1", "head_sha": SHA}
        bad = [
            "", "not json", "[]", "{}", '{"held": {}}', '{"held": [], "extra": 1}',
            json.dumps({"held": [dict(good, extra=1)]}),
            json.dumps({"held": [{"pr": 7, "version": "1.1"}]}),
            json.dumps({"held": [dict(good, pr="7")]}),
            json.dumps({"held": [dict(good, pr=True)]}),
            json.dumps({"held": [dict(good, pr=0)]}),
            json.dumps({"held": [dict(good, version="1.1.0")]}),
            json.dumps({"held": [dict(good, version="x")]}),
            json.dumps({"held": [dict(good, head_sha=SHA[:12])]}),
            json.dumps({"held": [dict(good, head_sha=SHA.upper())]}),
            json.dumps({"held": [good, good]}),
        ]
        for text in bad:
            entries, error = M.parse_held(text)
            self.assertTrue(error, text)
            self.assertEqual(entries, [])


class HoldLine(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(M.parse_hold_line(HOLD), "1.1")
        self.assertEqual(M.parse_hold_line(HOLD + "\r\nmore"), "1.1")
        for body in (None, "", "\n" + HOLD, "x\n" + HOLD, HOLD.replace("1.1", "1.1.0"), HOLD.replace("1.1", "9" * 5000 + ".1"),
                     HOLD.replace("1.1", "١.١"), HOLD + " x", "> " + HOLD, HOLD.replace("Hold:", "hold:")):
            self.assertIsNone(M.parse_hold_line(body), body)


class GatePaths(unittest.TestCase):
    def test_gate_files_are_refused(self):
        for path in (".github/workflows/ci.yml", ".github/workflows/publish-when-live.yml", "release/held.json",
                     "release/other.json", "scripts/publish_when_live.py", "scripts/storefront_parity.py"):
            self.assertEqual(M.touches_gate(["index.html", path]), [path])

    def test_ordinary_files_and_the_declaration_pass(self):
        self.assertEqual(M.touches_gate(["index.html", "compare/index.html", "scripts/verify_site.py", "release/site-version.json", "README.md"]), [])


class Checks(unittest.TestCase):
    def test_summary(self):
        done = {"status": "completed", "conclusion": "success"}
        self.assertEqual(M.check_summary(RUNS, True)[0], "ok")
        self.assertEqual(M.check_summary([], True)[0], "failed")
        self.assertEqual(M.check_summary([dict(done, name="other")], True)[0], "failed")
        self.assertEqual(M.check_summary([dict(done, name="storefront-parity")], True)[0], "failed")
        self.assertEqual(M.check_summary(RUNS, False)[0], "failed")
        self.assertEqual(M.check_summary(RUNS + [{"name": "validate-site", "status": "in_progress"}], True)[0], "pending")
        for conclusion in ("failure", "skipped", "cancelled", "neutral", None):
            self.assertEqual(M.check_summary(RUNS + [{"name": "validate-site", "status": "completed", "conclusion": conclusion}], True)[0], "failed")

    def test_parity_ignored_by_summary_but_tracked(self):
        failed = [RUNS[0], dict(RUNS[1], conclusion="failure")]
        self.assertEqual(M.check_summary(failed, True)[0], "ok")
        self.assertEqual(M.parity_state(failed), "failed")
        self.assertEqual(M.parity_state(RUNS), "ok")
        self.assertEqual(M.parity_state([RUNS[0]]), "missing")
        self.assertEqual(M.parity_state([RUNS[0], dict(RUNS[1], status="queued")]), "pending")


class Decide(unittest.TestCase):
    def test_merge(self):
        self.assertEqual(decide(), ("merge", []))
        self.assertEqual(decide(live="1.1.1")[0], "merge")

    def test_each_refusal_is_not_yet(self):
        cases = {
            "head moved": pr(head={"sha": OTHER, "ref": "t", "repo": {"full_name": REPO, "fork": False}}),
            "draft": pr(draft=True),
            "base branch": pr(base={"ref": "dev", "repo": {"full_name": REPO}}),
            "base repo": pr(base={"ref": "main", "repo": {"full_name": "x/y"}}),
            "fork": pr(head={"sha": SHA, "ref": "t", "repo": {"full_name": "x/parchmatte.com", "fork": True}}),
            "fork flag": pr(head={"sha": SHA, "ref": "t", "repo": {"full_name": REPO, "fork": True}}),
            "deleted head repo": pr(head={"sha": SHA, "ref": "t", "repo": None}),
            "no hold line": pr(body="Body only"),
            "other version in hold line": pr(body=HOLD.replace("1.1", "1.2")),
            "unknown mergeable": pr(mergeable=None),
            "conflict": pr(mergeable=False, mergeable_state="dirty"),
            "dirty": pr(mergeable_state="dirty"),
        }
        for name, pull in cases.items():
            action, reasons = decide(pull=pull)
            self.assertEqual(action, M.NOT_YET, name)
            self.assertTrue(reasons, name)

    def test_blocked_state_is_left_to_the_merge_api(self):
        self.assertEqual(decide(pull=pr(mergeable_state="blocked"))[0], "merge")
        self.assertEqual(decide(pull=pr(mergeable_state="unstable"))[0], "merge")

    def test_gate_changes_refused(self):
        action, reasons = decide(files=["index.html", ".github/workflows/ci.yml"])
        self.assertEqual(action, M.NOT_YET)
        self.assertIn("publishing gate", reasons[0])
        self.assertEqual(decide(files=["release/held.json"])[0], M.NOT_YET)

    def test_declaration_conditions(self):
        self.assertEqual(decide(declared=None, problems=["unreadable"])[0], M.NOT_YET)
        self.assertEqual(decide(problems=["home page softwareVersion '1.0' does not match"])[0], M.NOT_YET)
        self.assertEqual(decide(declared="1.0")[0], M.NOT_YET)
        self.assertEqual(decide(declared="1.1.0")[0], "merge")

    def test_live_version(self):
        self.assertEqual(decide(live="1.0")[0], M.NOT_YET)
        self.assertEqual(decide(live=None)[0], M.NOT_YET)
        action, reasons = decide(live="1.2.0")
        self.assertEqual(action, M.ERROR)
        self.assertIn("newer", reasons[0])

    def test_checks(self):
        self.assertEqual(decide(checks=("pending", "running"))[0], M.NOT_YET)
        self.assertEqual(decide(checks=("failed", "bad"))[0], M.NOT_YET)

    def test_closed_or_merged_is_done(self):
        self.assertEqual(decide(pull=pr(state="closed"))[0], M.DONE)
        self.assertEqual(decide(pull=pr(merged=True, state="closed"))[0], M.DONE)


class FakeGitHub:
    """Serves one pull request; `fresh` (if given) is returned from the second read of it."""

    def __init__(self, pull=None, fresh=None, files=("index.html",), runs=RUNS, site=SITE, index=INDEX, receipt=RECEIPT, fail=()):
        self.pull, self.fresh, self.files, self.runs = pull or pr(), fresh, list(files), runs
        self.contents = {"release/site-version.json": site, "index.html": index, "docs/homepage-media.json": receipt}
        self.calls, self.fail = [], set(fail)

    def paged(self, path):
        self.calls.append(("paged", path))
        return [{"filename": name} for name in self.files]

    def file_text(self, path, ref):
        self.calls.append(("file", path, ref))
        return self.contents.get(path)

    def request(self, method, path, payload=None):
        self.calls.append((method, path, payload))
        if path in self.fail:
            raise OSError("boom")
        if path.startswith("/commits"):
            return {"check_runs": self.runs, "total_count": len(self.runs)}
        if method == "GET" and path == "/pulls/7":
            reads = [c for c in self.calls if c[0] == "GET" and c[1] == path]
            return self.fresh if self.fresh is not None and len(reads) > 1 else self.pull
        return {}

    def writes(self):
        return [c for c in self.calls if c[0] in ("PUT", "DELETE", "POST")]


class Process(unittest.TestCase):
    def go(self, fake, live="1.1.0", dry_run=False, confirm=True):
        with mock.patch.object(M, "confirm_publication", return_value=confirm) as confirm_mock:
            status = M.process(fake, REPO, {"pr": 7, "version": "1.1", "head_sha": SHA}, live, dry_run)
        return status, confirm_mock

    def test_merges_pinned_to_the_armed_sha(self):
        fake = FakeGitHub()
        status, confirm = self.go(fake)
        self.assertEqual(status, 0)
        merge = [c for c in fake.calls if c[0] == "PUT"][0]
        self.assertEqual(merge[1], "/pulls/7/merge")
        self.assertEqual(merge[2], {"merge_method": "squash", "sha": SHA, "commit_title": "Site: copy for 1.1 (#7)", "commit_message": ""})
        self.assertIn(("DELETE", "/git/refs/heads/task/x", None), fake.calls)
        confirm.assert_called_once()

    def test_files_are_read_at_the_armed_sha_as_data(self):
        fake = FakeGitHub()
        self.go(fake)
        reads = [c for c in fake.calls if c[0] == "file"]
        self.assertEqual({c[2] for c in reads}, {SHA})
        self.assertEqual({c[1] for c in reads}, {"release/site-version.json", "index.html", "docs/homepage-media.json"})

    def test_dry_run_writes_nothing(self):
        fake = FakeGitHub()
        self.assertEqual(self.go(fake, dry_run=True)[0], 0)
        self.assertEqual(fake.writes(), [])

    def test_not_live_yet_writes_nothing(self):
        for live in ("1.0", None):
            fake = FakeGitHub()
            self.assertEqual(self.go(fake, live=live)[0], 0)
            self.assertEqual(fake.writes(), [])

    def test_live_ahead_is_an_error_and_writes_nothing(self):
        fake = FakeGitHub()
        self.assertEqual(self.go(fake, live="1.2")[0], 1)
        self.assertEqual(fake.writes(), [])

    def test_changed_head_is_not_read_or_merged(self):
        moved = pr(head={"sha": OTHER, "ref": "task/x", "repo": {"full_name": REPO, "fork": False}})
        fake = FakeGitHub(pull=moved)
        self.assertEqual(self.go(fake)[0], 0)
        self.assertEqual(fake.writes(), [])
        self.assertEqual([c for c in fake.calls if c[0] == "file"], [])

    def test_gate_changing_pull_request_is_refused(self):
        fake = FakeGitHub(files=["index.html", "release/held.json"])
        self.go(fake)
        self.assertEqual(fake.writes(), [])

    def test_declaration_mismatch_is_refused(self):
        fake = FakeGitHub(index='{"softwareVersion": "1.0"}')
        self.go(fake)
        self.assertEqual(fake.writes(), [])

    def test_missing_declaration_files_are_refused(self):
        for site, index, receipt in ((None, INDEX, RECEIPT), (SITE, None, RECEIPT), (SITE, INDEX, None)):
            fake = FakeGitHub(site=site, index=index, receipt=receipt)
            self.assertEqual(self.go(fake)[0], 0)
            self.assertEqual(fake.writes(), [])

    def test_failed_checks_are_refused(self):
        fake = FakeGitHub(runs=[dict(RUNS[0], conclusion="failure"), RUNS[1]])
        self.go(fake)
        self.assertEqual(fake.writes(), [])

    def test_stale_parity_failure_is_rerun_not_merged(self):
        fake = FakeGitHub(runs=[RUNS[0], dict(RUNS[1], conclusion="failure")])
        self.assertEqual(self.go(fake)[0], 0)
        self.assertEqual(fake.writes(), [("POST", "/actions/runs/55/rerun-failed-jobs", None)])

    def test_missing_or_pending_parity_waits(self):
        for runs in ([RUNS[0]], [RUNS[0], dict(RUNS[1], status="in_progress")]):
            fake = FakeGitHub(runs=runs)
            self.assertEqual(self.go(fake)[0], 0)
            self.assertEqual(fake.writes(), [])

    def test_hold_removed_between_check_and_merge(self):
        fake = FakeGitHub(fresh=pr(body="Hold removed"))
        self.go(fake)
        self.assertEqual([c for c in fake.writes() if c[0] == "PUT"], [])

    def test_head_moved_between_check_and_merge(self):
        fake = FakeGitHub(fresh=pr(head={"sha": OTHER, "ref": "task/x", "repo": {"full_name": REPO, "fork": False}}))
        self.go(fake)
        self.assertEqual([c for c in fake.writes() if c[0] == "PUT"], [])

    def test_failed_merge_is_an_error(self):
        fake = FakeGitHub(fail={"/pulls/7/merge"})
        self.assertEqual(self.go(fake)[0], 1)

    def test_failed_publication_confirmation_is_an_error(self):
        self.assertEqual(self.go(FakeGitHub(), confirm=False)[0], 1)

    def test_closed_pull_request_is_done(self):
        fake = FakeGitHub(pull=pr(state="closed", merged=True))
        self.assertEqual(self.go(fake)[0], 0)
        self.assertEqual(fake.writes(), [])


class Confirm(unittest.TestCase):
    def test_pages_request_failure(self):
        fake = FakeGitHub(fail={"/pages/builds"})
        self.assertFalse(M.confirm_publication(fake, "1.1", attempts=1, pause=0))

    def test_waits_for_the_live_version(self):
        fake = FakeGitHub()
        with mock.patch.object(M, "live_site_version", side_effect=["1.0", "1.1"]), mock.patch.object(M.time, "sleep"):
            self.assertTrue(M.confirm_publication(fake, "1.1", attempts=3, pause=0))
        with mock.patch.object(M, "live_site_version", return_value="1.0"), mock.patch.object(M.time, "sleep"):
            self.assertFalse(M.confirm_publication(fake, "1.1", attempts=2, pause=0))
        with mock.patch.object(M, "live_site_version", return_value=None), mock.patch.object(M.time, "sleep"):
            self.assertFalse(M.confirm_publication(fake, "1.1", attempts=2, pause=0))


class Run(unittest.TestCase):
    def held(self, text):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "held.json"
        if text is not None:
            path.write_text(text)
        return path

    def test_nothing_armed_does_nothing(self):
        with mock.patch.object(M, "GitHub") as github:
            self.assertEqual(M.run(REPO, "t", False, held_path=self.held('{"held": []}'), fetch_live=False), 0)
        github.assert_not_called()

    def test_malformed_or_missing_arming_file_fails_loudly(self):
        self.assertEqual(M.run(REPO, "t", False, held_path=self.held("nope"), fetch_live=False), 1)
        self.assertEqual(M.run(REPO, "t", False, held_path=self.held(None), fetch_live=False), 1)

    def test_only_listed_pull_requests_are_touched(self):
        fake = FakeGitHub()
        text = json.dumps({"held": [{"pr": 7, "version": "1.1", "head_sha": SHA}]})
        with mock.patch.object(M, "GitHub", return_value=fake), mock.patch.object(M, "confirm_publication", return_value=True):
            self.assertEqual(M.run(REPO, "t", False, held_path=self.held(text), live_version="1.1.0"), 0)
        self.assertTrue(all("/pulls/7" in c[1] or c[0] in ("file",) or c[1].startswith(("/commits", "/git/refs", "/actions")) for c in fake.calls if c[0] != "file"))

    def test_error_in_one_entry_does_not_stop_the_next(self):
        fake = FakeGitHub()
        entries = [{"pr": 9, "version": "1.1", "head_sha": OTHER}, {"pr": 7, "version": "1.1", "head_sha": SHA}]
        original = fake.request

        def request(method, path, payload=None):
            if path.startswith("/pulls/9"):
                raise OSError("boom")
            return original(method, path, payload)

        fake.request = request
        with mock.patch.object(M, "GitHub", return_value=fake), mock.patch.object(M, "confirm_publication", return_value=True):
            status = M.run(REPO, "t", False, held_path=self.held(json.dumps({"held": entries})), live_version="1.1.0")
        self.assertEqual(status, 1)
        self.assertTrue([c for c in fake.calls if c[0] == "PUT"])


if __name__ == "__main__":
    unittest.main()
