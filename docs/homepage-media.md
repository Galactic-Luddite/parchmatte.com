# Homepage media

This held 1.2.1 candidate uses actual pre-submission Parchmatte 1.2.1 (28)
captures alongside retained 1.2.0 (27) and 1.1.0 (26) examples. This update
remains held until 1.2.1 is available on the Mac App Store. Each image has its own provenance in
[`homepage-media.json`](homepage-media.json); the top-level build is the release
target, not a claim that every retained image came from that build.

| Public file | Size | Build | What it shows |
| --- | --- | --- | --- |
| `images/shots/01-overview.png` | 1920x970 | 1.2.1 (28) | Two windows in the same synthetic app: Woven/Gallery on the left and Soft Leaf/Candlelight on the right |
| `images/shots/10-light-shape-controls.png` | 635x804 | 1.2.1 (28) | Actual native Shape submenu: Oval, Round, Wide, Tall; Oval selected; nine position controls |
| `images/shots/09-velvet-writing.png` | 1440x900 | 1.2.0 (27) | Velvet in Wine across the sample writing workspace |
| `images/shots/02-menu.png` | 1920x1048 | 1.2.0 (27) | Nine-texture menu with Velvet selected, Strength 15%, Softness 35%, Candlelight on |
| `images/shots/07-woven-terminal.png` | 1400x1300 | 1.1.0 (26) | Woven on a dark synthetic terminal demo |
| `images/shots/08-denim-terminal.png` | 1400x1300 | 1.1.0 (26) | Denim on the same dark synthetic terminal demo |

The two 1.2.1 images were captured on 2026-10-29 from source
`00b92ddcbec5dc45253c4b46e98ffccb0488cb09`, executable SHA-256
`af212885f62f2ec46315996dd016e10c04f99a44d1d8f7de2a6e46a348cd9fb7`.
The hero is a physical compositor capture using `screencapture -x
-R0,80,1920,970` of two owned synthetic document windows with actual overlays.
Each window has Strength 28% and Light Strength 75%; the left uses Woven and
Gallery, the right Soft Leaf and Candlelight. Whole-screen paper is off.
The light image is an actual native menu-window layer captured with
`screencapture -x -o -l<windowID>` after AX opened Page Light > Shape. Its
visible state is Oval, Center, Gallery and Light Strength 50%. It documents
controls, not a new shape-selection test pass. Only ancillary PNG metadata
was removed using the committed script; IHDR and IDAT remain byte-for-byte
identical. No crop, resampling, enhancement or fabricated UI was applied.
The receipt retains the actual capture commit and executable identity.

The retained 1.2 Velvet workspace and texture-menu frames were captured on
2026-10-19 from source `007fcaff1090b2bb1a6ca9a5898e6a679ede294e`,
Store-project ad-hoc Release, macOS 26.7.1 (25G241), 1920x1080 display, scale 1.
The Velvet workspace is a physical compositor capture at `80,90,1440,900`,
whole-screen Velvet in Wine at Strength 15%, Softness 35%, Page Light off,
normal orientation and Hide from Screenshots disabled. The menu capture uses
`0,32,1920,1048`, whole-screen Velvet, Candlelight on, Light Strength 60% and
Glow Medium; Strength and Softness remain 15% and 35%. Only ancillary PNG
metadata was removed. These images retain their original build provenance.

The retained 1.1 terminal images were captured on 2026-10-10 at Strength 15%,
Softness 35%, Page Light off, with the actual app overlay on a browser-rendered
synthetic terminal demo. They are lossless 1400x1300 crops from 2880x1800 direct
captures, with metadata removed. The crop re-encoded pixels but did not resample
or edit the texture. Their original file and pixel hashes remain in the receipt.
The demo source is `scripts/fixtures/terminal-demo.html`.

Use `python3 scripts/strip_png_metadata.py INPUT.png OUTPUT.png` to remove
ancillary capture metadata. These images are separate from historical Build 6
App Store media in `release-media-build6.json`. The candidate remains held until
1.2.1 is live and owner review is complete; no publication is authorized here.
