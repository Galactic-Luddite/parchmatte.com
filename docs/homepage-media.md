# Homepage media

This held 1.2 candidate uses actual Parchmatte 1.2.0 (27) captures alongside
retained 1.1.0 (26) texture examples. Each image has its own provenance in
[`homepage-media.json`](homepage-media.json); the top-level build is the release
target, not a claim that every retained image came from that build.

| Public file | Size | Build | What it shows |
| --- | --- | --- | --- |
| `images/shots/01-overview.png` | 1440x900 | 1.2.0 (27) | Velvet in Wine confined to one sample writing window; the reference area outside stays plain |
| `images/shots/09-velvet-writing.png` | 1440x900 | 1.2.0 (27) | Velvet in Wine across the sample writing workspace |
| `images/shots/02-menu.png` | 1920x1048 | 1.2.0 (27) | Nine-texture menu with Velvet selected, Strength 15%, Softness 35%, Candlelight on |
| `images/shots/07-woven-terminal.png` | 1400x1300 | 1.1.0 (26) | Woven on a dark synthetic terminal demo |
| `images/shots/08-denim-terminal.png` | 1400x1300 | 1.1.0 (26) | Denim on the same dark synthetic terminal demo |

The three 1.2 frames were captured on 2026-10-19 from source commit
`007fcaff1090b2bb1a6ca9a5898e6a679ede294e`, Store-project ad-hoc Release,
on macOS 26.7.1 (25G241), with a 1920x1080 display at scale 1.
`/usr/sbin/screencapture` captured the physical desktop compositor at rectangle
`80,90,1440,900`. The overview and Velvet scene use Strength 15%, Softness 35%, Page Light off, normal
orientation and Hide from Screenshots disabled. The overview uses single-window
paper; the Velvet scene uses whole-screen paper. The menu capture uses rectangle
`0,32,1920,1048`, whole-screen Velvet, Candlelight on, Light Strength 60% and
Glow Medium; Strength and Softness remain 15% and 35%. The writing and reference
content are neutral sample material. Only ancillary PNG metadata was removed;
IHDR and IDAT are preserved byte for byte, with no crop or resampling.

The retained 1.1 terminal images were captured on 2026-10-10 at Strength 15%,
Softness 35%, Page Light off, with the actual app overlay on a browser-rendered
synthetic terminal demo. They are lossless 1400x1300 crops from 2880x1800 direct
captures, with metadata removed. The crop re-encoded pixels but did not resample
or edit the texture. Their original file and pixel hashes remain in the receipt.
The demo source is `scripts/fixtures/terminal-demo.html`.

Use `python3 scripts/strip_png_metadata.py INPUT.png OUTPUT.png` to remove
ancillary capture metadata. These images are separate from historical Build 6
App Store media in `release-media-build6.json`. The candidate remains held until
1.2 is live and owner review is complete; no publication is authorized here.
