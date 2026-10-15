"""Check approved icon identity, declarations and crawler access."""

import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import struct
import unittest
from urllib.robotparser import RobotFileParser

ROOT = Path(__file__).resolve().parents[2]


class IconLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.icons = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "link" and attributes.get("rel") in {"icon", "apple-touch-icon"}:
            self.icons.append(attributes)


class SiteIconTests(unittest.TestCase):
    def test_approved_assets_and_all_advertised_dimensions(self):
        receipt = json.loads((ROOT / "docs/site-icons.json").read_text())
        self.assertEqual(set(receipt["assets"]), {"icon.png", "favicon.png"})
        for name, expected in receipt["assets"].items():
            data = (ROOT / name).read_bytes()
            position = 8
            while position < len(data):
                length = struct.unpack(">I", data[position:position + 4])[0]
                self.assertIn(data[position + 4:position + 8], (b"IHDR", b"IDAT", b"IEND"))
                position += length + 12
            self.assertEqual(position, len(data))
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(hashlib.sha256(data).hexdigest(), expected["blob_sha256"])
            self.assertEqual(struct.unpack(">II", data[16:24]), (expected["width"], expected["height"]))
            self.assertEqual(expected["width"], expected["height"])
        robots = RobotFileParser()
        robots.parse((ROOT / "robots.txt").read_text().splitlines())
        self.assertTrue(robots.can_fetch("Googlebot", "https://parchmatte.com/"))
        for page in ("index.html", "compare/index.html", "privacy/index.html", "terms/index.html"):
            parser = IconLinks()
            parser.feed((ROOT / page).read_text())
            self.assertEqual(len(parser.icons), 3, page)
            self.assertEqual({link["href"] for link in parser.icons}, {"/icon.png", "/favicon.png"})
            for link in parser.icons:
                name = link["href"].lstrip("/")
                expected = receipt["assets"][name]
                self.assertEqual(link["sizes"], f'{expected["width"]}x{expected["height"]}')
                self.assertTrue(robots.can_fetch("Googlebot-Image", "https://parchmatte.com" + link["href"]))
            self.assertTrue(any(link["rel"] == "icon" and link["href"] == "/icon.png" for link in parser.icons))


if __name__ == "__main__":
    unittest.main()
