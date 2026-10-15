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
                for retired in ("github.com/Galactic-Luddite/", "build-it-yourself", "tip jar", "tip-jar", "MIT License", "MIT licensed"):
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
        self.assertFalse(any(value["@type"] == "FAQPage" for value in schemas))
        website = next(value for value in schemas if value["@type"] == "WebSite")
        self.assertEqual(website["name"], "Parchmatte")
        self.assertEqual(website["url"], "https://parchmatte.com/")
        self.assertNotIn("build it yourself", json.dumps(schemas))

    def test_obsolete_published_drafts_are_absent(self):
        self.assertFalse((ROOT / "drafts/homepage-current.html").exists())
        self.assertFalse((ROOT / "drafts/homepage-seo.html").exists())

    def test_homepage_copy_and_section_sequence(self):
        source = (ROOT / "index.html").read_text()
        self.assertIn("<title>Parchmatte: Paper Texture Overlay for Mac</title>", source)
        self.assertIn("<h1>Paper texture for your Mac.</h1>", source)
        description = "Add paper texture to one window or your whole Mac screen. Adjust the grain and optional Page Light tint. On the Mac App Store. Requires macOS 13+."
        for field in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
            self.assertIn(field + ' content="' + description + '"', source)
        headings = ["One window, with your own paper.", "One window or the whole screen", "Make it your paper.", "Add optional Page Light.", "Set it up for your workspace.", "Paper on a darker screen.", "Compare paper texture and screen tint.", "A few practical details", "Give your Mac a paper texture."]
        self.assertEqual([source.index(value) for value in headings], sorted(source.index(value) for value in headings))
        for retired in ("glare", "eye-care", "No permissions", "About 4 MB", "Nothing to give up", "Velvet"):
            self.assertNotIn(retired, source)
        self.assertIn("Paper texture on a writing window", source)
        self.assertEqual(source.count('alt="Download on the Mac App Store"'), 2)

    def test_metadata_and_shared_navigation(self):
        for name in PAGES:
            source = (ROOT / name).read_text()
            self.assertEqual(len(re.findall(r"<h1[ >]", source)), 1)
            self.assertEqual(source.count("<title>"), 1)
            self.assertEqual(source.count('name="description"'), 1)
            self.assertEqual(source.count('rel="canonical"'), 1)
            self.assertIn('href="/compare/">Compare</a>', source)
            self.assertIn('href="/terms/">Terms</a>', source)
        source = (ROOT / "compare/index.html").read_text()
        for product in ("Parchmatte", "Paperman", "PaperScreen", "Deckle", "Night Shift", "f.lux"):
            self.assertIn("<h3>" + product + "</h3>", source)
        self.assertIn("Vendor-described features; not independently tested", source)
        self.assertNotIn('class="yes"', source)
