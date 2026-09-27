# parchmatte.com

The static website for [Parchmatte](https://github.com/Galactic-Luddite/parchmatte):
the home page and the privacy policy at `/privacy/`, which the app's menu and
its App Store listing link to.

Plain HTML and CSS, with no site build step. Served by GitHub Pages from `main`.

## Release screenshots

The 12 gallery images and `images/og.jpg` are rendered from six unmodified
screen captures of the exact TestFlight build selected for review. The
captioned 2880×1800 PNGs are uploaded to App Store Connect. The larger menu
panels are crops of the same capture, never recreated interface elements.

Keep the raw captures and store PNGs locally through review. To regenerate,
install Pillow and run:

```sh
python3 scripts/render_release_shots.py RAW_DIR STORE_DIR images/shots
swift scripts/check_release_shots.swift STORE_DIR images/shots
```

The OCR check requires the approved build 6 labels in the final store and
website images and rejects retired labels. Inspect each image visually too;
the check only covers text it can recognize.

## Going live

1. Make this repository public, then Settings → Pages → Deploy from `main`
   (root). Set the custom domain to `parchmatte.com` and tick Enforce HTTPS.
2. In Squarespace → Domains → parchmatte.com → DNS, add:

   | Type | Host | Value |
   |---|---|---|
   | A | @ | 185.199.108.153 |
   | A | @ | 185.199.109.153 |
   | A | @ | 185.199.110.153 |
   | A | @ | 185.199.111.153 |
   | CNAME | www | galactic-luddite.github.io |

3. In Squarespace → Domains → parchmatte.app, forward to
   `https://parchmatte.com`.

When the app is live, replace the "coming soon" button in `index.html` with
the App Store link.
