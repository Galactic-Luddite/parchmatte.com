# Research: Compare-page design survey for parchmatte.com/compare

**Date:** 2026-09-29
**Issue:** none (feeds the `compare/index.html` + `style.css` build)
**Question:** How do well-designed indie/small-team Mac apps structure their "vs" / "alternatives" pages, and what should a paper-aesthetic single-page "Parchmatte vs Night Shift / f.lux / Paperman" page copy, avoid, and title?

Screenshots live in `docs/design/compare-survey/` (full-page PNG at 1280px unless noted). All page metadata was captured with `curl` and Playwright on 2026-09-29.

---

## Sources Consulted

| # | Source | Type | URL |
|---|--------|------|-----|
| 1 | Raycast vs Alfred | First-party compare page | https://www.raycast.com/raycast-vs-alfred |
| 2 | Craft vs Notion | First-party compare page | https://www.craft.do/compare/notion |
| 3 | Capacities vs Apple Notes | First-party compare page | https://capacities.io/compare/apple-notes |
| 4 | Todoist vs Notion | First-party compare article | https://www.todoist.com/inspiration/todoist-vs-notion |
| 5 | Vivaldi browser comparison | First-party compare page | https://vivaldi.com/compare/ |
| 6 | Bear FAQ | Indie FAQ (tone/structure reference) | https://bear.app/faq/ |
| 7 | f.lux F.A.Q. | Competitor FAQ (tone reference) | https://justgetflux.com/faq.html |
| 8 | Paperman landing | Direct competitor | https://paperman.cc/ |
| 9 | Night Shift Keeper blog | Ranking for "f.lux vs Night Shift mac" | https://www.nightshiftkeeper.com/blog/flux-vs-night-shift-vs-other-blue-light-apps-mac/ |
| 10 | CircadianShield compare | Ranking for "best blue light filter mac" | https://circadianshield.com/compare/best-blue-light-filter-mac-2026 |
| 11 | AlternativeTo f.lux (Mac) | Ranking for "f.lux alternative" | https://alternativeto.net/software/f-lux/?platform=mac |
| 12 | parchmatte.com `index.html` / `style.css` | Current site tokens and FAQ markup | repo |

### Substitutions (requested pages that do not exist)

Probed 2026-09-29, all HTTP 404 (curl, `-L`): `cleanshot.com/compare`, `cleanshot.com/alternatives`, `raycast.com/compare`, `arc.net/compare`, `sigmaos.com/compare`, `ulysses.app/compare`, `ia.net/writer/compare`, `bear.app/vs-apple-notes`, `bear.app/alternatives`, `culturedcode.com/things/vs-todoist`, `todoist.com/compare/things`. Web search for Ulysses/iA Writer/Things/Bear/CleanShot first-party "vs" pages returned only third-party articles (Reedsy, Setapp, Upbase, etc.), so those vendors appear not to publish compare pages. Substituted Craft, Capacities, Todoist (its `/compare` hub links to `/inspiration/todoist-vs-*`), Vivaldi, and Bear's FAQ. Raycast's page is at `/raycast-vs-alfred`, not `/alfred` (that URL is a user profile).

---

## Findings

### Q1: Surveyed pages

