# Verification log

Tracks which parts of the dataset have been checked against manufacturer data
and which are still raw transcription from the workbook. Update this as
verification progresses so it is always clear what can be trusted.

**Overall status: PROVISIONAL.** Nothing below is confirmed yet.

## Legend

| Mark | Meaning |
|---|---|
| ✅ | checked against manufacturer data and confirmed |
| ⚠️ | discrepancy found — see notes, awaiting John's decision |
| ⬜ | not yet checked |

## Models

Transcription from the workbook is verified for all 15 sheets — 9,450 rendered
cells matched the source with zero mismatches. That is a *fidelity* check
only: it proves the page matches the workbook, not that the workbook matches
the manufacturer.

| Compressor | ICC model(s) | Application | Manufacturer check |
|---|---|---|---|
| SC10CL | SUIC386 | Medium temp | ⬜ |
| NEU6215GK | SUIC500, SUOC500 | Medium temp | ⬜ |
| SC15MLX | SUIC530 | Medium temp | ⬜ |
| NT6222GK | SUIC700, SUOC700 | Medium temp | ⬜ |
| NT6226GK | SUIC1000, SUOC1000, MBIC1000 | Medium temp | ⬜ |
| NJ9238GK | SUIC1500, SUOC1500, MBIC1500 | Medium temp | ⬜ |
| YM34E3G | SUOC2000 | Medium temp | ⬜ |
| YM49E3G | SUOC3000 | Medium temp | ⬜ |
| YM70E3G | SUOC4000 | Medium temp | ⬜ |
| SC10CLX | MBIC350 | Medium temp | ⬜ |
| SC18MLX | MBIC750 | Medium temp | ⬜ |
| NJ2212GJ | MBIF450 | Low temp | ⬜ |
| YF13E3G | MBIF600, SUIF2000, SUOF2000 | Low temp | ⬜ |
| YF20E3G | MBIF1000, SUIF1000, SUOF1000 | Low temp | ⬜ |
| YF29E3G | MBIF1500, SUIF1500, SUOF1500 | Low temp | ⬜ |
| YSF60E7G | SUOF3000 | Low temp | ⬜ |
| YSF75E7G | SUOF4000 | Low temp | ⬜ |

## Corrections applied

| Cell | Was | Now | Basis | Confirmed by John |
|---|---|---|---|---|
| `YF13E3G!D9` (R404A, 5 °F suction, 80 °F condensing, Watts) | `a` | 3805 | R507 co-rated block gives 3805 W at the same condition; 12,983 BTU/H × 0.29307 = 3,805 W | ✅ 2026-08-20 |

## ICC model numbers added outside the workbook

Held in `ICC_MODEL_ADDITIONS` in `scripts/extract.py`. These pairings are not in
the source spreadsheet's model column and are shown on the page with a note.

| Sheet | Added | Now reads | Confirmed by John |
|---|---|---|---|
| YF13E3G | SUIF2000 | MBIF600, SUIF2000, SUOF2000 | ✅ 2026-08-27 — from ERP, numbering flagged |
| YF13E3G | SUOF2000 | MBIF600, SUIF2000, SUOF2000 | ✅ 2026-08-27 — from ERP, numbering flagged |
| YF20E3G | SUOF1000 | MBIF1000, SUIF1000, SUOF1000 | ✅ 2026-08-24 |
| YF20E3G | SUIF1000 | MBIF1000, SUIF1000, SUOF1000 | ✅ 2026-08-27 |
| YF29E3G | SUOF1500 | MBIF1500, SUIF1500, SUOF1500 | ✅ 2026-08-24 |
| YF29E3G | SUIF1500 | MBIF1500, SUIF1500, SUOF1500 | ✅ 2026-08-27 |

Remove the entry once the workbook itself carries the number.

## Sheets staged outside the .xlsx

Same workbook as everything else, held as JSON only because the file with that
tab has not been uploaded. Replace with a direct extraction when it is.

| Sheet | Staged | Arithmetic check |
|---|---|---|
| YSF60E7G (SUOF3000) | 2026-08-28, `extra-sheets/YSF60E7G.json` | All 126 BTU/Watt pairs match ×0.29307 to within 0.006%; capacity monotonic on both axes. |
| YSF75E7G (SUOF4000) | 2026-08-28, `extra-sheets/YSF75E7G.json` | 125 of 126 BTU/Watt pairs match ×0.29307 to within 0.006%; capacity monotonic on both axes. One cell unreadable — see below. |

