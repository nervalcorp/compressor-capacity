#!/usr/bin/env python3
"""Generate index.html: single-file capacity reference page with embedded data."""
import argparse
import json
import os

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--data", default="build/data.json", help="path to data.json")
ap.add_argument("--out", help="output HTML path (default: alongside data.json)")
ap.add_argument("--release", action="store_true",
                help="drop the PROVISIONAL banner; only for confirmed data")
args = ap.parse_args()

with open(args.data, encoding="utf-8") as fh:
    data = json.load(fh)

if args.release:
    data.pop("status", None)

payload = json.dumps(data, separators=(",", ":"))

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Condensing Unit Capacity Tables &mdash; ICC / Keeprite comparison</title>
<meta name="description" content="Rated cooling capacity tables for ICC condensing units and their Keeprite/InvoTech compressor equivalents, across R404A, R507, R452A, R449A and R448A.">
<style>
/* ============================================================
   PALETTE — cold-chain instrument panel
   ============================================================ */
:root{
  --ink:#0F1720;
  --ink-2:#3D4C5A;
  --ink-3:#6B7B8A;
  --page:#E8EDF1;
  --panel:#FFFFFF;
  --rule:#C9D3DB;
  --rule-soft:#E2E9EE;
  --mbp:#0B6E75;
  --lbp:#2F4B99;
  --caution:#A8500A;
  --caution-bg:#FBEADB;
  --note:#7A6314;
  --note-bg:#FBF3D6;
  --standard-bg:#DFE7F3;
  --up:#0B6E75;
  --down:#A8500A;
  --accent:var(--mbp);
  --shadow:0 1px 0 rgba(15,23,32,.04), 0 8px 24px -14px rgba(15,23,32,.35);
  --sans:Arial,Helvetica,"Liberation Sans",sans-serif;
  --mono:"Courier New",Courier,monospace;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0;
  background:var(--page);
  color:var(--ink);
  font-family:var(--sans);
  font-size:15px;
  line-height:1.5;
}
h1,h2,h3{margin:0;font-family:var(--sans);font-weight:600;letter-spacing:.005em}
a{color:var(--accent)}

.eyebrow{
  font-family:var(--sans);
  font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.16em;
  color:var(--ink-3);
}

