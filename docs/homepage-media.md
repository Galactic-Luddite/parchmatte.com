# Homepage media

The homepage shows the six Parchmatte 1.2.2 Mac App Store screenshots, in
listing order, all at the same size (1840x1150). Each one is the exact file
uploaded to App Store Connect for 1.2.2, resized from 2880x1800 with macOS
`sips` and stripped of ancillary PNG metadata with
`scripts/strip_png_metadata.py`. Nothing is cropped, retouched or retyped.
Hashes, sizes and source file hashes are in
[homepage-media.json](homepage-media.json).

| Public file | App Store card |
| --- | --- |
| `card-01-softer-look.png` | 1 · A softer, matte look: before and with Velvet |
| `card-02-your-windows.png` | 2 · Your windows. Your look.: two Preview windows, Woven and Velvet |
| `card-03-textures.png` | 3 · Find your texture.: Velvet, Woven and Denim close-ups |
| `card-04-light.png` | 4 · Shape your light.: Candlelight, Warm; Tall; Bottom Right |
| `card-05-menu-bar.png` | 5 · Right in your menu bar.: native Texture menu beside Velvet |
| `card-06-workspace.png` | 6 · Fit your workspace.: paper on, and paused with Preview excluded |

Each card carries its own headline, so the page gives each section a matching
heading for screen readers and search engines (`.sr-only`) instead of a
visible one. When the App Store screenshots change, replace these six files
from the uploaded set, keep them the same size and update the receipt.

The previous homepage images (`01-overview.png`, `02-menu.png`,
`07-woven-terminal.png`, `08-denim-terminal.png`, `09-velvet-writing.png`,
`10-light-shape-controls.png`) remain in `images/shots/` but are no longer on
the homepage; their receipts are in git history.