| Page / screenshot | Purpose | Layout | Feature table | Tone to competitor | FAQ | CTA placement | `<title>` / meta description | H1 / H2 pattern | Steal | Avoid |
|---|---|---|---|---|---|---|---|---|---|---|
| **Raycast vs Alfred** `raycast-vs-alfred.png`, `raycast-vs-alfred-mobile-table.png` | Convert Alfred users | Hero (H1 + sub-question) -> 10 feature-story H2 sections with screenshots -> "Feature comparison" table near the bottom -> closing CTA band. 10.6k px tall, dark bg, Inter | One `<table>`: `Built-in Features \| Raycast \| Alfred`; every cell is an SVG check/cross, no text; header not sticky; at 390px the table fits at 342px wide with no horizontal scroll (first col 173px) | Confident, slightly needling ("Why is it that few Alfred users go back") but factual; concedes Alfred's Powerpack is one-time | None | Nav "Download", per-section none, final band "Download for Mac / Install via Homebrew" | `Raycast vs Alfred - Why are people choosing Raycast over Alfred?` / "Why is it that few Alfred users go back after trying Raycast? Millions use Raycast..." | H1 = "X vs Y" + question sub-line; H2s are benefit nouns ("Calculate anything", "Manage Windows"), then "Feature comparison" | Two-line H1 (name pair + human question); table kept narrow so it survives phones | Icon-only cells: a check tells you nothing about *how* (Paperman "has a warm tint" is not the same as Page Light); 10k px of marketing before the table |
| **Craft vs Notion** `craft-vs-notion.png` | Rank for "Notion alternative" | Hero -> "Which one is right for you?" two cards (Craft / Notion) -> "Move from Notion in three steps" -> "Feature-by-Feature Comparison" grid -> testimonials -> "Compare the cost" -> "Common Questions". Warm off-white bg rgb(252,249,247) | Div grid, 4 cols: `Feature \| Craft \| Notion \| Winner`; cells are short text ("100% functionality offline" vs "Limited (requires internet)"); Winner column names Notion twice (databases, integrations) | Respectful; explicitly awards rows to the competitor, which reads as honest | 19 H3 questions under H2 "Common Questions"; FAQPage JSON-LD; plain H3 + p, no `<details>` | "Try Craft Free" repeated after hero, table and cost; "Import from Notion" as secondary | `Best Notion Alternative in 2026: Why Users Switch to Craft` / "Looking for the best Notion alternative? Craft is the fast, native, offline-first alternative..." | H1 = "Craft vs Notion"; title carries the search phrase ("Notion Alternative"), H1 carries the brand pair | Text cells + a Winner column that sometimes says the other guy; title-vs-H1 split (search phrase in title, "X vs Y" in H1) | 19 FAQ items is padding; FAQ without `<details>` is a wall of text |
| **Capacities vs Apple Notes** `capacities-vs-apple-notes.png` | Rank for "Capacities vs Apple Notes", honest positioning | "VS" eyebrow -> H1 -> one-paragraph framing -> "At a Glance" 6-row table -> "Feature Comparison" grouped by H3 category -> Pricing -> Strengths (both) -> Known Limitations (both) -> "Who Is It For?" -> "The Verdict: Choose X if… / Choose Y if…" -> FAQ. 12.3k px, white bg, system font | Div grids: `FEATURE \| CAPACITIES \| APPLE NOTES` with descriptive text in every cell; category H3s break the grid into 6 small tables; sticky top nav only | The word "Honest" is in the `<title>`; "Known Limitations" section lists its own weaknesses | H2 "Frequently Asked Questions"; FAQPage + BreadcrumbList + WebPage JSON-LD | "Get Started" in nav, "Switching guide / Import guide" under hero, "Get Started Free" at bottom | `Capacities vs Apple Notes — Honest Comparison (2026)` / "An in-depth, honest comparison of Capacities and Apple Notes. Compare features, pricing, strengths, and pain points..." | H1 "X vs Y"; H2s are nouns ("At a Glance", "Pricing", "Strengths", "The Verdict") | "At a Glance" mini-table before the long grid; "Choose X if… / Choose Y if…" verdict; "Known Limitations" for the home team | 12k px, six sub-tables for two products; too much for a one-page paper site |
| **Todoist vs Notion** `todoist-vs-notion.png` | Convert Notion teams, rank for "Todoist vs Notion" | Blog-style article: H1 + deck -> sticky "Jump to section" sidebar -> prose -> one `CATEGORY \| TODOIST \| NOTION` table -> "Where Notion Might Be the Right Fit" -> criticisms -> FAQ | One `<table>`, prose cells ("Opinionated simplicity that scales" vs "A blank canvas that can become anything – if someone has the time"); not sticky | Editorial, a bit loaded ("blank page", "sprawling") but includes a whole H2 conceding when Notion fits | H2 "Frequently Asked Questions", H3s prefixed "Q:"; Article JSON-LD (no FAQPage) | "Start for free" in nav, mid-article "Try Todoist for yourself" card, bottom | `Todoist vs Notion: Built for Doing, Not Just Documenting` / "Comparing Todoist and Notion for team task management? Discover how..." | H1 = "X vs Y: <slogan>"; H2s are full sentences ("Why Teams Switch from Notion to Todoist") | A whole section conceding when the competitor is the right pick | "Q:" prefixes, emoji H3s, article chrome (related posts) that dilutes the page |
| **Vivaldi compare** `vivaldi-compare.png` | Rank for "best browser" | H1 -> intro -> three question H2s, each with an icon table (Vivaldi + 5 rivals) and a "Verdict: Vivaldi is the best…" H3 -> Conclusion -> "Get away from Big Tech" CTA | Three `<table>`s, 7 columns, icon-only cells, `overflow-x: visible`; no sticky header | Self-declared verdicts on every table ("Verdict: Vivaldi is the best browser for privacy"), which reads as an ad | None | "Download" in nav and after conclusion | `The top 6 browsers for 2023 in direct comparison \| Vivaldi` / "In this 2023 best browser guide..." | H1 declarative; H2s are questions ("Which browser is best for privacy?") | Question-form H2s match how people search | Year baked into the title and never updated (still "2023" in 2026); 7-column icon tables; verdict under every table |
| **Bear FAQ** `bear-faq.png` | Help centre index | H1 "Lost in space? Bear is here to help." -> grid of topic cards (Get Started, Edit and format, Search, Note safety, Import your notes) | none | n/a (does not name competitors) | Topic cards link to articles; no on-page Q/A, no schema | none beyond nav | `Lost in space? Bear is here to help.` / "A comprehensive guide to all Bear features" | Playful H1 with a real subject; H3 topic nouns | Human H1 voice; card grid with one-line hooks | Nothing indexable on the page itself; title has no keyword |
| **f.lux F.A.Q.** `flux-faq.png` | Support FAQ | Salmon bg rgb(255,238,227), system font, one column: H2 groups ("Life and the universe", "f.lux on macOS", "f.lux at work", "General questions", "Troubleshooting") each a list of bold question + 1–3 sentence answer | none | Never mentions Night Shift at all | Plain bold Q / paragraph A; no `<details>`, no schema; a search box at top | none (support page) | `f.lux: F.A.Q.` / "Is your computer keeping you up late? f.lux is a free download that warms up your computer display at night, to match your indoor lighting." | H2 group names are dry-witty ("Life and the universe"); questions are first-person user voice ("I installed this but it looks too pink/orange.") | First-person question phrasing; short, unhedged answers ("This is a video driver bug and not something we can fix directly.") | Dated OS-version cruft; no headings on questions so nothing is linkable |
| **Paperman landing** `paperman-landing.png` | Sell the app; pre-empts the f.lux/Night Shift question | Hero (H1 "Make your screen feel like paper.™", live "Try the Paperman effect" toggle, store-rank badges) -> reviews carousel -> H2 **"Not a blue light filter."** with a two-card contrast (BLUE LIGHT FILTERS: "Change colors to warmer tones" / PAPERMAN: "Changes texture to soften contrast", captioned "Night Shift / f.lux ORANGE TINT" vs "Paperman MATTE SURFACE") -> How it works (01/02/03) -> "Better by design" science -> textures -> Desk Lamp -> details -> "Frequently asked." -> pricing. Dark green-black bg rgb(12,21,10), Inter, ~11.9k px, fixed sale pill + floating paper toggle | No table; the comparison is a two-card diptych | Firm differentiation, not disparagement: "Every other eye protection tool changes your colors. Paperman changes your screen's texture. It works alongside color filters" | H2 "Frequently asked." 7 Qs, first is "How is this different from f.lux or Night Shift?", also "Why pay when Night Light is free?"; FAQPage + SoftwareApplication JSON-LD; JS accordions, no `<details>` | "Get Paperman™" in nav and hero, download buttons per OS, pricing at bottom ($9.95 lifetime, Setapp trial) | `Paperman™ \| Digital Matte Surface for Visual Ergonomics` / "Paperman™ is a screen texture engine that applies a subtle digital matte surface to enhance visual ergonomics..." | H1 is a promise; H2s are short declaratives ending in periods ("Not a blue light filter.", "Nine textures.") | The two-card "colour vs texture" diptych is the clearest single explanation of the category; FAQ that names competitors by name in the question | Trademark symbols everywhere, countdown sale pill, "visual ergonomics" jargon; the page cannot say "warm tint" because Paperman positions against tint, which is exactly the gap Parchmatte's optional Page Light fills |

