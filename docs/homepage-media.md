# Homepage media

The homepage's four PNG screenshots were captured on 2026-10-10 from the
installed App Store build of Parchmatte 1.1.0 (26). They show Denim on a writing
page, the menu with the Page Light submenu open, and two texture examples over
a browser-rendered dark terminal demo. The demo contains synthetic sample text.
Both dark examples use strength 0.15, softness 0.35 and Page Light off; only
the texture changes.

| Public file | Size | What it shows |
| --- | --- | --- |
| `images/shots/01-overview.png` | 2880x1800 | Denim at 40% strength over a TextEdit page of sample prose, whole-screen paper |
| `images/shots/02-menu.png` | 2880x1800 | Menu with Strength 40%, Softness 35%, Page Light submenu (Candlelight on, six tints, Glow: Medium, Light Strength 50%) |
| `images/shots/07-woven-terminal.png` | 1400x1300 | Woven, the app's linen texture, on a dark terminal demo |
| `images/shots/08-denim-terminal.png` | 1400x1300 | Denim on a dark terminal demo |

The two full-frame images are direct desktop-compositor captures with only
ancillary PNG metadata removed. The two terminal images are lossless crops,
cut with ffmpeg from 2880x1800 direct captures, then stripped of metadata; the
crop re-encodes the pixels, so their IDAT bytes differ from the capture. The
page displays them at 700x650 CSS pixels, so they are 2x images.

The exact dimensions, pixel hashes, and PNG file hashes are recorded in
[`homepage-media.json`](homepage-media.json). The terminal demo source is
retained at `scripts/fixtures/terminal-demo.html` so the neutral sample content
can be reproduced.

Use `python3 scripts/strip_png_metadata.py INPUT.png OUTPUT.png` to remove
ancillary capture metadata before publication. It preserves the image header
and compressed pixel chunks byte for byte; it does not add or simulate texture.

These files are separate from the historical Build 6 App Store media
documented in `release-media-build6.json`, and are not covered by that
receipt's hashes or GUI-audit record.
