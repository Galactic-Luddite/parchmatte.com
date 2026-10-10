# parchmatte.com

The static website for [Parchmatte](https://github.com/Galactic-Luddite/parchmatte):
the home page, the comparison at `/compare/`, the privacy policy at
`/privacy/`, which the app's menu and its App Store listing link to, and the
terms at `/terms/`.

Plain HTML and CSS, with no site build step. Served by GitHub Pages from `main`.

## Website screenshots

The homepage uses current screenshots of Build 21:

- `images/shots/01-overview-build21.png` — Denim on a writing page (2880x1734, cropped to remove the menu bar)
- `images/shots/02-menu-build21.png` — current menu and eight-texture list (2880x1734, cropped to remove the menu bar)
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

`RAW_DIR` holds the six full-screen captures (`01-hero.png` to
`06-schedule.png`) and, for captures with the menu open, `rects.txt`: one line
per capture, `<stem> x0 y0 x1 y1 [x0 y0 x1 y1]`, the menu's and its submenu's
rectangles in points as the accessibility API reported them. The enlarged
panel is cropped from that union, so nothing is positioned by hand.

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

Before publishing, run `python3 scripts/verify_site.py` and
`python3 -m unittest discover -s scripts/tests -v`. The first command checks
the current screenshot file hashes and PNG dimensions plus local references on
the four live pages. GitHub Actions runs these checks and the historical
Build 6 site-image receipt check on pull requests and pushes to `main` or
`task/**` branches. External links and visual appearance still need review.

GitHub Pages serves `main` at `https://parchmatte.com`. After a release-image
change merges, verify the live home page, its image assets and `/privacy/`.

The homepage uses the current Build 21 screenshots listed above. The older
responsive JPEGs in `images/shots/` remain historical Build 6 release media
covered by `docs/release-media-build6.json`; the homepage no longer presents
them as current app screenshots.

Parchmatte 1.0 went on sale on the Mac App Store on 2026-10-07. The home and
comparison pages link to the listing with Apple's "Download on the Mac App
Store" badge (`images/badges/`, black for light mode and white for dark mode,
served unmodified per Apple's marketing guidelines), and the homepage offer
and FAQ structured data describe the $2.99 listing. Keep the structured data
in step with the visible text whenever either changes.

The four pages share `style.css`, header navigation, and footer links. Check
all four in light and dark mode at phone and desktop widths after changing
shared styles. Keyboard users must be able to reach the skip link, navigation,
comparison table, and expandable questions.

## Holding a release

The site must describe what is on the Mac App Store. Copy for a version that is
not out yet goes in a pull request that is held, and a scheduled workflow merges
it once that version is live.

To hold a pull request, make the first line of its description exactly:

`Hold: do not merge until Parchmatte X.Y is live on the Mac App Store.`

`.github/workflows/publish-when-live.yml` runs every 30 minutes (and on demand)
and runs `scripts/publish_when_live.py`. It reads the version on the store from
Apple's public lookup. For each open pull request into `main` that has the hold
line, it squash-merges the pull request only when all of these hold; otherwise
it merges nothing and prints which condition was not met:

- the live version equals the held version (`1.1` matches a store version of `1.1.0`);
- the pull request is not a draft, targets `main`, and its branch is in this
  repository, not a fork;
- its author is an owner, member or collaborator of the repository;
- GitHub reports it mergeable and clean, and every check on the head commit succeeded;
- the newest comment by an owner, member or collaborator that states a reviewed
  head has a line `READY TO MERGE` (and no line with another verdict) and a line
  `Reviewed head: <full 40-character sha>` equal to the pull request's current head.

The merge pins the head sha, so a push after the check cannot slip in, and it
deletes the branch. A new push makes the review stale; post a new review for the
new head. Then the workflow requests a Pages build and reports whether the live
home page changed. That last step is best effort and never fails the run.

To cancel a hold, edit the first line of the description (so it is no longer the
hold line) or convert the pull request to a draft. To see what would happen
without merging, run `python3 scripts/publish_when_live.py --dry-run` (set
`GH_TOKEN` to avoid anonymous rate limits), or run the workflow by hand with its
dry-run input left on (the default for manual runs).

Limits to know about:

- Apple's lookup can lag a release, so the site may trail the store for a while.
- Scheduled runs can be delayed by GitHub, sometimes by many minutes.
- GitHub disables scheduled workflows in a public repository with no activity for
  60 days. A held release that never publishes is the sign. Re-enable the
  workflow from the Actions tab or with `gh workflow enable publish-when-live.yml`.
- A pull request held for a version is merged only when the store version equals
  it. If a later version goes live first, the pull request waits for an edit.

Trust model: only this repository's own scheduled and manual runs act. The
workflow never uses `pull_request_target`, never checks out pull request code
and uses no secrets beyond the run's own token. Fork pull requests never qualify.
A hold line in a pull request from someone without write access is not enough,
because the branch must be in this repository and its author must be an owner,
member or collaborator. A review comment from anyone else is ignored. The store
lookup and all GitHub responses are parsed as data and never reach a shell.
