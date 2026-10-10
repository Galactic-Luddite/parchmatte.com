"""Pure-logic tests for the storefront parity check. No network."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("storefront_parity", Path(__file__).resolve().parents[1] / "storefront_parity.py")
P = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(P)

SITE = json.dumps({"version": "1.1", "receipt": "docs/homepage-media.json"})
RECEIPT = json.dumps({"build": "1.1.0 (26)"})
INDEX = '<script type="application/ld+json">{"softwareVersion": "1.1"}</script>'


def lookup(**changes):
    entry = {"trackId": P.APP_ID, "kind": "mac-software", "version": "1.1.0"}
    entry.update(changes)
    return json.dumps({"resultCount": 1, "results": [entry]})


class Versions(unittest.TestCase):
    def test_major_minor(self):
        self.assertEqual(P.major_minor("1.1"), (1, 1))
        self.assertEqual(P.major_minor("1.1.0"), (1, 1))
        self.assertEqual(P.major_minor("1.1.1"), (1, 1))
        self.assertEqual(P.major_minor("1.10"), (1, 10))
        self.assertEqual(P.triple("1.1"), (1, 1, 0))
        self.assertEqual(P.triple("1.1.2"), (1, 1, 2))
        for bad in (None, "", "1", "1.1 beta", "1.1;x", "9" * 5000 + ".1", "١.١", "1.1.1.1.1", "1.01", "01.1", "1.1\n", 1.1):
            self.assertIsNone(P.major_minor(bad), bad)

    def test_compare_live(self):
        self.assertEqual(P.compare_live("1.1", "1.1.0"), "match")
        self.assertEqual(P.compare_live("1.1", "1.1.1"), "ahead")
        self.assertEqual(P.compare_live("1.1.1", "1.1.1"), "match")
        self.assertEqual(P.compare_live("1.1.1", "1.1"), "behind")
        self.assertEqual(P.compare_live("1.1", "1.0"), "behind")
        self.assertEqual(P.compare_live("1.1", "1.2"), "ahead")
        self.assertEqual(P.compare_live("1.1", "1.10"), "ahead")
        self.assertEqual(P.compare_live("1.1", "2.0"), "ahead")
        self.assertEqual(P.compare_live("1.1", None), "unknown")
        self.assertEqual(P.compare_live(None, "1.1"), "unknown")


class Lookup(unittest.TestCase):
    def test_good(self):
        self.assertEqual(P.parse_live_version(lookup()), "1.1.0")

    def test_failures_are_unknown(self):
        two = json.loads(lookup())
        two["results"].append(two["results"][0])
        for text in (None, "", "not json", "[]", json.dumps({"results": []}), json.dumps({"results": "x"}),
                     json.dumps(two), lookup(trackId=1), lookup(kind="software"), lookup(version=None),
                     lookup(version=11), lookup(version="1.1; echo x"), lookup(version="9" * 5000)):
            self.assertIsNone(P.parse_live_version(text), text)


class Declarations(unittest.TestCase):
    def test_site_version_file(self):
        self.assertEqual(P.parse_site_version(SITE), ("1.1", "docs/homepage-media.json"))
        for bad in ("", "[]", "{}", json.dumps({"version": "1.1"}),
                    json.dumps({"version": "x", "receipt": "docs/a.json"}),
                    json.dumps({"version": "1.1", "receipt": "../a.json"}),
                    json.dumps({"version": "1.1", "receipt": "docs/../../a.json"}),
                    json.dumps({"version": "1.1", "receipt": "/absolute.json"}),
                    json.dumps({"version": "1.1", "receipt": "docs/a.txt"})):
            self.assertEqual(P.parse_site_version(bad), (None, None), bad)

    def test_ld_version_must_appear_once(self):
        self.assertEqual(P.parse_ld_version(INDEX), "1.1")
        self.assertIsNone(P.parse_ld_version("no version"))
        self.assertIsNone(P.parse_ld_version(INDEX + INDEX))
        self.assertIsNone(P.parse_ld_version(None))

    def test_receipt_build(self):
        self.assertEqual(P.parse_receipt_version(RECEIPT), "1.1.0")
        self.assertEqual(P.parse_receipt_version(json.dumps({"build": "1.0"})), "1.0")
        for bad in ("", "[]", "{}", json.dumps({"build": "release"}), json.dumps({"build": 1})):
            self.assertIsNone(P.parse_receipt_version(bad), bad)

    def test_agreement(self):
        self.assertEqual(P.declared_problems(SITE, INDEX, RECEIPT), ("1.1", []))
        _, problems = P.declared_problems(SITE, INDEX.replace("1.1", "1.0"), RECEIPT)
        self.assertEqual(len(problems), 1)
        _, problems = P.declared_problems(SITE, INDEX, json.dumps({"build": "1.0.0 (21)"}))
        self.assertEqual(len(problems), 1)
        _, problems = P.declared_problems("{}", INDEX, RECEIPT)
        self.assertEqual(problems, ["release/site-version.json is missing or malformed"])
        self.assertEqual(P.declared_problems(SITE, "", RECEIPT)[1][0][:25], "home page softwareVersion")


class Local(unittest.TestCase):
    def make(self, site=SITE, index=INDEX, receipt=RECEIPT):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        (root / "release").mkdir()
        (root / "docs").mkdir()
        (root / "release/site-version.json").write_text(site)
        (root / "index.html").write_text(index)
        (root / "docs/homepage-media.json").write_text(receipt)
        return root

    def test_match_declared_only_and_live(self):
        root = self.make()
        self.assertEqual(P.check_local(root, "1.1.0", False), [])
        self.assertEqual(P.check_local(root, None, True), [])

    def test_fails_closed(self):
        root = self.make()
        self.assertTrue(P.check_local(root, None, False))
        self.assertTrue(P.check_local(root, "1.0", False))
        self.assertTrue(P.check_local(root, "1.2", False))
        self.assertTrue(P.check_local(self.make(index=INDEX.replace("1.1", "1.0")), "1.1.0", True))
        self.assertTrue(P.check_local(self.make(site="{}"), "1.1.0", False))
        self.assertTrue(P.check_local(Path(tempfile.gettempdir()) / "does-not-exist", "1.1.0", False))


if __name__ == "__main__":
    unittest.main()
