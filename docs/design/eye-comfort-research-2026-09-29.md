# Eye-comfort evidence for the Parchmatte research page

- Date: 2026-09-29
- Requested by: team-lead (parchmatte.com)
- Decision this unblocks: what `parchmatte.com/research/index.html` ("Why a softer screen is easier on your eyes") may claim, and which source backs each claim.
- Depth: systematic multi-source (web only; primary sources and major medical/ergonomics bodies preferred). No other file modified. Nothing committed.

## Summary

- **Glare and reflections are a well-documented contributor to digital eye strain.** AAO, AOA and OSHA all name glare from windows/overhead lights reflected on a glossy screen as a cause of discomfort, and all recommend matte/anti-glare filters and matching screen brightness to the room. Confidence: high (three independent authoritative bodies agree).
- **"Paper-like" presentation is more comfortable for long reading, with caveats.** The strongest study (Benedetto 2013, PLOS ONE) found LCD reading produced more visual fatigue and fewer blinks than E-ink or paper, attributed to backlight luminance, not texture. Dyslexia-accessibility guidance (Microsoft, British Dyslexia Association) recommends off-white over pure white backgrounds. But the reading-performance literature (Piepenbrock/Buchner) shows dark-on-light positive polarity with *good* contrast reads best, so the page must not say "less contrast is always better." Confidence: moderate.
- **Blue light does not damage eyes (AAO); evening screen light does shift sleep timing (Chang 2015); Night Shift-style colour shifts alone show little or no measurable sleep benefit (Nagare 2019, Duraccio 2021); blue-blocking glasses probably do nothing for eye strain (Cochrane 2023).** The page may describe warm tint as a comfort preference and, at most, as consistent with generic "dim and warm screens in the evening" advice. It must not claim the tint improves sleep or protects eyes. Confidence: high on the negatives, moderate on the sleep-timing mechanism.
- **20-20-20, brightness matching, blinking, ambient lighting** are endorsed by AAO/AOA/OSHA. Confidence: high.
- **No peer-reviewed or institutional source on texture/grain overlays or "digital matte" software was found.** Only vendor product pages (Paper Overlay on the Microsoft Store, Paperman) make such claims. The page must say Parchmatte's specific effect has not been studied.

Recommended framing: Parchmatte *softens* a glossy display by adding a diffuse texture and optional warmth; the sources support "glare and harsh contrast contribute to discomfort" and "many people find a paper-like, less glaring screen more comfortable," but nothing supports "Parchmatte reduces eye strain by X" or any medical or sleep outcome.

## Source table

