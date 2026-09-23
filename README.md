# parchmatte.com

The static website for [Parchmatte](https://github.com/Galactic-Luddite/parchmatte):
the home page and the privacy policy at `/privacy/`, which the app's menu and
its App Store listing link to.

Plain HTML and CSS, with no build step. Served by GitHub Pages from `main`.

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
