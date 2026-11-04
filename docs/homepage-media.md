# Homepage media

The homepage shows nine genuine Parchmatte 1.2.2 captures. Page headings,
captions and labels are real HTML; the images hold only the product.

Rules:

- Every image is a 3:2 crop in the same CSS frame, shipped as 960x640 and 480x320
  PNG (`srcset`), both listed in [homepage-media.json](homepage-media.json).
- Sources are crops of the uploaded 2880x1800 App Store screenshots (panels only,
  without their headlines, labels or leaf art) and one native menu capture from the
  installed 1.2.2 build. Crop boxes are in each receipt entry's `transformation`.
- Resized with macOS `sips`, then stripped with `scripts/strip_png_metadata.py`.
  Nothing is retouched, redrawn or retyped. Captions must match the settings shown.

| Files | Shows |
| --- | --- |
| `home-plain`, `home-velvet` | the same document without paper and with Velvet (hero slider) |
| `window-woven`, `window-velvet` | two Preview windows with their own textures |
| `texture-velvet`, `texture-woven`, `texture-denim` | matching close-ups |
| `light-candlelight` | warm Candlelight Page Light, bottom right |
| `menu-textures` | the native Texture menu with Velvet selected |

The older images (`01-overview.png` and the other numbered files) remain in
`images/shots/` unused; their receipts are in git history.