| # | Source (URL) | Org / venue | Year | Finding (one line) | Strength |
|---|---|---|---|---|---|
| S1 | https://www.aao.org/eye-health/tips-prevention/computer-usage | American Academy of Ophthalmology, reviewed James M. Huffman MD | 2024-06-27 | "Try using a matte screen filter to cut glare." "Adjust your screen brightness to match the level of light around you." Blink rate falls to ~5-7/min at screens vs ~15 normally. Recommends looking into the distance regularly. Also says "try increasing the contrast on your screen to reduce eye strain." | High: major medical body, physician-reviewed. Verified by direct fetch. |
| S2 | https://www.aao.org/eye-health/tips-prevention/should-you-be-worried-about-blue-light | AAO | 2021-03-10 | "There is no scientific evidence that blue light from digital devices causes damage to your eye." Discomfort is digital eye strain from reduced blinking. Says late-night blue light "can make it harder to get to sleep"; suggests night settings and limiting screens 2-3 h before bed. | High. Verified by direct fetch. |
| S3 | https://www.aao.org/eye-health/tips-prevention/digital-devices-your-eyes | AAO | (undated in snippet) | Glass screens cause glare; consider a matte screen filter; adjust brightness/contrast and dim nearby lighting; blue light from screens does not cause eye strain or disease. | High. Seen via search snippet only; verify wording before quoting. |
| S4 | https://www.aoa.org/healthy-eyes/eye-and-vision-conditions/computer-vision-syndrome | American Optometric Association | current page | "The level of contrast of the letters to the background is reduced, and the presence of glare and reflections on the screen may make viewing difficult." "Position the computer screen to avoid glare." "If there is no way to minimize glare from light sources, consider using a screen glare filter." 20-20-20 rule. "Try to blink frequently." | High. Verified by direct fetch. |
| S5 | https://www.osha.gov/etools/computer-workstations/workstation-environment | US OSHA Computer Workstations eTool | current | Windows/overhead lights reflected on the monitor "make images more difficult to see, resulting in eye strain and fatigue." "Use glare filters that attach directly to the surface of the monitor to reduce glare" but they "should not significantly decrease screen visibility." Office lighting 20-50 foot-candles for screen work. | High: federal ergonomics guidance. Verified by direct fetch. |
| S6 | https://bmjophth.bmj.com/content/3/1/e000146 (DOI 10.1136/bmjophth-2018-000146) | Sheppard & Wolffsohn, BMJ Open Ophthalmology | 2018 | Peer-reviewed review: DES prevalence ~50%+ of computer users; symptoms split into accommodative/binocular and dry-eye types; management = refractive correction, dry-eye care, regular breaks. | High for prevalence/management. Full text not fetchable here (403); glare-specific wording not verified, cite only for prevalence and management. |
| S7 | https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0083676 | Benedetto et al., PLOS ONE 8(12): e83676 | 2013 | Prolonged reading on backlit LCD "triggers higher visual fatigue with respect to both the E-ink and the paper book" and lowers blink rate; E-ink and paper were indistinguishable. Authors attribute this to higher LCD luminance (27.8 vs 11.3 cd/m2 E-ink, 16.4 paper). | Moderate: single small lab study (n=12), peer-reviewed. Verified by direct fetch. |
| S8 | https://www.pnas.org/doi/10.1073/pnas.1418490112 | Chang, Aeschbach, Duffy, Czeisler, PNAS 112(4):1232-1237 | 2015 | Reading a light-emitting tablet for 5 evenings vs print book suppressed melatonin (~55%), delayed circadian phase, lengthened sleep latency, reduced REM and next-morning alertness. | High: controlled lab study in top journal; small n (12), tablet at max brightness. Verified via search summaries and journal listing. |
| S9 | https://www.health.harvard.edu/staying-healthy/blue-light-has-a-dark-side | Harvard Health Publishing | 2024-07-24 | Blue light suppressed melatonin about twice as long as green light in Harvard experiments; advises avoiding bright screens 2-3 h before bed and dim warm/red light at night. | Moderate: consumer-health summary of primary research, not itself primary. Verified by direct fetch. |
| S10 | Nagare, Plitnick, Figueiro, "Does the iPad Night Shift mode reduce melatonin suppression?" Lighting Research & Technology 51(3) (PMC6561503, https://pmc.ncbi.nlm.nih.gov/articles/PMC6561503) | Lighting Research Center, RPI | 2019 | Night Shift settings did not significantly change melatonin suppression; "changing the spectral composition of self-luminous displays without changing their brightness settings may be insufficient." | Moderate: single lab study. PMC fetch blocked by CAPTCHA; quote taken from search summary, verify before use. |
| S11 | Duraccio et al., "Does iPhone night shift mitigate negative effects of smartphone use on sleep outcomes in emerging adults?" Sleep Health 7(4) (https://www.sleephealthjournal.org/article/S2352-7218(21)00060-7/abstract) | BYU, Sleep Health | 2021 | n=167, wrist actigraphy: no sleep differences attributable to Night Shift; among longer sleepers, no-phone beat phone-with-Night-Shift. | Moderate: single field RCT. Journal page 403 here; details corroborated by MacRumors/Deseret coverage. |
| S12 | https://www.cochrane.org/about-us/news/blue-light-filtering-spectacles-probably-make-no-difference-eye-strain-eye-health-or-sleep (review CD013244.pub2) | Cochrane, Singh et al., 17 RCTs | 2023-07-26 | "There may be no short-term advantages" of blue-light filtering lenses for computer visual fatigue; effects on sleep unclear; no evidence of retinal protection. | High: systematic review. Verified by direct fetch. Note it concerns spectacles, not screen tints; use only as analogy for "blue light is not the main driver of eye strain." |
| S13 | https://support.apple.com/en-us/102191 | Apple Support (Night Shift) | current | "Studies have shown that exposure to bright blue light in the evening can affect your circadian rhythms and make it harder to fall asleep." Night Shift shifts colours warmer after dark. | Low-moderate: vendor statement; useful only to show what the OS itself claims. Verified by direct fetch. |
| S14 | Piepenbrock, Mayr, Mertens, Buchner, "Positive display polarity is advantageous for both younger and older adults" (Ergonomics 2013); Buchner & Baumgartner 2007; Piepenbrock 2014 https://pubmed.ncbi.nlm.nih.gov/25135324/ | Ergonomics / Applied Ergonomics, HHU Dusseldorf | 2007-2014 | Dark text on a light background reads better than light-on-dark, for all ages; the higher luminance yields smaller pupils and a sharper retinal image. | High for polarity; this is a *counterweight*: it argues against reducing text contrast. Seen via search summaries; PubMed blocked here. |
| S15 | https://support.microsoft.com/en-us/accessibility/powerpoint/make-your-powerpoint-presentations-accessible-to-people-with-disabilities | Microsoft Support | current | "Off-white backgrounds are better for people with perceptual disabilities, like dyslexia." | Moderate: vendor accessibility guidance, not a study. Search snippet; verify wording. |
| S16 | British Dyslexia Association Dyslexia Style Guide (URL not confirmed; the bdadyslexia.org.uk path tried returned 404; summarised at https://dyslexiascotland.org.uk/contrasting-advice-what-colours-are-best-for-accessibility/) | BDA | 2018/2023 | Recommends dark (not black) text on light (not white) background; avoid pure white which "can cause glare"; cream/off-white/pastel preferred. | Moderate: expert guidance body, evidence base is user preference. Locate current PDF before citing. |
| S17 | https://userfocus.co.uk/resources/iso9241/part7.html (summary of ISO 9241-7, now ISO 9241-303/307) | ISO ergonomics standard for displays with reflections | 1998 / 2008-2011 | Standard exists because "under some conditions, reflections become disturbing to the user and affect both comfort and task performance"; specular reflections reduce contrast and legibility. | High that the standard exists; cite as "international display ergonomics standards regulate screen reflections." Secondary summary; ISO text is paywalled. |
| S18 | https://apps.microsoft.com/detail/9mst0qc4z3d0 (Paper Overlay, Windows) and https://paperman.cc/ (Paperman) | Vendor product pages | current | Competing overlay apps claim reduced eye strain via grain/contrast attenuation. No study cited. | Not evidence. Listed only to document that no independent research on texture overlays was found. |

Rejected sources: vendor blogs (KTC, BenQ, ViewSonic, Arzopa, Alibaba) on matte vs glossy. One of them cites "a 2022 study in the Journal of Occupational Health and Ergonomics ... 37% fewer symptoms"; a targeted search found no such journal or study. Treat as unverifiable and do not use.

## Claims the page can make (with the supporting source)

1. Glare and reflections on a glossy screen make text harder to see and are a recognised contributor to eye strain and fatigue. -- S4 (AOA), S5 (OSHA), S1/S3 (AAO).
2. Eye-care and workplace-ergonomics bodies recommend reducing glare, including using a matte or anti-glare screen filter. -- S1, S3, S4, S5. (OSHA's caveat: a filter should not significantly reduce visibility, S5.)
3. Digital eye strain is common; estimates put it at half or more of regular computer users. -- S6.
4. A screen that is much brighter than the room makes your eyes work harder; match screen brightness to surroundings. -- S1, S3.
5. People blink far less at screens (roughly 5-7 vs 15 times a minute), which dries the eyes; consciously blinking and taking breaks helps. -- S1, S4.
6. The 20-20-20 rule: every 20 minutes look at something 20 feet away for 20 seconds. -- S4 (AOA). (AAO S1 gives the same advice without the "20-20-20" label.)
7. Room lighting matters: avoid windows and overhead lights reflecting in the screen; moderate, indirect lighting is recommended for screen work. -- S5.
8. In a controlled study, long reading on a bright backlit LCD produced more reported visual fatigue and fewer blinks than reading on E-ink or paper, which were indistinguishable; the authors linked this to the LCD's higher brightness. -- S7. (Say "one study," not "studies show.")
9. Accessibility guidance for dyslexic readers prefers off-white or cream backgrounds over pure white, which some people find glaring. -- S15, S16.
10. Blue light from screens has not been shown to damage the eyes. -- S2, S3, S12.
11. Screen discomfort is mostly about how we use screens (blinking less, glare, brightness, distance), not blue light. -- S2, S12.
12. Bright screen light in the evening can delay the body clock and make it harder to fall asleep; in a lab study, reading a bright tablet before bed suppressed melatonin and delayed sleep compared with a printed book. -- S8, S9, S2.
13. Studies of Night Shift-style warm colour modes have found little or no measurable effect on melatonin or sleep on their own; brightness appears to matter more than colour. -- S10, S11. (State this plainly; it is the honest counterpoint to claim 12.)
14. Warm tint is offered as a comfort preference for evening use, consistent with general advice to dim and warm screens at night, not as a sleep or health treatment. -- S2, S9, S13 (what the OS itself claims), bounded by S10/S11.
15. Parchmatte's specific texture overlay has not been independently studied; the claims above are about glare, brightness and contrast in general. -- S18 gap finding.

## Claims to avoid

- "Parchmatte reduces eye strain" / "reduces eye strain by N%". No study of texture overlays exists (S18 gap); the 37% matte figure is unverifiable.
- "Lower contrast is easier to read." The polarity literature (S14) shows dark-on-light with good contrast reads *best*; AAO (S1) even advises *increasing* contrast. Say "softer" or "less glaring," and be explicit that text stays legible.
- "Warm tint helps you sleep" / "protects your eyes from blue light" / "blocks harmful blue light." Contradicted or unsupported by S2, S10, S11, S12.
- "Blue light damages your eyes." Contradicted by S2, S3, S12.
- Any "prevents/treats computer vision syndrome," "doctor recommended," "clinically proven," or headache/migraine relief claims. No source.
- Citing OSHA as endorsing software overlays; OSHA (S5) refers to physical glare filters, and warns filters must not reduce visibility.
- "Studies show matte screens cause less eye strain." Only guidance (S1, S3, S4, S5) and one E-ink/LCD study (S7, about backlight brightness) exist; no direct matte-vs-glossy RCT was found.
- Presenting Benedetto 2013 (S7) as evidence for texture; it is about luminance/backlight.
- Any medical advice; include an "if symptoms persist, see an eye-care professional" line (AOA/AAO framing) rather than diagnostic language.

## Suggested page outline (plain language)

**H1:** Why a softer screen is easier on your eyes

Intro (2-3 sentences): Parchmatte adds a faint paper grain and an optional warm tint to a glossy Mac display. Here is what the research does and does not say about why that can feel more comfortable.

**H2: Glare is the problem everyone agrees on**
Glossy glass reflects windows and lights; AAO, AOA and OSHA all list glare as a cause of eye strain and recommend matte or anti-glare filters and repositioning the screen. (S1, S4, S5)

**H2: A screen that is brighter than the room makes your eyes work harder**
Brightness matching, evening dimming, ambient lighting. Include the E-ink study as one data point about backlight brightness. (S1, S3, S5, S7)

**H2: Paper-like, not low-contrast**
Explain the design goal: keep dark text on a light background legible (the polarity research), but take the edge off pure white and specular shine; note dyslexia guidance favouring off-white. (S14, S15, S16)

**H2: Blue light, warm tint and sleep: the honest version**
Blue light does not harm eyes (AAO). Evening bright screens can shift the body clock (Chang 2015). Colour-shift modes alone show little measured sleep benefit (Nagare 2019, Duraccio 2021); Cochrane 2023 on blue-blocking glasses. Warm tint in Parchmatte is a comfort preference. (S2, S8, S9, S10, S11, S12, S13)

**H2: Habits that matter more than any app**
20-20-20, blink, distance (about arm's length), room lighting, regular eye exams; see a professional if symptoms persist. (S1, S4, S5)

**H2: What we do not know**
No independent study of texture overlays, including Parchmatte, exists. What we would want tested. (S18)

**FAQ (3 questions)**
1. *Does Parchmatte reduce eye strain?* It reduces two things that guidance links to strain: perceived glare and harsh white brightness. Its specific effect has not been independently measured. (S1, S4, S5, S18)
2. *Does the warm tint help me sleep?* Evening bright screens can delay sleep; studies of warm-colour modes alone found little or no effect. Treat the tint as comfort, and dim the screen and stop earlier if sleep is the goal. (S8, S10, S11)
3. *Is blue light from my Mac damaging my eyes?* No evidence says so, per the American Academy of Ophthalmology and a 2023 Cochrane review. (S2, S12)

## Gaps and verification notes

- Full texts of S6 (BMJ Open Ophth), S10 (PMC), S11 (Sleep Health) and PubMed returned 403/CAPTCHA/cookie walls during this session; findings for these were taken from abstracts as reported by search summaries and reputable secondary coverage. Before publishing quotes, open them in a browser and confirm wording.
- S16 BDA style guide URL needs locating (current PDF is hosted under bdadyslexia.org.uk; the path tried was 404).
- No matte-vs-glossy controlled trial was found; the page should rely on guidance bodies for that point.
- No source exists for grain/texture overlays specifically (S18).