/* ---------- masthead ---------- */
.masthead{
  background:var(--ink);
  color:#F2F6F8;
  padding:22px 24px 20px;
  border-bottom:3px solid var(--accent);
}
.masthead-inner{max-width:1560px;margin:0 auto;display:flex;flex-wrap:wrap;gap:20px;align-items:flex-end;justify-content:space-between}
.masthead .eyebrow{color:#7F98A6}
.masthead h1{font-size:27px;line-height:1.1;margin-top:4px;color:#FFF}
.masthead .src{
  font-family:var(--sans);font-size:11.5px;color:#93A9B6;
  max-width:38ch;text-align:right;line-height:1.6;margin:0;
}
.masthead .src b{overflow-wrap:anywhere}
.masthead .src b{color:#CFDDE5;font-weight:500}

/* ---------- toolbar ---------- */
.toolbar{
  position:sticky;top:0;z-index:60;
  background:rgba(255,255,255,.94);
  backdrop-filter:saturate(140%) blur(8px);
  border-bottom:1px solid var(--rule);
}
.toolbar-inner{
  max-width:1560px;margin:0 auto;padding:9px 24px;
  display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;
}
.tgroup{display:flex;align-items:center;gap:7px}
.tgroup > .eyebrow{font-size:10px;letter-spacing:.13em}
.seg{display:inline-flex;border:1px solid var(--rule);border-radius:5px;overflow:hidden;background:#fff}
.seg button{
  appearance:none;border:0;background:transparent;cursor:pointer;
  font-family:var(--sans);font-size:12.5px;font-weight:600;
  color:var(--ink-2);padding:5px 11px;line-height:1.4;
  border-right:1px solid var(--rule-soft);
}
.seg button:last-child{border-right:0}
.seg button[aria-pressed="true"]{background:var(--accent);color:#fff}
.seg button:focus-visible{outline:2px solid var(--ink);outline-offset:-2px}
.btn{
  appearance:none;cursor:pointer;background:#fff;border:1px solid var(--rule);border-radius:5px;
  font-family:var(--sans);font-size:12.5px;font-weight:600;color:var(--ink-2);
  padding:6px 11px;
}
.btn:hover{border-color:var(--ink-3);color:var(--ink)}
.btn:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
.search{
  border:1px solid var(--rule);border-radius:5px;background:#fff;padding:6px 10px;
  font-family:var(--sans);font-size:12.5px;color:var(--ink);width:190px;
}
.search:focus{outline:2px solid var(--accent);outline-offset:-1px;border-color:var(--accent)}
.readout{
  margin-left:auto;font-family:var(--sans);font-size:12px;color:var(--ink-3);
  white-space:nowrap;min-height:18px;
}
.readout b{color:var(--ink);font-weight:600}

/* ---------- layout ---------- */
.shell{max-width:1560px;margin:0 auto;padding:20px 24px 64px;display:grid;grid-template-columns:236px minmax(0,1fr);gap:22px;align-items:start}
.rail{position:sticky;top:56px;max-height:calc(100vh - 76px);overflow:auto;padding-right:2px}
.rail-group{margin-bottom:16px}
.rail-group > .eyebrow{display:block;padding:0 0 6px 2px;border-bottom:1px solid var(--rule);margin-bottom:6px}
.rail-btn{
  display:block;width:100%;text-align:left;cursor:pointer;
  background:transparent;border:1px solid transparent;border-radius:6px;
  padding:7px 9px;margin-bottom:2px;
}
.rail-btn:hover{background:#fff;border-color:var(--rule-soft)}
.rail-btn[aria-current="true"]{background:#fff;border-color:var(--rule);box-shadow:var(--shadow)}
.rail-btn[aria-current="true"] .rb-icc{color:var(--accent)}
.rb-icc{
  display:block;font-family:var(--sans);font-weight:700;font-size:14px;
  color:var(--ink);letter-spacing:.01em;
}
.rb-cmp{display:block;font-family:var(--sans);font-size:11px;color:var(--ink-3);margin-top:1px}
.rail-empty{font-size:12.5px;color:var(--ink-3);padding:8px 2px}

/* ---------- model header ---------- */
.model-head{
  background:var(--panel);border:1px solid var(--rule);border-radius:8px;
  padding:16px 18px;margin-bottom:18px;box-shadow:var(--shadow);
  display:flex;flex-wrap:wrap;gap:16px 28px;align-items:flex-start;
  border-left:4px solid var(--accent);
}
.mh-main{min-width:0}
.mh-main h2{font-size:24px;line-height:1.15}
.mh-main .sub{font-family:var(--sans);font-size:12.5px;color:var(--ink-3);margin-top:3px}
.mh-facts{display:flex;flex-wrap:wrap;gap:14px 22px;margin-left:auto;min-width:0}
.fact span{overflow-wrap:anywhere}
.fact{min-width:88px}
.fact .eyebrow{display:block;font-size:10px}
.fact span{font-family:var(--sans);font-size:13.5px;color:var(--ink);font-weight:500}

/* ---------- capacity block ---------- */
.block{
  background:var(--panel);border:1px solid var(--rule);border-radius:8px;
  margin-bottom:16px;box-shadow:var(--shadow);overflow:hidden;
}
.block-head{
  display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 12px;
  padding:10px 14px;border-bottom:1px solid var(--rule);
  background:var(--standard-bg);
}
.block[data-status="caution"] .block-head{background:var(--caution-bg)}
.block[data-status="note"] .block-head{background:var(--note-bg)}
.ref-name{font-family:var(--sans);font-size:18px;font-weight:700;letter-spacing:.01em}
.ref-qual{font-size:12.5px;color:var(--ink-2)}
.block[data-status="caution"] .ref-name,
.block[data-status="caution"] .ref-qual{color:var(--caution)}
.block[data-status="note"] .ref-qual{color:var(--note)}
.ref-icc{margin-left:auto;font-family:var(--sans);font-size:11.5px;color:var(--ink-3)}
.baseline-tag{
  font-family:var(--sans);font-size:10px;font-weight:700;
  text-transform:uppercase;letter-spacing:.12em;color:#fff;background:var(--ink-2);
  padding:2px 6px;border-radius:3px;
}

.tscroll{overflow-x:auto}
table.cap{border-collapse:separate;border-spacing:0;width:100%;min-width:940px}
table.cap th,table.cap td{
  border-right:1px solid var(--rule-soft);border-bottom:1px solid var(--rule-soft);
  padding:5px 8px;text-align:center;white-space:nowrap;
}
table.cap thead th{
  background:#F4F7F9;font-family:var(--sans);font-weight:600;
  font-size:12px;color:var(--ink-2);position:sticky;top:0;z-index:3;
}
table.cap thead tr:nth-child(2) th{top:29px}
th.cond{border-bottom:1px solid var(--rule);letter-spacing:.02em}
th.cond span{display:block;font-family:var(--sans);font-size:10.5px;color:var(--ink-3);font-weight:400}
th.unit{font-family:var(--sans);font-size:10.5px;font-weight:500;letter-spacing:.03em}
th.unit.w{color:var(--ink-3)}

/* sticky left columns */
th.c-model,td.c-model{
  position:sticky;left:0;z-index:4;background:#F4F7F9;
  border-right:1px solid var(--rule);min-width:118px;
}
th.c-suct,td.c-suct{
  position:sticky;left:118px;z-index:4;background:#F4F7F9;
  border-right:1px solid var(--rule);min-width:132px;
}
thead th.c-model,thead th.c-suct{z-index:6}
td.c-model{
  vertical-align:middle;font-family:var(--sans);font-weight:700;font-size:14px;
}
td.c-suct{font-size:12px;font-variant-numeric:tabular-nums;color:var(--ink-2);text-align:right}

td.v{font-size:12.5px;font-variant-numeric:tabular-nums;letter-spacing:.01em;text-align:right}

td.v.w{color:var(--ink-3);font-size:12px}
td.v.na{color:#A9B6C1;text-align:center;font-size:12.5px}
td.v.flag{color:var(--caution);font-weight:600;text-align:center;font-size:14px;cursor:help}
td.v.fixed{color:var(--caution);font-weight:700;cursor:help;
  text-decoration:underline dotted var(--caution);text-underline-offset:3px}
tbody tr:nth-child(even) td.c-suct{background:#EFF3F6}
tbody tr:nth-child(even) td.v{background:rgba(15,23,32,.018)}

/* crosshair */
tbody tr.hot td.c-suct{background:var(--accent);color:#fff}
td.v.hot{outline:1.5px solid var(--accent);outline-offset:-1.5px;position:relative;z-index:1}
th.hot{color:var(--accent)}

/* heat shading — the capacity field */
.block.shade td.v[data-i]{background-image:linear-gradient(to right,var(--sh),var(--sh))}

/* delta mode */
.block.delta td.v{color:var(--ink-3)}
.block.delta td.v.up{color:var(--up)}
.block.delta td.v.down{color:var(--down)}
.block.delta td.v.base{color:var(--ink-3)}

/* hidden unit columns */
table.cap.hide-w th.unit.w,table.cap.hide-w td.v.w{display:none}
table.cap.hide-b th.unit.b,table.cap.hide-b td.v.b{display:none}

/* ---------- legend / footer ---------- */
.legend{
  background:var(--panel);border:1px solid var(--rule);border-radius:8px;padding:14px 16px;
  margin-top:22px;font-size:12.5px;color:var(--ink-2);box-shadow:var(--shadow);
}
.legend h3{font-size:12px;text-transform:uppercase;letter-spacing:.14em;color:var(--ink-3);margin-bottom:8px}
.legend ul{margin:0;padding-left:0;list-style:none;display:grid;gap:6px}
.legend li{display:flex;gap:9px;align-items:flex-start}
.swatch{width:14px;height:14px;border-radius:3px;border:1px solid var(--rule);flex:0 0 auto;margin-top:2px}
.sw-std{background:var(--standard-bg)}
.sw-cau{background:var(--caution-bg);border-color:var(--caution)}
.sw-note{background:var(--note-bg);border-color:var(--note)}
.provisional{
  background:#6B2D0A;color:#FFE6D2;padding:8px 24px;font-size:12.5px;
  border-bottom:1px solid #8A3D10;
}
.provisional-inner{max-width:1560px;margin:0 auto;display:flex;gap:10px;align-items:baseline}
.provisional b{color:#FFF;text-transform:uppercase;letter-spacing:.12em;font-size:11px;white-space:nowrap}
.notes{
  background:var(--caution-bg);border:1px solid #E7C8A8;border-left:4px solid var(--caution);
  border-radius:8px;padding:13px 16px;margin-bottom:18px;font-size:12.5px;color:#6B3A08;
}
.notes h3{font-size:12px;text-transform:uppercase;letter-spacing:.14em;color:var(--caution);margin-bottom:6px}
.notes p{margin:0 0 4px}
.notes code{font-family:var(--mono);font-size:12px;background:rgba(168,80,10,.10);padding:1px 4px;border-radius:3px}
.foot{max-width:1560px;margin:0 auto;padding:0 24px 40px;font-size:12px;color:var(--ink-3)}

/* ---------- URL-driven embedding ---------- */
body.no-rail .shell{grid-template-columns:minmax(0,1fr)}
body.embed{background:transparent}
body.embed .shell{padding:0;max-width:none}
body.embed .toolbar-inner{max-width:none;padding-left:0;padding-right:0}
body.embed .block:last-of-type{margin-bottom:0}
body.bare .block{border-radius:0;border-left:0;border-right:0;box-shadow:none}

/* ---------- responsive ---------- */
@media (max-width:1080px){
  .shell{grid-template-columns:minmax(0,1fr);gap:14px}
  .rail{position:static;max-height:none;display:flex;gap:8px;overflow-x:auto;padding-bottom:6px}
  .rail-group{margin:0;display:flex;gap:6px;align-items:center;flex:0 0 auto}
  .rail-group > .eyebrow{border:0;padding:0 4px 0 0;margin:0;white-space:nowrap}
  .rail-btn{width:auto;white-space:nowrap;background:#fff;border-color:var(--rule-soft);margin:0}
  .masthead .src{text-align:left}
  .mh-facts{margin-left:0}
}
@media (max-width:640px){
  .masthead h1{font-size:22px}
  .shell{padding:14px 12px 48px}
  .toolbar-inner{padding:8px 12px}
  .readout{display:none}
  .search{width:130px}
}

/* ---------- print ---------- */
@media print{
  .toolbar,.rail,.btn,.masthead .src{display:none !important}
  .provisional{background:#fff;color:#6B2D0A;border:1.5px solid #6B2D0A;padding:5px 8px;margin:6px 0}
  .provisional b{color:#6B2D0A}
  body{background:#fff;font-size:10px}
  .masthead{background:#fff;color:#000;border-bottom:2px solid #000;padding:0 0 8px}
  .masthead h1{color:#000;font-size:18px}
  .masthead .eyebrow{color:#444}
  .shell{display:block;padding:10px 0;max-width:none}
  .block,.model-head,.legend{box-shadow:none;break-inside:avoid;page-break-inside:avoid}
  table.cap{min-width:0}
  table.cap th,table.cap td{padding:2px 4px}
  td.v{font-size:9px}
  thead th{position:static}
  th.c-model,td.c-model,th.c-suct,td.c-suct{position:static}
}
@media (prefers-reduced-motion:reduce){*{transition:none !important;animation:none !important}}
</style>
</head>
<body>

<header class="masthead">
  <div class="masthead-inner">
    <div>
      <span class="eyebrow" id="eyebrow"></span>
      <h1>Rated capacity by refrigerant, suction &amp; condensing temperature</h1>
    </div>
    <p class="src">
      Source workbook: <b id="srcName">&mdash;</b><br>
      <span id="srcCount">&mdash;</span>
    </p>
  </div>
</header>

<div class="provisional" id="provisional" hidden>
  <div class="provisional-inner">
    <b>Provisional</b>
    <span id="provisionalText"></span>
  </div>
</div>

<div class="toolbar">
  <div class="toolbar-inner">
    <div class="tgroup" data-part="search">
      <label class="eyebrow" for="q">Find</label>
      <input id="q" class="search" type="search" placeholder="ICC or compressor model" autocomplete="off">
    </div>
    <div class="tgroup" data-part="units">
      <span class="eyebrow">Show</span>
      <div class="seg" id="unitSeg" role="group" aria-label="Capacity units">
        <button type="button" data-unit="both" aria-pressed="true">Both</button>
        <button type="button" data-unit="btu" aria-pressed="false">BTU/H</button>
        <button type="button" data-unit="w" aria-pressed="false">Watts</button>
      </div>
    </div>
    <div class="tgroup" data-part="values">
      <span class="eyebrow">Values</span>
      <div class="seg" id="modeSeg" role="group" aria-label="Value display">
        <button type="button" data-mode="value" aria-pressed="true">Rated</button>
        <button type="button" data-mode="delta" aria-pressed="false">&Delta; vs R404A</button>
      </div>
    </div>
    <div class="tgroup" data-part="shading">
      <div class="seg" role="group" aria-label="Capacity shading">
        <button type="button" id="shadeBtn" aria-pressed="true">Capacity shading</button>
      </div>
    </div>
    <button type="button" class="btn" id="csvBtn" data-part="csv">Download CSV</button>
    <button type="button" class="btn" id="printBtn" data-part="print">Print</button>
    <p class="readout" id="readout" aria-live="polite"></p>
  </div>
</div>

<main class="shell">
  <aside class="rail" id="rail" aria-label="Model index"></aside>
  <section id="main"></section>
</main>

<p class="foot" id="foot"></p>

<script id="capacity-data" type="application/json">__DATA__</script>
<script>
/* ============================================================
   CONFIG — edit these, not the render code below
   ============================================================ */
const CONFIG = {
  /* Load data from an external file instead of the embedded block.
     Set to e.g. "data.json" when hosting on GitHub Pages with the
     JSON alongside index.html. Leave null to use the embedded copy. */
  dataUrl: null,

  /* Which refrigerant block acts as the baseline for the Δ column. */
  baselineRefrigerant: "R404A",

  /* Capacity shading on by default. */
  shadingOn: true,

  /* Shading ramp: rgb triplet + max alpha at the highest capacity in a block. */
  shadeRGB: [11, 110, 117],
  shadeMaxAlpha: 0.30,

  /* Rail grouping order. */
  groupOrder: ["Medium temp", "Low temp"],

  /* Accent per application group. */
  accents: { "Medium temp": "#0B6E75", "Low temp": "#2F4B99" },

  /* Line above the page title. Keep this brand-neutral until the dataset is
     confirmed and the owning brand has been decided. */
  eyebrow: "Condensing unit capacity reference",

  /* Named parts that ?hide= and ?show= understand. Any other token is read as
     a class name, so ?hide=ref-icc works too, as does ?hide=.ref-icc or #foot. */
  parts: {
    masthead:    ".masthead",
    provisional: ".provisional",
    toolbar:     ".toolbar",
    rail:        ".rail",
    search:      '[data-part="search"]',
    units:       '[data-part="units"]',
    values:      '[data-part="values"]',
    shading:     '[data-part="shading"]',
    csv:         '[data-part="csv"]',
    print:       '[data-part="print"]',
    readout:     ".readout",
    header:      ".model-head",
    facts:       ".mh-facts",
    notes:       ".notes",
    legend:      ".legend",
    footer:      ".foot",
    blockhead:   ".block-head"
  },

  /* Footer note. */
  footNote: "Capacities are manufacturer-rated values transcribed from the source workbook. " +
            "Blocks flagged as not released or reference only are shown for comparison and must not be quoted as published ratings."
};

/* ============================================================
   STATE
   ============================================================ */
const state = {
  data: null,
  sheetIndex: 0,
  unit: "both",     // both | btu | w
  mode: "value",    // value | delta
  shade: CONFIG.shadingOn,
  refs: [],
  filter: ""
};

const $  = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const el = (tag, cls, txt) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (txt != null) n.textContent = txt;
  return n;
};
const nf = new Intl.NumberFormat("en-CA");
const fmtT = v => String(v).replace("-", "\u2212");

/* ============================================================
   URL PARAMETERS
   ------------------------------------------------------------
   Everything the page shows can be driven from the query string, so one
   deployed file can serve several different iframe embeds.

     ?hide=masthead,provisional     hide named parts, or any class name
     ?show=header,legend            hide everything hideable except these
     ?embed=1                       preset: no masthead, rail, or footer,
                                    padding collapsed for an iframe
     ?bare=1                        also strip block borders and radius
     ?model=NT6226GK                open a model (accepts the ICC number too)
     ?ref=R404A,R507                show only these refrigerant blocks
     ?unit=btu|w|both               which columns
     ?mode=delta|value              rated numbers or delta vs baseline
     ?shade=0|1                     capacity shading
     ?height=1                      post height to the parent frame

   Hiding is done with injected CSS rather than by removing nodes, so it
   survives the re-render that happens on every model switch.
   ============================================================ */
const params = new URLSearchParams(location.search);

/* Turn a token into a selector. Named parts win; otherwise it is read as a
   class name, and a leading . or # is respected. Anything with characters
   that do not belong in a selector is dropped rather than injected. */
function partSelector(token){
  const t = String(token).trim();
  if (!t) return null;
  if (CONFIG.parts[t]) return CONFIG.parts[t];
  if (!/^[.#]?[A-Za-z][\w-]*$/.test(t)) return null;
  return /^[.#]/.test(t) ? t : "." + t;
}

function tokens(name){
  const raw = params.get(name);
  return raw ? raw.split(",").map(s => s.trim()).filter(Boolean) : [];
}

function applyUrlChrome(){
  const hide = new Set();

  if (params.get("embed") === "1" || params.get("embed") === "true"){
    ["masthead", "rail", "footer"].forEach(p => hide.add(p));
    document.body.classList.add("embed");
  }
  if (params.get("bare") === "1") document.body.classList.add("bare");

  tokens("hide").forEach(t => hide.add(t));

  /* ?show= is the inverse: keep the listed parts, hide the other named ones.
     It only ever touches names in CONFIG.parts, so page content is safe. */
  const keep = tokens("show");
  if (keep.length){
    const kept = new Set(keep);
    Object.keys(CONFIG.parts).forEach(p => { if (!kept.has(p)) hide.add(p); });
    kept.forEach(p => hide.delete(p));
  }

  if (!hide.size) return;

  const sels = Array.from(hide).map(partSelector).filter(Boolean);
  if (!sels.length) return;

  const style = document.createElement("style");
  style.textContent = sels.join(",") + "{display:none !important}";
  document.head.appendChild(style);

  if (hide.has("rail")) document.body.classList.add("no-rail");
}

/* Content-level parameters, read once at boot. */
function applyUrlState(){
  const unit = (params.get("unit") || "").toLowerCase();
  if (["both", "btu", "w"].includes(unit)){
    state.unit = unit;
    $$("#unitSeg button").forEach(x => x.setAttribute("aria-pressed", String(x.dataset.unit === unit)));
  }

  const mode = (params.get("mode") || "").toLowerCase();
  if (["value", "delta"].includes(mode)){
    state.mode = mode;
    $$("#modeSeg button").forEach(x => x.setAttribute("aria-pressed", String(x.dataset.mode === mode)));
  }

  const shade = params.get("shade");
  if (shade !== null){
    state.shade = !(shade === "0" || shade === "false");
    $("#shadeBtn").setAttribute("aria-pressed", String(state.shade));
  }

  state.refs = tokens("ref").map(r => r.toUpperCase());

  /* ?model= matches the compressor model or any ICC model on the sheet. */
  const want = (params.get("model") || "").trim().toUpperCase();
  if (want){
    const i = state.data.sheets.findIndex(s =>
      s.compressorModel.toUpperCase() === want ||
      s.iccModels.some(m => m.toUpperCase() === want));
    if (i > -1) state.sheetIndex = i;
  }
}

/* Report height to the parent frame so an iframe can size itself.
   Parent side:
     window.addEventListener("message", e => {
       if (e.data && e.data.type === "capacity-tables:height")
         iframe.style.height = e.data.height + "px";
     }); */
function reportHeight(){
  if (params.get("height") !== "1" || window.parent === window) return;
  const post = () => window.parent.postMessage(
    { type: "capacity-tables:height", height: document.documentElement.scrollHeight }, "*");
  new ResizeObserver(post).observe(document.body);
  window.addEventListener("load", post);
  post();
}

/* ============================================================
   BOOT
   ============================================================ */
(async function init(){
  try {
    state.data = CONFIG.dataUrl
      ? await (await fetch(CONFIG.dataUrl)).json()
      : JSON.parse($("#capacity-data").textContent);
  } catch (err) {
    $("#main").innerHTML =
      '<div class="legend"><h3>Data did not load</h3>' +
      '<p>Check that <code>' + (CONFIG.dataUrl || "the embedded data block") +
      '</code> is present and valid JSON.</p></div>';
    return;
  }

  const d = state.data;
  const points = d.sheets.reduce((a, s) =>
    a + s.blocks.reduce((b, bl) => b + bl.rows.length * bl.rows[0].points.length, 0), 0);

  $("#srcName").textContent  = d.source;
  $("#srcCount").textContent =
    d.sheets.length + " compressor models \u00B7 " +
    d.sheets[0].blocks.length + " refrigerants each \u00B7 " +
    nf.format(points) + " rated points";
  $("#eyebrow").textContent = CONFIG.eyebrow;
  $("#foot").textContent = CONFIG.footNote;

  if (d.status){
    $("#provisionalText").textContent =
      d.status.replace(/^\s*provisional\s*[\u2014-]\s*/i, "") +
      ". Values are still being checked against manufacturer data \u2014 do not quote " +
      "from this page in quotations, submittals or published literature.";
    $("#provisional").hidden = false;
  }

  applyUrlChrome();
  bindToolbar();

  const fromHash = d.sheets.findIndex(s => s.name === location.hash.replace(/^#/, ""));
  if (fromHash > -1) state.sheetIndex = fromHash;
  applyUrlState();

  renderRail();
  renderSheet();
  reportHeight();

  window.addEventListener("hashchange", () => {
    const i = state.data.sheets.findIndex(s => s.name === location.hash.replace(/^#/, ""));
    if (i > -1 && i !== state.sheetIndex) { state.sheetIndex = i; renderRail(); renderSheet(); }
  });
})();

/* ============================================================
   TOOLBAR
   ============================================================ */
function bindToolbar(){
  $$("#unitSeg button").forEach(b => b.addEventListener("click", () => {
    state.unit = b.dataset.unit;
    $$("#unitSeg button").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
    applyUnit();
  }));

  $$("#modeSeg button").forEach(b => b.addEventListener("click", () => {
    state.mode = b.dataset.mode;
    $$("#modeSeg button").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
    renderSheet();
  }));

  const sb = $("#shadeBtn");
  sb.setAttribute("aria-pressed", String(state.shade));
  sb.addEventListener("click", () => {
    state.shade = !state.shade;
    sb.setAttribute("aria-pressed", String(state.shade));
    $$(".block").forEach(n => n.classList.toggle("shade", state.shade));
  });

  $("#q").addEventListener("input", e => { state.filter = e.target.value.trim().toLowerCase(); renderRail(); });
  $("#printBtn").addEventListener("click", () => window.print());
  $("#csvBtn").addEventListener("click", downloadCSV);
}

function applyUnit(){
  $$("table.cap").forEach(t => {
    t.classList.toggle("hide-w", state.unit === "btu");
    t.classList.toggle("hide-b", state.unit === "w");
  });
}

/* ============================================================
   RAIL
   ============================================================ */
function renderRail(){
  const rail = $("#rail");
  rail.textContent = "";
  const f = state.filter;

  const groups = new Map(CONFIG.groupOrder.map(g => [g, []]));
  state.data.sheets.forEach((s, i) => {
    const hay = (s.name + " " + s.iccModel).toLowerCase();
    if (f && !hay.includes(f)) return;
    if (!groups.has(s.application)) groups.set(s.application, []);
    groups.get(s.application).push({ s, i });
  });

  let any = false;
  groups.forEach((items, name) => {
    if (!items.length) return;
    any = true;
    const g = el("div", "rail-group");
    g.appendChild(el("span", "eyebrow", name));
    items.forEach(({ s, i }) => {
      const b = el("button", "rail-btn");
      b.type = "button";
      b.setAttribute("aria-current", String(i === state.sheetIndex));
      b.appendChild(el("span", "rb-icc", s.iccModel));
      b.appendChild(el("span", "rb-cmp", s.compressorModel));
      b.addEventListener("click", () => {
        state.sheetIndex = i;
        history.replaceState(null, "", "#" + s.name);
        renderRail();
        renderSheet();
        window.scrollTo({ top: 0, behavior: "auto" });
      });
      g.appendChild(b);
    });
    rail.appendChild(g);
  });

  if (!any) rail.appendChild(el("p", "rail-empty", "No model matches \u201C" + state.filter + "\u201D."));
}

/* ============================================================
   SHEET
   ============================================================ */
function renderSheet(){
  const s = state.data.sheets[state.sheetIndex];
  const main = $("#main");
  main.textContent = "";
  document.documentElement.style.setProperty("--accent", CONFIG.accents[s.application] || CONFIG.accents["Medium temp"]);

  /* header card */
  const head = el("div", "model-head");
  const mh = el("div", "mh-main");
  mh.appendChild(el("h2", null, s.iccModels.join(" \u00B7 ")));
  mh.appendChild(el("p", "sub", "Keeprite / InvoTech compressor " + s.compressorModel));
  head.appendChild(mh);

  const facts = el("div", "mh-facts");
  const rows = s.blocks[0].rows;
  addFact(facts, "Application", s.application);
  const factRefs = state.refs.length
    ? s.blocks.filter(b => state.refs.includes(b.refrigerant.toUpperCase()))
    : s.blocks;
  addFact(facts, "Refrigerants", (factRefs.length ? factRefs : s.blocks).map(b => b.refrigerant).join(", "));
  addFact(facts, "Suction range", fmtT(rows[rows.length - 1].f) + "\u2009\u2013\u2009" + fmtT(rows[0].f) + " \u00B0F");
  addFact(facts, "Condensing range", fmtT(s.condensing[0].f) + "\u2009\u2013\u2009" + fmtT(s.condensing[s.condensing.length - 1].f) + " \u00B0F");
  head.appendChild(facts);
  main.appendChild(head);

  /* baseline for delta mode — always the full set, so ?ref= narrowing the
     visible blocks never changes what the percentages are measured against */
  const base = s.blocks.find(b => b.refrigerant === CONFIG.baselineRefrigerant) || s.blocks[0];

  const notes = renderNotes(s);
  if (notes) main.appendChild(notes);

  const shown = state.refs.length
    ? s.blocks.filter(b => state.refs.includes(b.refrigerant.toUpperCase()))
    : s.blocks;

  if (!shown.length){
    const box = el("div", "legend");
    box.appendChild(el("h3", null, "Nothing to show"));
    box.appendChild(el("p", null,
      "No refrigerant on this model matches \u201C" + state.refs.join(", ") +
      "\u201D. Available: " + s.blocks.map(b => b.refrigerant).join(", ") + "."));
    main.appendChild(box);
  }

  shown.forEach(b => main.appendChild(renderBlock(s, b, base)));

  /* legend */
  main.appendChild(renderLegend());
  applyUnit();
}

function addFact(parent, label, value){
  const f = el("div", "fact");
  f.appendChild(el("span", "eyebrow", label));
  f.appendChild(el("span", null, value));
  parent.appendChild(f);
}

function renderBlock(sheet, block, base){
  const wrap = el("section", "block");
  wrap.dataset.status = block.status;
  if (state.shade) wrap.classList.add("shade");
  const isDelta = state.mode === "delta";
  const isBase  = block === base;
  if (isDelta) wrap.classList.add("delta");

  const bh = el("div", "block-head");
  bh.appendChild(el("span", "ref-name", block.refrigerant));
  if (block.qualifier) bh.appendChild(el("span", "ref-qual", block.qualifier));
  if (isDelta && isBase) bh.appendChild(el("span", "baseline-tag", "baseline"));
  bh.appendChild(el("span", "ref-icc", block.iccModel));
  wrap.appendChild(bh);

  /* max capacity in this block drives the shading ramp */
  let max = 0;
  block.rows.forEach(r => r.points.forEach(p => { if (p.btu != null && p.btu > max) max = p.btu; }));

  const table = el("table", "cap");

  /* head */
  const thead = el("thead");
  const r1 = el("tr");
  const thM = el("th", "c-model", sheet.headers.modelCol); thM.rowSpan = 2; r1.appendChild(thM);
  const thS = el("th", "c-suct", sheet.headers.suctionCol); thS.rowSpan = 2; r1.appendChild(thS);
  sheet.condensing.forEach((c, i) => {
    const th = el("th", "cond");
    th.colSpan = 2;
    th.dataset.col = i;
    th.appendChild(document.createTextNode(String(c.f) + " \u00B0F"));
    th.appendChild(el("span", null, c.c + " \u00B0C"));
    r1.appendChild(th);
  });
  thead.appendChild(r1);

  const r2 = el("tr");
  sheet.condensing.forEach((c, i) => {
    const a = el("th", "unit b", sheet.headers.btuLabel);  a.dataset.col = i; r2.appendChild(a);
    const w = el("th", "unit w", sheet.headers.wattLabel); w.dataset.col = i; r2.appendChild(w);
  });
  thead.appendChild(r2);
  table.appendChild(thead);

  /* body */
  const tbody = el("tbody");
  block.rows.forEach((row, ri) => {
    const tr = el("tr");
    tr.dataset.f = row.f;
    if (ri === 0){
      const tdm = el("td", "c-model", sheet.compressorModel);
      tdm.rowSpan = block.rows.length;
      tr.appendChild(tdm);
    }
    tr.appendChild(el("td", "c-suct", row.label));

    row.points.forEach((p, ci) => {
      const bp = base.rows[ri].points[ci];
      const bad = p.bad || {}, fx = p.fixed || {};
      tr.appendChild(cell(p.btu, bp.btu, "b", ci, max, isDelta, isBase, bad.btu, fx.btu));
      tr.appendChild(cell(p.w,  bp.w,  "w", ci, max, isDelta, isBase, bad.w,   fx.w));
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);

  const scroll = el("div", "tscroll");
  scroll.appendChild(table);
  wrap.appendChild(scroll);

  bindCrosshair(table, sheet, block);
  return wrap;
}

function cell(val, baseVal, kind, colIndex, max, isDelta, isBase, bad, fixed){
  const td = el("td", "v " + kind);
  td.dataset.col = colIndex;

  /* a flagged cell: the source held something that is neither a number nor "-" */
  if (bad){
    td.classList.add("flag");
    td.textContent = "\u26A0";
    td.title = "Source cell contains \u201C" + bad + "\u201D, not a number. See source data notes.";
    return td;
  }
  /* "-" in the source: condition outside the published rating envelope */
  if (val == null){
    td.classList.add("na");
    td.textContent = "\u2014";
    td.title = "Not rated at this condition";
    return td;
  }

  td.dataset.i = "1";
  if (fixed != null){
    td.classList.add("fixed");
    td.title = "Corrected value \u2014 the source workbook holds a typo in this cell. See source data notes.";
  }

  if (isDelta){
    if (isBase || baseVal == null){
      td.textContent = nf.format(val);
      td.classList.add("base");
    } else {
      const pct = ((val - baseVal) / baseVal) * 100;
      td.textContent = (pct > 0 ? "+" : pct < 0 ? "\u2212" : "") + Math.abs(pct).toFixed(1) + "%";
      if (pct > 0.05) td.classList.add("up");
      else if (pct < -0.05) td.classList.add("down");
      td.title = nf.format(val) + " vs " + nf.format(baseVal);
    }
  } else {
    td.textContent = nf.format(val);
  }

  if (kind === "b" && max){
    const a = (val / max) * CONFIG.shadeMaxAlpha;
    td.style.setProperty("--sh", "rgba(" + CONFIG.shadeRGB.join(",") + "," + a.toFixed(3) + ")");
  } else if (kind === "w"){
    td.style.setProperty("--sh", "rgba(0,0,0,0)");
  }
  return td;
}

/* crosshair: highlight the row + condensing column under the pointer,
   and echo the operating point in the toolbar readout. */
function bindCrosshair(table, sheet, block){
  const readout = $("#readout");
  const clear = () => {
    $$("tr.hot, td.hot, th.hot", table).forEach(n => n.classList.remove("hot"));
  };

  table.addEventListener("mouseover", e => {
    const td = e.target.closest("td.v");
    if (!td) return;
    clear();
    const col = td.dataset.col;
    const tr  = td.closest("tr");
    tr.classList.add("hot");
    $$('[data-col="' + col + '"]', table).forEach(n => {
      if (n.tagName === "TH") n.classList.add("hot");
    });
    $$('td.v[data-col="' + col + '"]', tr).forEach(n => n.classList.add("hot"));

    const suct = fmtT(tr.dataset.f);
    const cond = fmtT(sheet.condensing[+col].f);
    const cells = $$('td.v[data-col="' + col + '"]', tr);
    readout.innerHTML =
      block.refrigerant + " \u00B7 suction <b>" + suct + "\u00B0F</b> \u00B7 condensing <b>" +
      cond + "\u00B0F</b> \u2192 <b>" + cells[0].textContent + "</b> BTU/H \u00B7 <b>" +
      cells[1].textContent + "</b> W";
  });

  table.addEventListener("mouseleave", () => { clear(); readout.textContent = ""; });
}

/* Source anomalies affecting the current model, surfaced rather than silently patched. */
function renderNotes(sheet){
  const m     = sheet.compressorModel;
  const fixes = (state.data.corrections || []).filter(i => i.sheet === m);
  const hits  = (state.data.issues      || []).filter(i => i.sheet === m);
  if (!fixes.length && !hits.length) return null;

  const box = el("div", "notes");
  box.appendChild(el("h3", null, "Source data notes"));

  const where = i => i.refrigerant + ", suction " + i.suction + " \u00B0F, condensing " +
                     i.condensing + " \u00B0F, " + i.unit;

  fixes.forEach(i => {
    const p = el("p");
    p.innerHTML = "Corrected: cell <code>" + i.sheet + "!" + i.cell + "</code> (" + where(i) +
      ") holds <code>" + i.raw + "</code> in the workbook and is shown here as <b>" +
      nf.format(i.corrected) + "</b>. " + i.reason;
    box.appendChild(p);
  });

  hits.forEach(i => {
    const p = el("p");
    p.innerHTML = "Cell <code>" + i.sheet + "!" + i.cell + "</code> (" + where(i) +
      ") holds <code>" + i.raw + "</code> instead of a number. It is shown as \u26A0 and " +
      "excluded from shading and \u0394 calculations.";
    box.appendChild(p);
  });
  return box;
}

/* ============================================================
   LEGEND
   ============================================================ */
function renderLegend(){
  const box = el("div", "legend");
  box.appendChild(el("h3", null, "Reading these tables"));
  const ul = el("ul");
  const items = [
    ["sw-std",  "Blue header \u2014 rated or released. Published or co-rated data suitable for selection."],
    ["sw-cau",  "Peach header \u2014 not released or not suitable. Carried for comparison only; do not quote as a rating."],
    ["sw-note", "Yellow header \u2014 released with a qualifier. Check the note beside the refrigerant before selecting."],
    [null, "An em dash means the source lists no rating at that condition \u2014 the point sits outside the published envelope for that compressor and refrigerant."],
    [null, "Columns are saturated condensing temperature; rows are saturated suction temperature. Each pair gives gross capacity in BTU/H and Watts."],
    [null, "Shading tracks capacity within a block, so the operating envelope reads at a glance. Switch to \u0394 vs R404A to see how each alternative refrigerant shifts capacity at the same conditions."]
  ];
  items.forEach(([cls, text]) => {
    const li = el("li");
    li.appendChild(el("span", "swatch " + (cls || ""), ""));
    if (!cls) li.firstChild.style.visibility = "hidden";
    li.appendChild(el("span", null, text));
    ul.appendChild(li);
  });
  box.appendChild(ul);
  return box;
}

/* ============================================================
   CSV EXPORT — current model, all refrigerant blocks
   ============================================================ */
function downloadCSV(){
  const s = state.data.sheets[state.sheetIndex];
  const q = v => {
    const t = String(v ?? "");
    return /[",\n]/.test(t) ? '"' + t.replace(/"/g, '""') + '"' : t;
  };
  const lines = [];

  s.blocks.forEach(b => {
    lines.push([b.iccModel, b.label].map(q).join(","));
    const h1 = [s.headers.modelCol, s.headers.suctionCol];
    s.condensing.forEach(c => h1.push(c.label, ""));
    lines.push(h1.map(q).join(","));
    const h2 = ["", s.headers.suctionUnits];
    s.condensing.forEach(() => h2.push(s.headers.btuLabel, s.headers.wattLabel));
    lines.push(h2.map(q).join(","));
    b.rows.forEach((r, i) => {
      const line = [i === 0 ? s.compressorModel : "", r.label];
      r.points.forEach(p => line.push(
        p.btu == null ? ((p.bad && p.bad.btu) || "-") : p.btu,
        p.w   == null ? ((p.bad && p.bad.w)   || "-") : p.w));
      lines.push(line.map(q).join(","));
    });
    lines.push("");
  });

  const blob = new Blob(["\uFEFF" + lines.join("\r\n")], { type: "text/csv;charset=utf-8" });
  const a = el("a");
  a.href = URL.createObjectURL(blob);
  a.download = s.compressorModel + "_" + s.iccModels[0] + "_capacities.csv";
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 2000);
}
</script>
</body>
</html>
"""

html = TEMPLATE.replace("__DATA__", payload)
path = args.out or os.path.join(os.path.dirname(os.path.abspath(args.data)), "index.html")
with open(path, "w", encoding="utf-8") as fh:
    fh.write(html)
print(f"wrote {path}  ({os.path.getsize(path):,} bytes)")
