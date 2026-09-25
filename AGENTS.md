# Working on parchmatte.com (for people and coding agents)

Two static pages for the Parchmatte Mac app: the home page and the privacy
policy at `/privacy/`, which the app's menu and its App Store listing link
to. Plain HTML and CSS, no build step, no JavaScript, served by GitHub Pages
from `main` at `parchmatte.com` (see `CNAME`). `CLAUDE.md` imports this file.

## Rules

1. **No JavaScript and no third-party requests.** No analytics, fonts,
   embeds or CDNs. "Collects nothing" is the product's pitch and the site
   keeps the same promise. If that ever changes it is an owner decision, not
   a PR.
2. **Accuracy over copy.** Every claim about the app must be true of the
   current release: hotkeys, texture and lamp names, the macOS floor,
   permissions, what the privacy policy says it reads. The source of truth
   is the app repo (`Galactic-Luddite/parchmatte`): `README.md`,
   `Sources/Parchmatte/AppController.swift` for hotkeys, `Surfaces.swift`
   for names, `docs/PRIVACY.md` for the policy.
3. **`privacy/index.html` mirrors `docs/PRIVACY.md` in the app repo**
   sentence for sentence. Change both in the same day and bump "Last
   updated" on both. Apple links to this page from the store listing.
4. **Nothing here may contradict the App Store listing**, but this site is
   where the "free if you build it, $2.99 on the store" message lives; the
   store metadata must not carry it.
5. **Keep it light.** Images get `width`, `height`, `srcset` (800 and 1600
   px JPEG, or WebP when added), `loading="lazy"` below the fold, and real
   alt text. Target under 700 KB on first paint.
6. **Author commits with a GitHub no-reply address.** This repo is public.

## Layout

| Path | What |
|---|---|
| `index.html` | Home: hero, build-or-buy choice, features, gallery, hotkeys, privacy summary, build steps |
| `privacy/index.html` | The policy |
| `style.css` | Tokens in `:root` with a dark-mode override; system serif stack |
| `grain.png` | 512 px paper tile used as the fixed page background at 256 px |
| `images/og.jpg` | Social card |
| `images/shots/NN-name-{800,1600}.jpg` | Gallery frames, exported from the App Store screenshot set |
| `favicon.png`, `icon.png` | 64 and 256 px icon |
| `CNAME` | Custom domain for Pages; don't delete it |

## Checks before pushing

Run from the repo root; none need a Mac.

```sh
python3 - <<'PY'
from html.parser import HTMLParser; import os, re
for f in ("index.html", "privacy/index.html"):
    s = open(f).read()
    for m in re.findall(r'(?:src|href|srcset)="([^"]+)"', s):
        for part in m.split(","):
            u = part.strip().split(" ")[0]
            if u.startswith("/") and not (os.path.exists("." + u.rstrip("/")) or os.path.exists("." + u.rstrip("/") + "/index.html")):
                print("BROKEN", f, u)
print("link check done")
PY
```

Then open both pages in a browser at phone width and in dark mode, and
compare the hotkey table against the app README. If you have `tidy` or
`html5validator` installed, run it; otherwise the parser above is the floor.

## Deploy

Push to `main`. GitHub Pages publishes within a minute or two. Keep "Enforce
HTTPS" on in the repository's Pages settings. There is no staging: use a
branch and a pull request for anything more than a typo, and preview the
HTML locally by opening the file.

## Pending from the 2026-09-25 audit

See `docs/audit/release-audit-2026-09-25.md` in the app repo, items W1–W3
and R1–R2: replace the "coming soon" button with the store link once it
exists, add the missing privacy field, add canonical/OG/JSON-LD/robots/
sitemap, and convert the heavy assets to WebP.
