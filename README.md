# parchmatte.com

The static website for [Parchmatte](https://parchmatte.com/):
the home page, the comparison at `/compare/`, the privacy policy at
`/privacy/`, which the app's menu and its App Store listing link to, and the
terms at `/terms/`, plus the single-window guide at
`/guides/paper-texture-on-mac/`.

Plain HTML and CSS, with no site build step. Served by GitHub Pages from `main`.

## Website screenshots

The held 1.2.1 candidate combines actual pre-submission Parchmatte 1.2.1 (28)
captures with explicitly retained 1.2.0 (27) and 1.1.0 (26) examples:

- `images/shots/01-overview.png` — independently styled windows in the same app (1920x970, 1.2.1)
- `images/shots/10-light-shape-controls.png` — actual native shape and position menu controls (635x804, 1.2.1)
- `images/shots/09-velvet-writing.png` — whole-screen Velvet at 15% Strength and 35% Softness (1440x900, 1.2)
- `images/shots/02-menu.png` — nine-texture menu with Velvet selected; Candlelight on (1920x1048, 1.2)
- `images/shots/07-woven-terminal.png` and `08-denim-terminal.png` — retained 1.1 dark terminal examples (1400x1300)

Per-image build, settings, source identity, transformations, dimensions and file
hashes are recorded in `docs/homepage-media.json`; see `docs/homepage-media.md`.
The synthetic terminal fixture is `scripts/fixtures/terminal-demo.html`. These
images are separate from the historical Build 6 App Store media receipt.

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
the five live pages. GitHub Actions runs these checks and the historical
Build 6 site-image receipt check on pull requests and pushes to `main` or
`task/**` branches. External links and visual appearance still need review.

GitHub Pages serves `main` at `https://parchmatte.com`. After a release-image
change merges, verify the live home page, its image assets and `/privacy/`.

The held homepage uses the mixed-release screenshots listed above. The older
responsive JPEGs in `images/shots/` remain historical Build 6 release media
covered by `docs/release-media-build6.json`; the homepage no longer presents
them as current app screenshots.

This 1.2.1 candidate must remain held until the corresponding app version is live
and owner review is complete. The home and
comparison pages link to the listing with Apple's "Download on the Mac App
Store" badge (`images/badges/`, black for light mode and white for dark mode,
served unmodified per Apple's marketing guidelines), and the homepage offer
and FAQ structured data describe the $2.99 listing. Keep the structured data
in step with the visible text whenever either changes.

The five pages share `style.css`, header navigation, and footer links. Check
all five in light and dark mode at phone and desktop widths after changing
shared styles. Keyboard users must be able to reach the skip link, navigation,
comparison table, and expandable questions.

## Holding a release

The site must describe what is on the Mac App Store. Release gates compare the
major, minor and patch numbers, with a missing patch read as zero: `1.2` equals
`1.2.0`, while `1.2.1` requires that exact patch in the declarations and live store.
Arming entries and hold lines accept `X.Y` or `X.Y.Z`. Copy for a version that is
not out yet goes in a pull request that is held, and a scheduled workflow merges
it once that version is live. Only an entry in `release/held.json` on `main` can
arm a merge. A comment, a label or a pull request description cannot.

What the site declares:

- `release/site-version.json` names the app version the site describes (`version`,
  for example `1.0`) and the media receipt for that version (`receipt`).
- `softwareVersion` in the home page's structured data and the `build` field of that
  receipt must agree with it on major.minor.
- `python3 scripts/storefront_parity.py` checks that they agree and that the declared
  version equals the version Apple's public lookup reports for the app (1.1 matches
  1.1.0; a store version of 1.1.1 is newer than a declared 1.1 and fails). It fails when
  the lookup is unreachable or returns nothing.
  `--declared-only` checks only that the three declarations agree; the main CI job
  runs that, and a separate `storefront-parity` job runs the full check.

How to hold a release:

1. Prepare the release copy in a pull request. It declares the new version in
   `release/site-version.json`, the home page and its receipt. Make the first line of
   its description exactly `Hold: do not merge until Parchmatte X.Y is live on the Mac App Store.`
   (a notice for people; the publisher requires it to be present and to match, but it
   does not arm anything). The pull request may not change `.github/`, `release/`
   (other than `release/site-version.json`) or the two publishing scripts.
