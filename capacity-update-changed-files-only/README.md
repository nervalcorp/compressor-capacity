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

## Embedding in an iframe

The page reads its own query string, so one deployed file can serve several
different embeds without maintaining separate copies.

| Parameter | Effect |
|---|---|
| `?hide=` | Hide named parts or raw class names, comma separated |
| `?show=` | The inverse — keep only these named parts, hide the other named ones |
| `?embed=1` | Preset: no masthead, rail or footer, padding collapsed |
| `?bare=1` | Also strip block borders, radius and shadow |
| `?model=` | Open a model — accepts `NT6226GK` or `SUIC1000` |
| `?ref=` | Show only these refrigerant blocks, e.g. `R404A,R452A` |
| `?unit=` | `btu`, `w`, or `both` |
| `?mode=` | `value` or `delta` |
| `?shade=` | `0` or `1` |
| `?height=1` | Post the page height to the parent frame |

Named parts for `hide` / `show`: `masthead`, `provisional`, `toolbar`, `rail`,
`search`, `units`, `values`, `shading`, `csv`, `print`, `readout`, `header`,
`facts`, `notes`, `legend`, `footer`, `blockhead`.

Any other token is read as a class name, so `?hide=ref-icc` works, as does
`?hide=.ref-icc` or `?hide=#foot`. Tokens that are not valid selectors are
ignored rather than injected. Hiding uses injected CSS, so it survives the
re-render that happens when you switch models.

```html
<!-- one model, one refrigerant, chrome stripped -->
<iframe src="https://.../index.html?embed=1&bare=1&model=SUIC530&ref=R404A&hide=provisional"
        style="width:100%;height:900px;border:0"></iframe>
```

### Auto-sizing the iframe

Add `&height=1` and the page posts its height to the parent:

```html
<iframe id="cap" src="https://.../index.html?embed=1&height=1"
        style="width:100%;border:0;height:400px"></iframe>
<script>
window.addEventListener("message", function (e) {
  if (e.data && e.data.type === "capacity-tables:height") {
    document.getElementById("cap").style.height = e.data.height + "px";
  }
});
</script>
```

`?ref=` narrows which blocks are drawn but never changes what Δ vs R404A is
measured against — the baseline is always taken from the full set, so a
single-refrigerant embed still shows correct percentages.

**`?hide=provisional` removes the warning banner.** That is fine for an
internal page where everyone already knows the data is being checked. On
anything a customer or contractor might see, leave the banner on — the numbers
look just as authoritative without it.

## Page features

Model index grouped by application and searchable · per-model hash links
(`index.html#NT6226GK`) · BTU/H, Watts or both · Δ vs R404A · capacity shading
· hover crosshair with readout · per-model CSV download · print stylesheet.

Typography is Arial only, with Courier New for cell references. No web fonts
and no external requests of any kind.