### Q2: Pages ranking for the target phrases

| Page | `<title>` | Meta description | H2s (abridged) | Notes |
|---|---|---|---|---|
| Night Shift Keeper | `f.lux vs Night Shift vs Other Blue Light Apps on Mac (2026 Comparison) \| Night Shift Keeper` | "Comparing f.lux, Night Shift, Iris, and other blue light filter apps on Mac. Find out which is best for battery life, performance, and eye strain in 2026." | "f.lux: The Veteran", "macOS Night Shift: The Native Option", "Iris: The Feature-Rich Alternative", "Dimmer & Similar Minimal Apps", "The Verdict"; H3 "Why Night Shift + Night Shift Keeper Wins" | FAQPage schema, one table. Epithet-per-app H2 pattern. No mention of Paperman or Parchmatte. |
| CircadianShield | `Best Blue Light Filter for Mac 2026: 8 Apps Compared and Ranked` | "Blue light filter apps for Mac ranked: CircadianShield, f.lux, Night Shift, Iris, Lunar and LookAway compared across 11 features, plus anti blue light MacBook film." | "Quick answer: the best blue light filter for Mac", "Full reviews of all 8…", "Which Mac blue light filter fits your situation", "…external displays", "Which Macs each … runs on", "What the research says…", "…frequently asked questions", "Final verdict…" | FAQPage schema; FAQ H3s are literal search queries ("Is Night Shift on Mac good for your eyes?", "Does Mac have a built-in blue light filter?"). Keyword repeated in nearly every H2. |
| AlternativeTo (f.lux, Mac) | `f.lux Alternatives for Mac: Top 18 Color Temperature Tools \| AlternativeTo` | "There are many alternatives to f.lux for Mac if you are looking for a replacement. The best Mac alternative is Redshift, which is both free and Open Source…" | H1 "f.lux Alternatives for Mac"; H2 per app: Redshift, Iris mini, Solace, Iris, Vivid, Lumen, NightTone, Desktop Dimmer, Shifty, Nox… | Curl returns 403 (Cloudflare); loads in a browser. Neither Paperman nor Parchmatte is listed. Gap: nobody currently ranks for "Paperman alternative" with a first-party page. |