## Pinned for the InvoTech cross-check

Held in `SHEET_NOTES` in `scripts/extract.py` and shown on the affected model's
page under a "To review" tag. These are recorded as-is from the ERP, not
corrected — the plan is to revisit them once the variant/compressor pairings
are complete and cross-check against InvoTech or the most reliable source
available.

| Sheet | Issue |
|---|---|
| YSF75E7G | BTU/H at 30 °F suction / 80 °F condensing is column-overflowed (`#####`) in the source, in both the R404A and R507 blocks. Watts of 29,931 bounds it to 102,128–102,130. **Needs the exact figure from the workbook.** |
| YSF75E7G | R404A frequency-scaled from 50 Hz, same as SUOF3000. |
| YSF60E7G | R404A is published at 50 Hz and frequency-scaled on this sheet. Every other model's R404A block is published data at the rated frequency. Confirm the scaling factor. |
| YF13E3G | SUIF2000 / SUOF2000 sit with MBIF600. Every other sheet shares one suffix across its ICC models, and the number otherwise tracks capacity — here 2000 is on the second-smallest freezer (11,935 BTU/H at 5/90), below SUIF1000 (16,692) and SUIF1500 (24,280). |

## Open questions

Things noticed during extraction that are worth resolving during verification.
None of these are errors as such — they may be exactly as intended.

1. **Low-temp models carry medium-temp suction rows.** The MBIF sheets
   (NJ2212GJ, YF13E3G, YF20E3G, YF29E3G) list suction temperatures from 30 °F
   down to −10 °F, the same grid as the medium-temp sheets, rather than an LBP
   range. NJ2212GJ marks 30 through 15 °F as `-` (not rated); the YF sheets
   carry numbers across the whole range. Worth confirming those YF rows are
   real ratings and not a fill-down.

2. **R507 blocks are identical to R404A on every sheet.** Consistent with
   co-rating, and the labels say so on several sheets, but confirm this is
   intended rather than a copy of the block.

3. **Fill colour and label text disagree in places.** On NJ2212GJ the R449A
   and R448A blocks are labelled "NOT approved for LBP — reference only" but
   carry the blue "released" fill. On the YM sheets the R452A block is labelled
   plainly but carries the peach "caution" fill. The page shows both; the
   labels should win, but the fills are worth correcting in the workbook so the
   two agree.

4. **Freezer line-up may still be incomplete.** YF20E3G, YF29E3G and YF13E3G
   now carry a full MBIF + SUIF + SUOF trio. NJ2212GJ (MBIF450) still has no
   SUIF or SUOF number — either it has no indoor/outdoor variant, or two more
   numbers are missing.

5. **R449A and R448A blocks are identical to each other** wherever both appear,
   and on several sheets identical to R452A. Some of these are explicitly noted
   as proxies or estimates in the labels. Confirm which are genuine published
   data and which are placeholders, since the Δ vs R404A view will otherwise
   show them as real differences.

## History

| Date | Change |
|---|---|
| 2026-08-24 | Added SUOF1000 to YF20E3G and SUOF1500 to YF29E3G via `ICC_MODEL_ADDITIONS`. No capacity values changed. |
| 2026-08-28 | Added YSF75E7G / SUOF4000. 17 sheets, 5,355 rated points, one cell outstanding. |
| 2026-08-28 | Added YSF60E7G / SUOF3000 via the new `extra-sheets/` route. Numbers stored as text are now coerced silently instead of being flagged. 16 sheets, 5,040 rated points. |
| 2026-08-27 | Added SUIF2000 and SUOF2000 to YF13E3G from the ERP, with a pinned review note on the numbering. Added `SHEET_NOTES` mechanism. No capacity values changed. |
| 2026-08-27 | Added SUIF1000 to YF20E3G and SUIF1500 to YF29E3G. No capacity values changed. Live at https://nervalcorp.github.io/compressor-capacity/ |
| 2026-08-20 | Initial extraction from `_CLEAN__Condensing_Units_and_Evaps_-_Keeprite_for_comparison.xlsx`. 15 models, 5 refrigerants each, 4,725 rated points, 2,020 not-rated cells. One transcription error found and corrected. Page built and fidelity-checked at 9,450 cells. |
