# Icon candidate for the combined 1.3 release

The website icon candidate uses the approved Parchmatte 1.3 artwork. It is held for the combined 1.3 release. Preparing these assets does not establish that other 1.3 features or release materials are ready. Page content and screenshot declarations continue to describe 1.2.2.

The approved native PNG has SHA-256 `34a9b62dc6c85b5c441cd7fa12ceebe160ac566d7bcd304400ed18625c68216c`; the native master has SHA-256 `6b2389d6603ae0f7cca390e97e6f84a299e35fa8b389826d2cd96c8350c643c2`. The native icon source is pinned to commit `5999159c9777f109555627aeba6606224bd86ab2`, including the approved 981-pixel native crop and Icon Composer's uniform 1024/981 fit. The export receipt in `site-icons.json` records the system-resolved output and the metadata stripping applied to each website asset.

The six outputs are `icon.png` (1024), `favicon.png` (32), `favicon-48.png` (48), `favicon-96.png` (96), `favicon-192.png` (192), and `apple-touch-icon.png` (180), with square dimensions in pixels. Existing navigation and favicon references automatically use the replacement icon at the same URLs. The dedicated touch icon and additional favicon sizes are refreshed even though the HTML currently does not advertise them. The existing touch declaration continues to reference `icon.png`.

The Open Graph card contains no icon and does not need an artwork replacement. Existing screenshots retain their recorded provenance. A future 1.3 screenshot refresh depends on the final 1.3 interface and must receive its own media verification.

Before release, run `python3 -m unittest discover -s scripts/tests` and `python3 scripts/verify_site.py`. The icon tests check all six assets against receipt hashes, expected dimensions, metadata-free PNG chunks and valid chunk checksums, crawler access, and the icon declarations on all five page types, including the guide. A controlled-corruption test confirms rejection of incorrect hashes, dimensions, ancillary metadata, truncated files and trailing bytes.

Release publication remains a separate action after the combined 1.3 release is ready and authorized. This preparation does not authorize a push, merge, deployment, publisher arming, or version bump.
