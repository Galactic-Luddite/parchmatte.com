"""Check approved icon identity, declarations and crawler access."""

import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import struct
import unittest
from urllib.robotparser import RobotFileParser
import zlib

ROOT = Path(__file__).resolve().parents[2]
ASSET_SIZES = {
    "icon.png": 1024,
    "favicon.png": 32,
    "favicon-48.png": 48,
    "favicon-96.png": 96,
    "favicon-192.png": 192,
    "apple-touch-icon.png": 180,
}
PAGES = ("index.html", "compare/index.html", "privacy/index.html", "terms/index.html",
         "guides/paper-texture-on-mac/index.html")


def validate_icon(data, expected, size):
    """Reject changed bytes, dimensions, metadata and malformed PNG containers."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("PNG signature")
    position = 8
    chunks = []
    while position < len(data):
        if position + 12 > len(data):
            raise ValueError("truncated PNG chunk")
        length = struct.unpack(">I", data[position:position + 4])[0]
        end = position + length + 12
        if end > len(data):
            raise ValueError("truncated PNG payload")
        kind = data[position + 4:position + 8]
        payload = data[position + 8:end - 4]
        if kind not in (b"IHDR", b"IDAT", b"IEND"):
            raise ValueError("ancillary PNG metadata")
        crc = struct.unpack(">I", data[end - 4:end])[0]
        if zlib.crc32(kind + payload) != crc:
            raise ValueError("PNG CRC")
        chunks.append((kind, payload))
        position = end
    kinds = [kind for kind, _ in chunks]
    if (len(kinds) < 3 or kinds[0] != b"IHDR" or kinds[-1] != b"IEND"
            or any(kind != b"IDAT" for kind in kinds[1:-1])
            or len(chunks[0][1]) != 13 or chunks[-1][1]):
        raise ValueError("PNG chunk structure")
    if struct.unpack(">II", chunks[0][1][:8]) != (size, size):
        raise ValueError("PNG dimensions")
    if (expected["width"], expected["height"]) != (size, size):
        raise ValueError("receipt dimensions")
    if hashlib.sha256(data).hexdigest() != expected["blob_sha256"]:
        raise ValueError("PNG hash")


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
        self.assertEqual(receipt["approved_source_sha256"],
                         "34a9b62dc6c85b5c441cd7fa12ceebe160ac566d7bcd304400ed18625c68216c")
        self.assertEqual(receipt["approved_master_sha256"],
                         "6b2389d6603ae0f7cca390e97e6f84a299e35fa8b389826d2cd96c8350c643c2")
        self.assertEqual(set(receipt["assets"]), set(ASSET_SIZES))
        robots = RobotFileParser()
        robots.parse((ROOT / "robots.txt").read_text().splitlines())
        for name, size in ASSET_SIZES.items():
            with self.subTest(asset=name):
                validate_icon((ROOT / name).read_bytes(), receipt["assets"][name], size)
                for crawler in ("Googlebot", "Googlebot-Image"):
                    self.assertTrue(robots.can_fetch(crawler, "https://parchmatte.com/" + name))
        for page in PAGES:
            with self.subTest(page=page):
                self.assertTrue(robots.can_fetch("Googlebot", "https://parchmatte.com/" + page))
                parser = IconLinks()
                parser.feed((ROOT / page).read_text())
                declarations = {(link["rel"], link["href"], link.get("sizes")) for link in parser.icons}
                self.assertEqual(len(parser.icons), 3)
                self.assertEqual(declarations, {
                    ("icon", "/favicon.png", "32x32"),
                    ("icon", "/icon.png", "1024x1024"),
                    ("apple-touch-icon", "/icon.png", "1024x1024"),
                })
                for link in parser.icons:
                    if link["rel"] == "icon":
                        self.assertEqual(link.get("type"), "image/png")

    def test_controlled_corruption_is_rejected(self):
        receipt = json.loads((ROOT / "docs/site-icons.json").read_text())
        expected = receipt["assets"]["favicon.png"]
        data = (ROOT / "favicon.png").read_bytes()
        validate_icon(data, expected, 32)
        metadata = b"tEXt" + b"Comment\x00unexpected metadata"
        chunk = struct.pack(">I", len(metadata) - 4) + metadata + struct.pack(">I", zlib.crc32(metadata))
        cases = {
            "hash": (data, dict(expected, blob_sha256="0" * 64), 32, "PNG hash"),
            "dimensions": (data, expected, 48, "PNG dimensions"),
            "metadata": (data[:-12] + chunk + data[-12:], expected, 32, "ancillary PNG metadata"),
            "truncation": (data[:-1], expected, 32, "truncated PNG chunk"),
            "trailing bytes": (data + b"x", expected, 32, "truncated PNG chunk"),
        }
        for label, (corrupt, manifest, size, reason) in cases.items():
            with self.subTest(corruption=label), self.assertRaisesRegex(ValueError, reason):
                validate_icon(corrupt, manifest, size)


if __name__ == "__main__":
    unittest.main()