2. Arm it in a second, small pull request that adds an entry to `release/held.json`:
   `{"pr": N, "version": "X.Y", "head_sha": "<the 40-character head of pull request N>"}`.
   That pull request changes nothing a visitor sees. Merging it is the decision to
   publish automatically.
3. Any later push to the held pull request leaves it unmerged until the entry is
   updated with the new head.

To disarm, remove the entry from `release/held.json` on `main`, or close the pull
request. Entries for merged or closed pull requests do nothing and can be deleted.

`.github/workflows/publish-when-live.yml` runs `scripts/publish_when_live.py` every
30 minutes and on demand (manual runs default to a dry run; it only ever acts from
`main`). For each entry it merges only when all of these hold, and otherwise prints
exactly which condition was not met:

- the pull request is open, not a draft, targets `main`, its branch is in this
  repository (not a fork), and its head is exactly the armed sha;
- the first line of its description is the matching hold line;
- it does not change the publishing gate (see above, renames included);
- the declared version, the home page and the receipt at that head agree and equal
  the armed version (read through the API as data; no pull request code runs);
- the store version equals the armed version as Apple's lookup reports it right now
  (1.1 matches 1.1.0);
- GitHub reports it conflict-free, a `validate-site` check succeeded on the head and
  no other GitHub Actions check failed or is still running, and a `storefront-parity`
  check succeeded on the head (check runs from other integrations are ignored). That check fails on a held pull request until release, so the publisher
  re-runs a stale failure at decision time and merges on a later run.

The merge pins the armed sha, uses the subject "<title> (#N)" and deletes the
branch. Afterwards the publisher requests a Pages build and waits up to ten minutes
for the live home page to declare the new version, and fails the run if it does not.

If the store version is newer than the armed one (for example 1.1.1 or 1.2 is live while
1.1 is armed), the run fails on purpose so someone notices; update or remove the entry.
An outage, an empty lookup (a pulled release) or an older store version only means
"not yet"; the publisher never reverts anything.

Limits and settings:

- Apple's lookup is cached and can lag a release by hours, so the site may trail the
  store.
- Scheduled runs can be delayed by GitHub.
- GitHub disables scheduled workflows in a public repository with no activity for 60
  days. A held release that never publishes is the sign. Re-enable it from the Actions
  tab or with `gh workflow enable publish-when-live.yml`.
- Pushes and merges made with the workflow token do not start a branch-based Pages
  build by themselves, so the workflow requests one explicitly. If that request
  fails, or the live site does not change, the run fails.
- Making `validate-site` and `storefront-parity` required status checks on `main` is
  a repository setting the repository owner changes. Until then the publisher checks
  them itself; no setting is needed for it to work. With `storefront-parity` required,
  a held pull request cannot be merged by hand before release either.
- The publisher trusts the `validate-site` result that the pull request's own workflow
  run reports. A held pull request cannot edit the workflow files, but it can edit the
  validators and tests that job runs (`scripts/verify_site.py` and the tests), so that
  check is evidence from reviewed content, not an independent control. The declaration
  check is repeated by the publisher itself from main's code. Requiring `validate-site`
  as a status check does not change this.

Trust model: only this repository's own scheduled and manual runs act, with a token
limited to the permissions the one job lists. The job runs only when the workflow is
run from `main`; someone with write access could still run a modified copy of the
workflow from another branch, so write access is the boundary. The publisher runs with
`python3 -I` and imports its one sibling module after the standard library, so a file
added under `scripts/` cannot shadow a standard module. The workflow never uses
`pull_request_target`, never checks out pull request code, uses no secrets and no
third-party actions, and uses the one first-party action pinned by commit. Fork pull
requests never qualify. The store response and all GitHub responses are parsed as data
(JSON and anchored patterns with bounded digits) and never reach a shell. Everyone who
works on this repository, people and agents alike, shares one GitHub account, so a
comment or review proves nothing about who wrote it; that is why no comment can arm or
authorize a merge.
