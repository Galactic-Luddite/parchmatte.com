# parchmatte.com

The static website for [Parchmatte](https://github.com/Galactic-Luddite/parchmatte):
the home page, the comparison at `/compare/`, and the privacy policy at
`/privacy/`, which the app's menu and its App Store listing link to.

Plain HTML and CSS, with no site build step. Served by GitHub Pages from `main`.

## Website screenshots

The homepage uses current screenshots of Build 21:

- `images/shots/01-overview-build21.png` — Denim on a writing page
- `images/shots/02-menu-build21.png` — current menu and eight-texture list
- `images/shots/07-woven-terminal.png` — Woven on a dark terminal demo
- `images/shots/08-denim-terminal.png` — Denim on a dark terminal demo

These PNGs show the current app but are not part of the Build 6 App Store media
audit or its hash receipt. Their dimensions and pixel and file hashes are in
`docs/homepage-media-build21.json`, with a readable summary in
`docs/homepage-media-build21.md`. The synthetic terminal page used in the two
texture examples is retained at `scripts/fixtures/terminal-demo.html`.

## Historical Build 6 release media

The 12 release image files and `images/og.jpg` are rendered from six unmodified
screen captures of TestFlight build 1.0.0 (6), whose installed binary passed
the full store GUI audit. The captioned 2880×1800 PNGs are uploaded to App
Store Connect. The larger menu panels are crops of the same capture, never
recreated interface elements. `docs/release-media-build6.json` records the
source commit, installed binary hash, audit run and SHA-256 hashes of all raw,
store and committed site images. The raw and store files are retained locally
through review; they are not served by this website.

Keep the raw captures and store PNGs locally through review. To regenerate,
install Pillow and run:

```sh
python3 scripts/render_release_shots.py RAW_DIR STORE_DIR images/shots
swift scripts/check_release_shots.swift STORE_DIR images/shots
python3 scripts/verify_release_media.py docs/release-media-build6.json \
  --raw-dir RAW_DIR --store-dir STORE_DIR \
  --app-binary /Applications/Parchmatte.app/Contents/MacOS/Parchmatte
```

For a checkout without the retained local files, run the receipt's committed
image check with `python3 scripts/verify_release_media.py
docs/release-media-build6.json --site-only`.

The OCR check requires the approved build 6 labels in the final store and
website images and rejects retired labels. Inspect each image visually too;
the check only covers text it can recognize.

## Publishing

GitHub Pages serves `main` at `https://parchmatte.com`. After a release-image
change merges, verify the live home page, its image assets and `/privacy/`.

The homepage uses the current Build 21 screenshots listed above. The older
responsive JPEGs in `images/shots/` remain historical Build 6 release media
covered by `docs/release-media-build6.json`; the homepage no longer presents
them as current app screenshots.

When the app is live, update the availability text on the home and comparison
pages, add the App Store link, and update the homepage offer and FAQ structured
data to match the visible content. Until then, only the free source build is
listed as an offer.

The three pages share `style.css`, header navigation, and footer links. Check
all three in light and dark mode at phone and desktop widths after changing
shared styles. Keyboard users must be able to reach the skip link, navigation,
comparison table, and expandable questions.
