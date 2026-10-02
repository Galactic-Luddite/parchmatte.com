# Homepage media — Build 21

The homepage's four PNG screenshots are direct desktop-compositor captures of
Parchmatte Build 21. They show Denim on a writing page, the current menu, and two
texture examples over a browser-rendered dark terminal demo. The demo contains
synthetic sample text. Both dark examples use strength 0.15, softness 0.35 and
Page Light off; only the texture changes.

| Public file | What it shows |
| --- | --- |
| `images/shots/01-overview-build21.png` | Build 21 Denim texture on a writing page |
| `images/shots/02-menu-build21.png` | Build 21 menu with all eight texture names |
| `images/shots/07-woven-terminal.png` | Woven, the app's linen texture, on a dark terminal demo |
| `images/shots/08-denim-terminal.png` | Denim on a dark terminal demo |

The exact dimensions, pixel hashes, and PNG file hashes are recorded in
[`homepage-media-build21.json`](homepage-media-build21.json). The terminal demo
source is retained at `scripts/fixtures/terminal-demo.html` so the neutral sample
content can be reproduced.

Use `python3 scripts/strip_png_metadata.py INPUT.png OUTPUT.png` to remove
ancillary capture metadata before publication. This preserves the image header
and compressed pixel chunks byte for byte; it does not add or simulate texture.

These files are current homepage captures, separate from the historical Build 6
App Store media documented in `release-media-build6.json`. They are not covered
by that receipt's hashes or GUI-audit record.
