"""Keep visitor copy and structured data aligned with the App Store product."""

import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
PAGES = ("index.html", "compare/index.html", "privacy/index.html", "terms/index.html")


class SitePositioningTests(unittest.TestCase):
    def test_public_pages_have_no_retired_distribution_links(self):
        for name in PAGES:
            with self.subTest(page=name):
                source = (ROOT / name).read_text()
                for retired in ("github.com/", "build-it-yourself", "tip jar", "tip-jar", "MIT License", "MIT licensed"):
                    self.assertNotIn(retired, source)
                self.assertIn('href="mailto:support@parchmatte.com"', source)

    def test_homepage_has_only_store_offer_and_matching_faq(self):
        source = (ROOT / "index.html").read_text()
        schemas = [json.loads(value) for value in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)]
        app = next(value for value in schemas if value["@type"] == "SoftwareApplication")
        self.assertNotIn("codeRepository", app)
        self.assertNotIn("license", app)
        self.assertEqual(len(app["offers"]), 1)
        self.assertIn("apps.apple.com", app["offers"][0]["url"])
        faq = next(value for value in schemas if value["@type"] == "FAQPage")
        for question in faq["mainEntity"]:
            self.assertIn("<summary>" + question["name"] + "</summary>", source)
        self.assertNotIn("build it yourself", json.dumps(schemas))

    def test_obsolete_published_drafts_are_absent(self):
        self.assertFalse((ROOT / "drafts/homepage-current.html").exists())
        self.assertFalse((ROOT / "drafts/homepage-seo.html").exists())
