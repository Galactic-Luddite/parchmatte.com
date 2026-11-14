"""Exact visitor copy and preservation checks for the proposed site text."""
import hashlib
import html
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = json.loads(Path(__file__).with_name('site_copy_expected.json').read_text())


def text(value):
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', '', value)).split())


def blocks(source):
    return [text(m[2]) for m in re.finditer(r'<(p|h1|h2|summary)(?:\s[^>]*)?>(.*?)</\1>', source, re.S)]


def protected(source):
    """Retain visual assets, behavior, navigation, legal and competitor content."""
    patterns = (r'<title>.*?</title>', r'<style\b.*?</style>',
                r'<script(?! type="application/ld\+json")\b.*?</script>',
                r'<figure\b.*?</figure>', r'<(?:img|source|link)\b[^>]*>',
                r'<nav\b.*?</nav>', r'<footer\b.*?</footer>',
                r'<div class="download">.*?</div>',
                r'<div class="alternative"><h3>(?!Parchmatte).*?</div></div>',
                r'<section class="comparison".*?</section>')
    return '\n'.join(m.group() for pattern in patterns for m in re.finditer(pattern, source, re.S))


class ExactSiteCopyTests(unittest.TestCase):
    def test_all_exact_copy_blocks(self):
        for row in EXPECTED['blocks']:
            with self.subTest(block=row['id']):
                actual = blocks((ROOT / row['file']).read_text())
                wanted = row['paragraphs']
                self.assertTrue(any(actual[i:i + len(wanted)] == wanted for i in range(len(actual))), row['id'])

    def test_metadata_and_schema(self):
        for row in EXPECTED['metadata']:
            source = (ROOT / row['file']).read_text()
            self.assertIn('<title>' + html.escape(row['title_after']) + '</title>', source)
            for field in row['fields']:
                match = re.search(r'(?:name|property)="' + re.escape(field) + r'" content="([^"]*)"', source)
                self.assertIsNotNone(match)
                self.assertEqual(html.unescape(match[1]), row['description_after'])
        schemas = [json.loads(value) for value in re.findall(r'<script type="application/ld\+json">(.*?)</script>', (ROOT / 'index.html').read_text(), re.S)]
        app = next(value for value in schemas if value['@type'] == 'SoftwareApplication')
        self.assertEqual(app, EXPECTED['app_schema'])

    def test_protected_content_and_release_receipts(self):
        for name, digest in EXPECTED['protected'].items():
            self.assertEqual(hashlib.sha256(protected((ROOT / name).read_text()).encode()).hexdigest(), digest, name)
        for name, digest in EXPECTED['receipts'].items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest, name)
        source = (ROOT / 'guides/paper-texture-on-mac/index.html').read_text()
        self.assertNotIn('Parchmatte’s menu again', source)
        self.assertNotIn('Parchmatte’s menu,', source)
        self.assertIn('Open Parchmatte’s controls in the menu bar.', source)
        steps = source.split('<ol>', 1)[1].split('</ol>', 1)[0]
        self.assertEqual(len(re.findall(r'<li(?: |>)', steps)), 4)
        self.assertIn('<li id="step4"><p><strong>Adjust that window’s paper.</strong>', steps)
        self.assertEqual(source.count('<a href="/">Parchmatte</a>'), 1)
