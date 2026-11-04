# Homepage media

This local website candidate retains the four botanical compositions and two
historical terminal examples. Botanical scenes retain their 1.2.1 (28)
provenance. Native controls in 02-menu.png and 10-light-shape-controls.png were
recaptured from installed TestFlight 1.2.2 (29). Per-image component provenance,
hashes, sizes and visible settings are in [homepage-media.json](homepage-media.json).

| Public file | What it shows |
| --- | --- |
| `01-overview.png` | Two Preview windows, Woven and Velvet; Strength 28%, Softness 50%, Page Light off |
| `09-velvet-writing.png` | Botanical document with Velvet; Strength 28%, Softness 50%, Page Light off |
| `02-menu.png` | Separate native menu details and retained document; Velvet selected among nine textures; document Strength 28%, Softness 50%, Page Light off |
| `10-light-shape-controls.png` | Separate native menu details; Tall, Bottom Right, Light Strength 75%, Candlelight, Warm |
| `07-woven-terminal.png` | Retained Woven terminal example |
| `08-denim-terminal.png` | Retained Denim terminal example |

The botanical exports use lossless RGB8 PNG. Ancillary metadata is removed
without changing IHDR or compressed IDAT chunks. Separate native menu panels
show actual captured controls, with editable alpha silhouettes excluding only
pixels outside native windows and their outside shadows. Retina control crops
are fitted at native pixel size or smaller; 1:1 placements use integer pixels.
PhotoCraft converts the source display ICC profile to the destination
workingRGB profile during composition. No UI text is retyped or darkened, and
no texture or effect is enhanced. These are mixed-provenance compositions,
not wholly recaptured build 29 scenes. All screenshots link to full-size
images; fine labels in wide menu details require that view on narrow screens.

The terminal examples are lossless crops of a synthetic terminal with the
actual 1.1.0 (26) application overlay, at Strength 15%, Softness 35%, Page Light
off. Their original hashes and settings are retained in the JSON receipt.

This candidate remains local. Public website PR33 is unchanged and held;
public update and release-parity approval gates still apply.