**Confidence:** Confirmed for every row (captured directly from the live pages).

---

## Synthesis: shared patterns

1. **H1 is "X vs Y"; the search phrase lives in `<title>`.** Craft (`Best Notion Alternative in 2026…` / H1 `Craft vs Notion`), Capacities, Raycast and Todoist all do this. Ranking pages put the year and "Mac" in the title.
2. **Framing before the table.** Every good page has a one-paragraph "which one is right for you" or "at a glance" block before feature rows (Craft cards, Capacities "At a Glance", Todoist deck, Paperman diptych).
3. **Text cells beat icons.** The three most persuasive pages (Craft, Capacities, Todoist) use short descriptive text in cells; the icon-only pages (Raycast, Vivaldi) tell you *that* a thing exists, not *how*. For a category where the whole point is "colour vs texture", checkmarks would flatten the argument.
4. **Nobody uses a sticky table header.** Only site navs are sticky. Tables are kept to 3–4 columns and survive 390px by narrowing (Raycast: 342px wide, no scroll). Parchmatte's existing `th:first-child { white-space: nowrap }` at 560px is the same trick.
5. **Concede something.** Craft's Winner column awards Notion two rows; Todoist has "Where Notion Might Be the Right Fit"; Capacities has "Known Limitations" for itself. Vivaldi's "Verdict: Vivaldi is best" under every table is the anti-pattern.
6. **FAQ is H2 + question H3s, with FAQPage JSON-LD.** Craft, Capacities, Paperman, Night Shift Keeper and CircadianShield all ship FAQPage schema. None of the surveyed pages uses native `<details>/<summary>` (Paperman uses JS accordions), so Parchmatte's existing `.faq details > summary > h3` pattern is already ahead on accessibility and keeps the H3s indexable.
7. **CTA cadence is nav + after-table + bottom.** Never inside the table. Secondary CTA is always "import/switch" (Craft, Capacities) — for Parchmatte that maps to "run it alongside Night Shift".
8. **Tone that works:** firm about the difference, dry about the rival. Paperman's "Every other eye protection tool changes your colors. Paperman changes your screen's texture." and f.lux's "This is a video driver bug and not something we can fix directly." Both avoid superlatives.
9. **Paperman's blind spot.** Its whole page argues *against* tint ("Not a blue light filter", "Why pay when Night Light is free?"). Parchmatte has grain *and* an optional warm Page Light, is free/OSS or $2.99, and papers a single window (`⌃⌥P`). None of the ranking pages mention Paperman, so "Paperman alternative" is an open query.

