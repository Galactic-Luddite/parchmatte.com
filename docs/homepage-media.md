# Homepage media

The homepage shows nine genuine Parchmatte 1.2.2 captures. Page headings,
captions and labels are real HTML; the images hold only the product.

Rules:

- Every image is a 3:2 crop in the same CSS frame. Each ships at its original crop
  size (never enlarged) plus a smaller copy for phones (600x400, or 480x320 for the
  texture close-ups) via `srcset`, all listed in [homepage-media.json](homepage-media.json).
- Sources are crops of the uploaded 2880x1800 App Store screenshots (panels only,
  without their headlines, labels or leaf art) and one native menu capture from the
  installed 1.2.2 build. Crop boxes are in each receipt entry's `transformation`.
- Cropped and, for the phone copies, resized with macOS `sips`, then encoded as WebP
  quality 90 with `cwebp -q 90 -metadata none`. In a side-by-side at 1:1 the grain
  matches the exact PNG. Nothing is retouched, redrawn or retyped. Captions must match
  the settings shown.
- The hero slider is plain HTML/CSS with a short inline script: a hidden range input
  keeps it keyboard accessible, and mouse or a sideways finger drag moves the divider.

| Files | Shows |
| --- | --- |
| `home-plain`, `home-velvet` | the same document without paper and with Velvet (hero slider) |
| `window-woven`, `window-velvet` | two Preview windows with their own textures |
| `texture-velvet`, `texture-woven`, `texture-denim` | matching close-ups |
| `light-candlelight` | warm Candlelight Page Light, bottom right |
| `menu-textures` | the native Texture menu with Velvet selected |

The older images (`01-overview.png` and the other numbered files) remain in
`images/shots/` unused; their receipts are in git history.
