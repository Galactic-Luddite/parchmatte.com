"""Keep visitor copy and structured data aligned with the App Store product."""

import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
PAGES = ("index.html", "compare/index.html", "privacy/index.html", "terms/index.html", "guides/paper-texture-on-mac/index.html")


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
        self.assertIn("<title>Parchmatte: Paper Texture &amp; Matte Screen Effect for Mac</title>", source)
        self.assertIn('<h1>A softer, matte look for your Mac screen.</h1>', source)
        description = "Give your Mac windows a matte paper texture, a gentle wash of light, or both. Style individual windows or your whole screen from the menu bar."
        for field in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
            self.assertIn(field + ' content="' + description + '"', source)
        headings = ["Your windows. Your look.", "One window or the whole screen", "Light, with or without paper.", "Find your texture.", "Right in your menu bar.", "Fit your workspace.", "Compare paper texture and screen tint.", "A few practical details", "Make your screen feel more like your page."]
        self.assertEqual([source.index(value) for value in headings], sorted(source.index(value) for value in headings))
        for retired in ("glare", "eye-care", "No permissions", "About 4 MB", "Nothing to give up"):
            self.assertNotIn(retired, source)
        shots = re.findall(r'<img class="shot[^"]*" src="/images/shots/([a-z-]+)\.webp" srcset="/images/shots/([a-z0-9-]+\.webp) \d+w, [^"]*" sizes="[^"]*" width="(\d+)" height="(\d+)"', source)
        self.assertEqual(len(shots), 8)
        # Every homepage picture is the same 3:2 shape, with a smaller copy for phones.
        for name, small, width, height in shots:
            self.assertEqual(int(width) * 2, int(height) * 3, name)
            self.assertTrue((ROOT / "images/shots" / small).is_file(), small)
        self.assertEqual(source.count('alt="Download on the Mac App Store"'), 2)

    def test_selected_image_roles_and_full_size_access(self):
        source = (ROOT / "index.html").read_text()
        hero = source.split('<div class="hero">', 1)[1].split('<section id="paper-in-use"', 1)[0]
        for name in ("window-woven", "window-velvet"):
            self.assertIn('src="/images/shots/' + name + '.webp"', hero)
        texture = source.split('aria-labelledby="texture-title">', 1)[1].split('</section>', 1)[0]
        self.assertIn('id="compare"', texture)
        self.assertIn('type="range" min="0" max="100"', texture)
        self.assertNotIn('src="/images/shots/texture-velvet.webp"', source)
        for name in ("window-woven", "window-velvet", "home-plain", "home-velvet", "texture-woven", "texture-denim", "light-candlelight", "menu-textures"):
            self.assertIn('href="/images/shots/' + name + '.webp"', source)
            self.assertTrue((ROOT / "images/shots" / (name + ".webp")).is_file())
        self.assertIn("Native Parchmatte 1.2.2 reference.", source)

    def test_guide_reference_supports_existing_four_steps(self):
        source = (ROOT / "guides/paper-texture-on-mac/index.html").read_text()
        steps = source.split('<ol>', 1)[1].split('</ol>', 1)[0]
        self.assertEqual(len(re.findall(r'<li(?: |>)', steps)), 4)
        self.assertIn('id="step4"', steps)
        adjustment = steps.split('id="step4"', 1)[1]
        self.assertIn('This Window — [app name]', adjustment)
        self.assertIn('src="/images/shots/menu-textures.webp"', adjustment)
        self.assertIn('href="/images/shots/menu-textures.webp"', adjustment)
        self.assertIn('Native Parchmatte 1.2.2 reference.', adjustment)
        self.assertIn('href="/#light-title">see Parchmatte’s texture and Page Light overview</a>', source)

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