---

## Recommendations (paper-aesthetic single page: Parchmatte vs Night Shift / f.lux / Paperman)

1. **Structure (top to bottom), ~5 screens, not 10k px:**
   - Hero: H1 "X vs Y" pair + one human sub-line (Raycast's two-line H1; reuse `.hero h1 .h1-sub`), one sentence of framing, primary CTA "Get it on the Mac App Store — $2.99" + text link "or build it free".
   - **"At a glance" diptych** (steal Paperman's two-card contrast, but three cards on `--card` with `--rule` borders): *Colour tint* (Night Shift, f.lux) / *Paper grain* (Paperman) / *Both, your choice* (Parchmatte). One line each. This is the single most important block; it makes the argument before any table.
   - **One 4-column table**: `What you get \| Night Shift \| f.lux \| Paperman \| Parchmatte` is five columns, too many for 390px. Use `Feature \| Colour-shift apps (Night Shift, f.lux) \| Paperman \| Parchmatte` (4 cols) with **short text cells** ("Warm tint only" / "Grain only, no tint" / "Grain + optional Page Light"). Rows: what it changes, warm tint, paper grain, single-window mode, price, source, external monitors, screenshots, runs alongside. Add a "Runs alongside Parchmatte?" row as the concession/complement (pattern 5). Reuse existing `table/th/td` rules; add `.compare td:last-child { background: var(--paper-deep) }` to highlight the home column, and keep `th:first-child` nowrap on mobile. No sticky header.
   - Three short **"vs" H2 sections** (one paragraph + one concrete detail each), each ending with a one-line "Pick <rival> if…" (Capacities "Choose X if…"). Be explicit that Night Shift/f.lux can run underneath Parchmatte.
   - **FAQ** using the existing `.faq details > summary > h3` markup and FAQPage JSON-LD, 5–6 questions max, in first-person user voice (f.lux): "I already use Night Shift. Do I still need this?", "Does it turn my screen orange?", "How is this different from Paperman?", "Can I paper only one window?", "Is it really free?".
   - Closing CTA band, same two buttons as hero.
2. **Cell text, not checkmarks**, except a small ✓/– glyph for the "Runs alongside" row where a boolean is honest.
3. **Concede on the page**: Paperman has more textures and Windows; Night Shift is built in and free; f.lux has schedule/wake automation. Say so in the table and the H2s. Credibility is the differentiator against CircadianShield-style "we ranked ourselves #1" pages.
4. **Tone**: paper, not polemic. No "veteran / native option" epithets (Night Shift Keeper), no verdict badges (Vivaldi), no trademark symbols or countdowns (Paperman). Sentences that end in periods, like Paperman's H2s, suit the existing "What it does / See it / Hotkeys" H2 voice.
5. **SEO plumbing**: canonical `https://parchmatte.com/compare/`, add to `sitemap.xml`, link from the homepage FAQ answer that already says "Night Shift and f.lux only warm your screen's colour", BreadcrumbList (Capacities) is optional, FAQPage required. Keep the year out of the H1 (Vivaldi's stale "2023"); a year in the `<title>` is fine only if the page will be re-dated.
6. **Mobile**: 4-column table at 390px with `font-size: 0.9rem`, `th:first-child` nowrap, cell text ≤ 4 words; test with Playwright at 390px as Raycast's table demonstrates it can be done without scroll.

### Title candidates (≤ 60 chars)

1. `Parchmatte vs Night Shift, f.lux and Paperman for Mac`
2. `Night Shift vs f.lux vs Paperman: a Paper-Texture Alternative`
3. `Paperman Alternative for Mac: Parchmatte vs f.lux & Night Shift`

### Meta description candidates (≤ 155 chars)

1. `Night Shift and f.lux warm your colours. Paperman adds grain. Parchmatte does both, on one window or all of them, free and open source or $2.99 on the Mac App Store.`
2. `Compare Parchmatte with Night Shift, f.lux and Paperman on Mac: warm tint, paper grain, single-window mode, price and what runs alongside what.`
3. `Looking for a Paperman or f.lux alternative for Mac? Parchmatte lays a paper grain and an optional warm Page Light over your screen. Honest side-by-side.`

### H1 candidates (with sub-line, per the Raycast two-line pattern)

1. `Parchmatte vs Night Shift, f.lux and Paperman` / sub: `Tint, grain, or both. Which one your eyes actually want.`
2. `Night Shift, f.lux, Paperman, Parchmatte.` / sub: `Four ways to soften a Mac screen, compared honestly.`
3. `A paper-texture alternative to f.lux, Night Shift and Paperman` / sub: `What each one changes, and what you can run together.`

### "vs" H2 candidates (three sections; pick one per row)

| Section | Option A (search-tuned) | Option B (question, Vivaldi/CircadianShield style) | Option C (declarative, Paperman style) |
|---|---|---|---|
| Night Shift | `Parchmatte vs Night Shift on Mac` | `Is Night Shift enough on a Mac?` | `Night Shift warms. Parchmatte adds the page.` |
| f.lux | `Parchmatte vs f.lux` | `f.lux vs Night Shift: does Parchmatte replace either?` | `f.lux schedules the tint. Parchmatte softens the surface.` |
| Paperman | `Parchmatte vs Paperman: the Paperman alternative with a warm tint` | `Looking for a Paperman alternative?` | `Paperman is grain only. Parchmatte is grain, tint, or one window.` |

Recommendation: Option A for H2 text (matches "f.lux vs Night Shift mac" and "Paperman alternative" literally) with Option C as the first sentence of each section's paragraph.

---

## Gaps

- No first-party compare pages from CleanShot, Arc/Orion/SigmaOS, Ulysses/iA Writer, Bear (vs Apple Notes) or Things exist; substitutes are listed above. Not a research failure, a market fact: most indie Mac vendors do not publish "vs" pages, which is itself a signal that a modest, honest one can rank.
- Search-volume figures for "f.lux vs Night Shift mac" and "Paperman alternative" were not measured (no keyword tool in scope); the phrase tuning above is based on the titles/H2s of the pages that currently rank.
- Mobile behaviour was verified only for Raycast's table (390px); other pages were captured at 1280px.
- AlternativeTo blocks curl (Cloudflare 403); metadata was read through the browser.

## Decision Points

1. 4-column table (colour-shift apps merged) vs 5-column (Night Shift and f.lux separate). Recommendation: 4 columns; split them only in the H2 prose.
2. Whether to put a year in `<title>` (ranking pages do; Vivaldi shows the rot). Recommendation: no year.
3. Which H2 option set (A/B/C) — recommendation above.

## Next Steps

1. Developer builds `compare/index.html` from the structure in Recommendation 1, reusing `style.css` tokens and the existing `.faq` markup; add `.compare` table styles only.
2. Add `/compare/` to `sitemap.xml` and link it from the homepage FAQ.
3. Playwright check at 390px and 1280px before merge.
