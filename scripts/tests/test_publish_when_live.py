"""Pure-logic tests for the publish-when-live script. No network."""

import importlib.util
import json
from pathlib import Path
import unittest
from unittest import mock

SPEC = importlib.util.spec_from_file_location("publish_when_live", Path(__file__).resolve().parents[1] / "publish_when_live.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)

REPO = "Galactic-Luddite/parchmatte.com"
SHA = "a" * 40
OTHER = "b" * 40
HOLD = "Hold: do not merge until Parchmatte 1.1 is live on the Mac App Store."


def pr(**changes):
    value = {
        "number": 7,
        "title": "Site: copy for 1.1",
        "body": HOLD + "\n\nBody.",
        "draft": False,
        "author_association": "MEMBER",
        "mergeable": True,
        "mergeable_state": "clean",
        "base": {"ref": "main", "repo": {"full_name": REPO}},
        "head": {"sha": SHA, "ref": "task/x", "repo": {"full_name": REPO, "fork": False}},
    }
    value.update(changes)
    return value


def comment(body, association="MEMBER", created="2026-10-10T10:00:00Z"):
    return {"body": body, "author_association": association, "created_at": created}


GOOD_RUNS = [{"status": "completed", "conclusion": "success"}]
GOOD_REVIEW = [comment(f"VERDICT: READY TO MERGE\nReviewed head: {SHA} (matches)")]


def lookup(**changes):
    entry = {"trackId": M.APP_ID, "kind": "mac-software", "version": "1.1.0", "trackName": "Parchmatte"}
    entry.update(changes)
    return json.dumps({"resultCount": 1, "results": [entry]})


class HoldLine(unittest.TestCase):
    def test_exact_first_line(self):
        self.assertEqual(M.parse_hold_line(HOLD), "1.1")
        self.assertEqual(M.parse_hold_line(HOLD + "\r\nmore"), "1.1")
        self.assertEqual(M.parse_hold_line(HOLD.replace("1.1", "12.30")), "12.30")

    def test_rejects_other_forms(self):
        for body in (
            None,
            "",
            "\n" + HOLD,
            "Intro\n" + HOLD,
            HOLD.replace("Hold:", "hold:"),
            HOLD.replace("1.1", "1"),
            HOLD.replace("1.1", "1.1.0"),
            HOLD[:-1],
            HOLD + " extra",
            "> " + HOLD,
            HOLD.replace("Parchmatte 1.1", "Parchmatte 1.1; rm -rf"),
        ):
            self.assertIsNone(M.parse_hold_line(body), body)


class Versions(unittest.TestCase):
    def test_equality_with_padding(self):
        self.assertTrue(M.version_matches("1.1", "1.1.0"))
        self.assertTrue(M.version_matches("1.1", "1.1"))
        self.assertFalse(M.version_matches("1.1", "1.0"))
        self.assertFalse(M.version_matches("1.1", "1.10"))
        self.assertFalse(M.version_matches("1.1", "1.1.1"))
        self.assertFalse(M.version_matches("1.1", "1.1 beta"))
        self.assertFalse(M.version_matches("1.1", None))

    def test_lookup_parsing(self):
        self.assertEqual(M.parse_live_version(lookup()), "1.1.0")

    def test_lookup_failures_are_unknown(self):
        for text in (
            "",
            "not json",
            "[]",
            json.dumps({"results": []}),
            json.dumps({"results": [{}, {}]}),
            json.dumps({"results": "x"}),
            lookup(trackId=1),
            lookup(kind="software"),
            lookup(version="1.1; echo x"),
            lookup(version=None),
            lookup(version=11),
            None,
        ):
            self.assertIsNone(M.parse_live_version(text), text)
        two = json.loads(lookup())
        two["results"].append(two["results"][0])
        self.assertIsNone(M.parse_live_version(json.dumps(two)))


class Verdicts(unittest.TestCase):
    def test_ready(self):
        self.assertEqual(M.parse_verdict(f"## Verdict: READY TO MERGE (held)\n\nReviewed head: {SHA}"), ("READY TO MERGE", SHA))
        self.assertEqual(M.parse_verdict(f"VERDICT: READY TO MERGE\nReviewed head: {SHA.upper()}"), ("READY TO MERGE", SHA))

    def test_not_ready_if_any_line_disagrees(self):
        self.assertEqual(M.parse_verdict(f"READY TO MERGE\nCHANGES REQUESTED\nReviewed head: {SHA}")[0], "NOT READY")
        self.assertEqual(M.parse_verdict(f"CHANGES REQUESTED\nReviewed head: {SHA}")[0], "NOT READY")

    def test_prose_does_not_count(self):
        self.assertEqual(M.parse_verdict(f"This is not READY TO MERGE yet\nReviewed head: {SHA}"), (None, None))
        self.assertEqual(M.parse_verdict(f"NOT READY TO MERGE\nReviewed head: {SHA}"), (None, None))

    def test_head_must_be_one_full_sha(self):
        self.assertEqual(M.parse_verdict("READY TO MERGE\nReviewed head: " + SHA[:12])[1], None)
        self.assertEqual(M.parse_verdict(f"READY TO MERGE\nReviewed head: {SHA}\nReviewed head: {OTHER}")[1], None)

    def test_latest_trusted_review_wins(self):
        comments = [
            comment(f"READY TO MERGE\nReviewed head: {SHA}", created="2026-10-10T10:00:00Z"),
            comment(f"CHANGES REQUESTED\nReviewed head: {SHA}", created="2026-10-10T11:00:00Z"),
        ]
        self.assertEqual(M.latest_review(comments)[0], "NOT READY")

    def test_untrusted_and_headless_comments_ignored(self):
        comments = [
            comment(f"READY TO MERGE\nReviewed head: {SHA}", created="2026-10-10T10:00:00Z"),
            comment(f"CHANGES REQUESTED\nReviewed head: {SHA}", association="NONE", created="2026-10-10T12:00:00Z"),
            comment("CHANGES REQUESTED, see below", created="2026-10-10T13:00:00Z"),
        ]
        self.assertEqual(M.latest_review(comments), ("READY TO MERGE", SHA))
        self.assertEqual(M.latest_review([]), (None, None))


class Evaluate(unittest.TestCase):
    def check(self, pull=None, live="1.1.0", runs=GOOD_RUNS, statuses=(), comments=GOOD_REVIEW):
        return M.evaluate(pull or pr(), REPO, live, runs, list(statuses), comments)

    def test_all_met(self):
        self.assertEqual(self.check(), [])

    def test_no_hold_line_never_qualifies(self):
        self.assertEqual(len(self.check(pr(body="Body only"))), 1)
        self.assertEqual(len(self.check(pr(body=None))), 1)

    def test_each_refusal(self):
        cases = {
            "author": pr(author_association="NONE"),
            "draft": pr(draft=True),
            "base branch": pr(base={"ref": "dev", "repo": {"full_name": REPO}}),
            "base repo": pr(base={"ref": "main", "repo": {"full_name": "x/y"}}),
            "fork head": pr(head={"sha": SHA, "ref": "t", "repo": {"full_name": "someone/parchmatte.com", "fork": True}}),
            "fork flag": pr(head={"sha": SHA, "ref": "t", "repo": {"full_name": REPO, "fork": True}}),
            "deleted head repo": pr(head={"sha": SHA, "ref": "t", "repo": None}),
            "unknown mergeable": pr(mergeable=None),
            "conflict": pr(mergeable=False, mergeable_state="dirty"),
            "behind": pr(mergeable_state="behind"),
            "unstable": pr(mergeable_state="unstable"),
        }
        for name, pull in cases.items():
            self.assertTrue(self.check(pull), name)

    def test_live_version(self):
        self.assertEqual(self.check(live="1.0"), ["live version is 1.0, held for 1.1"])
        self.assertEqual(self.check(live=None), ["live version is unknown"])

    def test_checks(self):
        self.assertTrue(self.check(runs=[]))
        self.assertTrue(self.check(runs=[{"status": "in_progress", "conclusion": None}]))
        self.assertTrue(self.check(runs=GOOD_RUNS + [{"status": "completed", "conclusion": "failure"}]))
        self.assertTrue(self.check(runs=[{"status": "completed", "conclusion": "skipped"}]))
        self.assertTrue(self.check(statuses=[{"state": "failure"}]))
        self.assertEqual(self.check(statuses=[{"state": "success"}]), [])

    def test_review_conditions(self):
        self.assertTrue(self.check(comments=[]))
        self.assertTrue(self.check(comments=[comment(f"READY TO MERGE\nReviewed head: {SHA}", association="NONE")]))
        self.assertTrue(self.check(comments=[comment(f"READY TO MERGE\nReviewed head: {SHA}", association="CONTRIBUTOR")]))
        self.assertTrue(self.check(comments=[comment(f"READY TO MERGE\nReviewed head: {OTHER}")]))
        self.assertTrue(self.check(comments=[comment("READY TO MERGE")]))
        self.assertEqual(self.check(comments=[comment(f"READY TO MERGE\nReviewed head: {SHA}", association="COLLABORATOR")]), [])

    def test_stale_review_after_new_push(self):
        pull = pr(head={"sha": OTHER, "ref": "t", "repo": {"full_name": REPO, "fork": False}})
        self.assertEqual(self.check(pull), ["latest trusted review is for a different head than the current one"])


class FakeGitHub:
    def __init__(self, pulls, fresh=None):
        self.pulls, self.fresh, self.calls = pulls, fresh, []

    def paged(self, path):
        self.calls.append(("paged", path))
        return self.pulls if path.startswith("/pulls") else GOOD_REVIEW

    def request(self, method, path, payload=None):
        self.calls.append((method, path, payload))
        if path.startswith("/commits") and path.endswith("check-runs?per_page=100"):
            return {"check_runs": GOOD_RUNS}
        if path.startswith("/commits"):
            return {"statuses": []}
        if method == "GET":
            return self.fresh or pr()
        return {}


class RunFlow(unittest.TestCase):
    def run_flow(self, fake, live, dry_run=False):
        with mock.patch.object(M, "GitHub", return_value=fake), mock.patch.object(M, "report_publication"), mock.patch.object(M, "home_page_digest", return_value="x"):
            return M.run(REPO, "token", dry_run, live_version=live)

    def writes(self, fake):
        return [call for call in fake.calls if call[0] in ("PUT", "DELETE", "POST")]

    def test_merges_when_everything_holds(self):
        fake = FakeGitHub([pr()])
        self.assertEqual(self.run_flow(fake, "1.1.0"), 0)
        merge = [c for c in fake.calls if c[0] == "PUT"][0]
        self.assertEqual(merge[1], "/pulls/7/merge")
        self.assertEqual(merge[2], {"merge_method": "squash", "sha": SHA, "commit_title": "Site: copy for 1.1 (#7)", "commit_message": ""})
        self.assertIn(("DELETE", "/git/refs/heads/task/x", None), fake.calls)

    def test_dry_run_writes_nothing(self):
        fake = FakeGitHub([pr()])
        self.run_flow(fake, "1.1.0", dry_run=True)
        self.assertEqual(self.writes(fake), [])

    def test_wrong_version_or_unknown_writes_nothing(self):
        for live in ("1.0", None):
            fake = FakeGitHub([pr()])
            self.run_flow(fake, live)
            self.assertEqual(self.writes(fake), [])

    def test_pr_without_hold_line_is_untouched(self):
        fake = FakeGitHub([pr(body="No hold")])
        self.run_flow(fake, "1.1.0")
        self.assertEqual(fake.calls, [("paged", "/pulls?state=open&base=main")])

    def test_head_moved_between_check_and_merge(self):
        moved = pr(head={"sha": OTHER, "ref": "task/x", "repo": {"full_name": REPO, "fork": False}})
        fake = FakeGitHub([pr()], fresh=moved)
        self.run_flow(fake, "1.1.0")
        self.assertEqual(self.writes(fake), [])

    def test_hold_removed_between_check_and_merge(self):
        fake = FakeGitHub([pr()], fresh=pr(body="Hold removed"))
        self.run_flow(fake, "1.1.0")
        self.assertEqual(self.writes(fake), [])


if __name__ == "__main__":
    unittest.main()
