# compressor-capacity

> **PROVISIONAL — DATA NOT CONFIRMED.**
> Every capacity value in this repository is transcribed from a working
> spreadsheet and is still being checked against manufacturer data. Do not
> quote these figures in quotations, submittals, brochures or spec sheets, and
> do not treat them as published ratings. See
> [`verification-log.md`](verification-log.md) for what has and has not been
> checked.

Rated cooling capacity for condensing units and their Keeprite / InvoTech
compressor equivalents — 15 compressor models, 5 refrigerants each (R404A,
R507, R452A, R449A, R448A), 7 condensing temperatures × 9 suction
temperatures. 4,725 rated points.

This is a temporary staging repository for verification work. It is
intentionally **not** connected to ICC Energy or iCoola — no shared branding,
no shared assets, no cross-imports. That comes later, if and when the data is
signed off.

## Contents

| Path | What it is |
|---|---|
| `index.html` | The capacity tables page. Self-contained — data embedded, no dependencies, no external requests. |
| `data.json` | The dataset, structured. |
| `csv/<MODEL>.csv` | One CSV per compressor model, laid out like the source spreadsheet sheet. |
| `csv/_all-capacities-long.csv` | Every rated point as one flat row, 4,725 rows. Best for pivot tables or Power Query. |
| `scripts/extract.py` | Spreadsheet → `data.json` + CSVs. |
| `scripts/build_page.py` | `data.json` → `index.html`. |
| `verification-log.md` | Per-model checklist, applied corrections, open questions. |

## Viewing it

Open `index.html` in a browser. It works straight off disk — no server needed.

If GitHub Pages is enabled on this repo it will also serve at
`https://nervalcorp.github.io/compressor-capacity/`. **Only enable Pages if
this repo is private or you are comfortable with provisional numbers being
publicly reachable.** The page carries a PROVISIONAL banner either way, but a
banner is not access control.

## Rebuilding after the spreadsheet changes

Needs Python 3 and `openpyxl` (`pip install openpyxl`).

```powershell
python scripts\extract.py --source "path\to\workbook.xlsx" --out build
python scripts\build_page.py --data build\data.json --out index.html
copy build\data.json data.json
xcopy /E /Y build\csv csv\
```

The `--release` flag on `build_page.py` removes the PROVISIONAL banner. Do not
use it until the data is confirmed.

## Fixing a wrong value

Do not edit `data.json`, the CSVs, or `index.html` directly — the next
extraction silently reverts the change and nobody can tell which values were
touched.

Instead add the cell to the `CORRECTIONS` map at the top of
`scripts/extract.py`, keyed by sheet and cell, with the corrected value and a
short reason naming the evidence:

```python
CORRECTIONS = {
    ("YF13E3G", "D9"): (
        3805,
        "Source cell held the letter 'a'. The R507 co-rated block on the same "
        "sheet gives 3805 W at this condition, and 12,983 BTU/H x 0.29307 = 3,805 W.",
    ),
}
```

Re-run both scripts. The corrected cell gets a dotted underline on the page
and the reason appears above the table, so a fix is never invisible. Once the
cell is fixed in the spreadsheet itself, delete the entry and re-extract.

## Page features

Model index grouped by application and searchable · per-model hash links
(`index.html#NT6226GK`) · BTU/H, Watts or both · Δ vs R404A · capacity shading
· hover crosshair with readout · per-model CSV download · print stylesheet.

Typography is Arial only, with Courier New for cell references. No web fonts
and no external requests of any kind.
