# parchmatte.com

The static website for [Parchmatte](https://github.com/Galactic-Luddite/parchmatte):
the home page, the comparison at `/compare/`, and the privacy policy at
`/privacy/`, which the app's menu and its App Store listing link to.

Plain HTML and CSS, with no site build step. Served by GitHub Pages from `main`.

## Release screenshots

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

The homepage uses three release screenshots: the overview, menu controls, and
per-window view. All release image files remain covered by the media receipt.

When the app is live, update the availability text on the home and comparison
pages, add the App Store link, and update the homepage offer and FAQ structured
data to match the visible content. Until then, only the free source build is
listed as an offer.

The three pages share `style.css`, header navigation, and footer links. Check
all three in light and dark mode at phone and desktop widths after changing
shared styles. Keyboard users must be able to reach the skip link, navigation,
comparison table, and expandable questions.
