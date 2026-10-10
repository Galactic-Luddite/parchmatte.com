"""Mutation checks for the website validator, isolated from the real site."""

import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("verify_site", Path(__file__).resolve().parents[1] / "verify_site.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class VerifySiteTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for directory in ("docs", "images/shots", "compare", "privacy", "terms"):
            (self.root / directory).mkdir(parents=True)
        # Header-only fixture: this validator checks identity and IHDR, not PNG decoding.
        self.png = b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + struct.pack(">IIBBBBB", 700, 650, 8, 6, 0, 0, 0) + b"\0" * 4
        self.image = self.root / "images/shots/demo.png"
        self.image.write_bytes(self.png)
        self.receipt = {"images": {"demo.png": {"blob_sha256": hashlib.sha256(self.png).hexdigest(), "width": 700, "height": 650, "color_type": 6}}}
        self.write_receipt()
        (self.root / "index.html").write_text('<img src="/images/shots/demo.png"><a href="/compare/">Compare</a><a href="https://example.com/">External</a><a href="#main">Skip</a>')
        (self.root / "compare/index.html").write_text('<a href="../privacy/">Privacy</a>')
        (self.root / "privacy/index.html").write_text('<a href="/">Home</a>')
        (self.root / "terms/index.html").write_text('<a href="/">Home</a>')

    def write_receipt(self):
        (self.root / "docs/homepage-media-build21.json").write_text(json.dumps(self.receipt))

    def test_valid_site(self):
        self.assertEqual(MODULE.verify(self.root), [])

    def test_changed_image_bytes_fail_hash(self):
        self.image.write_bytes(self.png + b"changed")
        self.assertTrue(any("hash mismatch" in item for item in MODULE.verify(self.root)))

    def test_wrong_dimensions_fail(self):
        self.receipt["images"]["demo.png"]["width"] = 701
        self.write_receipt()
        self.assertTrue(any("dimensions/color mismatch" in item for item in MODULE.verify(self.root)))

    def test_missing_screenshot_fails(self):
        self.image.unlink()
        self.assertTrue(any("missing screenshot" in item for item in MODULE.verify(self.root)))

    def test_missing_relative_link_fails(self):
        (self.root / "compare/index.html").write_text('<a href="missing.html">Missing</a>')
        self.assertTrue(any("missing local reference" in item for item in MODULE.verify(self.root)))

    def test_missing_srcset_asset_fails(self):
        (self.root / "index.html").write_text('<img srcset="/images/shots/demo.png 1x, /missing.png 2x">')
        self.assertTrue(any("missing local reference" in item for item in MODULE.verify(self.root)))

    def test_empty_receipt_fails(self):
        self.receipt["images"] = {}
        self.write_receipt()
        self.assertIn("current screenshot receipt is empty", MODULE.verify(self.root))

    def test_missing_live_page_fails(self):
        (self.root / "privacy/index.html").unlink()
        self.assertIn("missing page: privacy/index.html", MODULE.verify(self.root))

    def test_reference_outside_site_fails(self):
        (self.root / "index.html").write_text('<a href="../outside.html">Outside</a>')
        self.assertTrue(any("escapes site" in item for item in MODULE.verify(self.root)))


if __name__ == "__main__":
    unittest.main()
