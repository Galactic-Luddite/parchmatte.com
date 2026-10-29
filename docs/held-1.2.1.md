# Held Parchmatte 1.2.1 website candidate

Hold: do not merge until Parchmatte 1.2.1 is live on the Mac App Store.

This local candidate implements the approved messaging direction. Expanded copy
and final images still require owner/Lindsay review. The live Store version
was verified through App Store Connect GET as 1.2 READY_FOR_SALE on October 29.
This candidate describes 1.2.1 and must remain unpublished until both Connect
and the public listing show that release.

The hero now uses the actual build 28 same-app independent-style capture.
The Page Light section now shows actual build 28 native shape and position
controls. Both images preserve source pixels with ancillary PNG metadata removed;
`docs/homepage-media.json` records source/image hashes, dimensions and methods.
The retained material and texture-menu examples keep their original 1.2/1.1
provenance. The release-target receipt declares 1.2.1 (28). Final image approval
remains pending. Keep pricing, support/legal destinations, icon/favicon and
shortcut assignments unchanged.

The private app issue #67 owns progress; #65 owns wording and #66 captures.
The public repository receives only the reviewed website publication batch.
No publisher arming, remote branch push or live-site change has occurred.

Local checks: all 66 existing site tests pass; `scripts/verify_site.py` passes
local asset references and retained image hashes. The existing positioning test
now expects the proposed title/lead and section order. Headless desktop (1440px)
and emulated mobile (390px) upper-page renders were visually inspected. Mobile
document width equals viewport width (390px); no horizontal overflow observed.
The refreshed media received full-page desktop and correctly emulated 390px mobile inspection; final owner image approval remains required before publication.
