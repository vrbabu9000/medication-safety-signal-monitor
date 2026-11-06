// MSSM hand-in demo deck (20 minutes). Builder: pptxgenjs 3.12 (installed outside the repo).
//   NODE_PATH=<dir with node_modules/pptxgenjs> node docs/11-handin/deck/build_deck.js
// Every number on a slide is read from docs/11-handin/numbers.json (captured from Foundry at the baseline gate).
// Pictures: docs/diagrams/png/30-37 (hand-in set), docs/11-handin/screens/*.jpg, and three crops in ./assets
// (made from those same files; see slide_explanations.md "Assets").
// Agenda (binding): docs/11-handin/AGENT-BRIEF.md "The 20-minute demo". Main slides 1-16, backup divider 17, backups B1-B12 = 18-29.
// Style: BlueJay midterm v0.4 (evidence pills, status bands, backups) in the hand-in palette (tools/handin/style.py).
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");

const HERE = __dirname;
const ROOT = path.join(HERE, "..", "..", "..");
const DIA = (f) => path.join(ROOT, "docs", "diagrams", "png", f);
const SCR = (f) => path.join(ROOT, "docs", "11-handin", "screens", f);
const ASSET = (f) => path.join(HERE, "assets", f);
const OUT = path.join(HERE, "MSSM-demo-deck.pptx");
const N = JSON.parse(fs.readFileSync(path.join(HERE, "..", "numbers.json"), "utf8"));
const SC = N.scope, RAW = N.raw, F = N.faers, SG = N.signals, NA = SG.naion, SY = N.synonyms, RC = N.recalls,
  CH = N.changes, AI = N.ai, MO = N.monitoring, OP = N.optimization, APP = N.app;

// ---------- formatting (derived values are computed here, never typed) ----------
const fmt = (x) => Number(x).toLocaleString("en-US");
const pct = (x, d = 0) => (100 * x).toFixed(d) + "%";
const mmss = (s) => `${Math.floor(s / 60)} m ${s % 60} s`;
const frac = (s) => s.split("/").map(Number); // "35/37" -> [35, 37]
const ratio = (a, b, d = 2) => (a / b).toFixed(d);
const capDate = N._meta.captured_at.slice(0, 10);
const [recN, recD] = frac(AI.gold_recall_strict);
const [p1N] = frac(AI.gold_recall_strict_p1);
const [precN, precD] = frac(AI.gold_precision_upper);
const o2slower = ratio(OP.O2.incremental_add_q2_s, OP.O2.full_rebuild_s);
const o3cut = Math.round(100 * (OP.O3.before_s - OP.O3.after_s) / OP.O3.before_s);
const rh = SG.ranked_history;
const queueCut = Math.round(100 * (rh.step9 - rh.syn_v2) / rh.step9);
const driftX = ratio(MO.recalls_last4w, MO.recalls_prev4w, 1);
const TM = APP.timing_s;
const switchMin = Math.min(TM.switch_recalls, TM.switch_what_changed, TM.switch_signals_with_labels), switchMax = Math.max(TM.switch_recalls, TM.switch_what_changed, TM.switch_signals_with_labels);
// Not in numbers.json: MSSM Product object count, from foundry/ontology/README.md (baseline gate). Cited on the slide where used.
const PRODUCTS_TRACKED = 658;
const formulary = `${SC.drugs_formulary} drugs (${SC.opioids} opioids + ${SC.glp1} GLP-1 drugs)`;

// ---------- palette: tools/handin/style.py ----------
const C = { navy: "13324B", teal: "087F8C", light: "EAF3F5", ink: "263746", gray: "607080", rule: "C9D6DC", white: "FFFFFF",
  greenF: "E1F5EE", greenE: "0F6E56", greenI: "085041", amberF: "FFF3D6", amberE: "B7791F", amberI: "7A4B00",
  stoneF: "F1EFE8", stoneE: "5F5E5A", stoneI: "444441", violetF: "EEEDFE", violetE: "534AB7", violetI: "3C3489",
  tealPillF: "D7EEF0", tealPillI: "05606A", red: "A33A3A", redF: "FBE9E7" };
const FONT = "Arial";
// Visual system 1: EVIDENCE (soft filled pill, dark text) — AGENT-BRIEF honesty rules
const EVID = { OBSERVED: [C.tealPillF, C.tealPillI], DERIVED: ["E3E8EE", C.ink], ASSUMED: [C.amberF, C.amberI],
  DESIGNED: [C.stoneF, C.stoneI], "AI OUTPUT": [C.violetF, C.violetI] };
// Visual system 2: EXECUTION STATUS (white band, coloured border, square corners; dashed = not built / not accepted)
const STATUS = { TESTED: ["BUILT · TESTED IN FOUNDRY", C.greenE, "solid"], PLANNED: ["PLANNED — NOT BUILT", C.amberE, "dash"],
  PROPOSED: ["DECISION PROPOSED — NOT YET ACCEPTED", C.red, "dash"], PARTLY: ["BUILT · PARTLY MEASURED", C.amberE, "solid"] };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
pres.title = "Medication Safety Signal Monitor — 20-minute hand-in demo";
pres.subject = "Soragence technical build brief: pilot on Palantir Foundry + AIP";
pres.company = "Medication Safety Signal Monitor (MSSM)";
pres.theme = { headFontFace: FONT, bodyFontFace: FONT };

pres.defineSlideMaster({ title: "TITLE_DARK", background: { color: C.navy }, objects: [] });
pres.defineSlideMaster({ title: "CONTENT", background: { color: C.white }, objects: [
  { rect: { x: 0, y: 0, w: 13.333, h: 0.09, fill: { color: C.teal }, line: { color: C.teal } } }] });
pres.defineSlideMaster({ title: "SECTION", background: { color: C.light }, objects: [
  { rect: { x: 0, y: 0, w: 0.22, h: 7.5, fill: { color: C.teal }, line: { color: C.teal } } }] });

// ---------- helpers ----------
let slideNo = 0;
const BK = {}; // backup id -> slide number, filled before use (fixed order below)
["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12"].forEach((b, i) => (BK[b] = 18 + i));

function txt(slide, text, o) {
  slide.addText(text, Object.assign({ isTextBox: true, fontFace: FONT, fontSize: 14, color: C.ink, margin: 0.04, valign: "top" }, o));
}
function source(slide, s) { txt(slide, "Source: " + s, { x: 0.5, y: 7.04, w: 11.4, h: 0.3, fontSize: 9, color: C.gray, valign: "middle" }); }
function evid(slide, kind, x, y, w) {
  const [f, c] = EVID[kind]; w = w || 1.25;
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.26, rectRadius: 0.13, fill: { color: f }, line: { color: f } });
  txt(slide, kind, { x, y, w, h: 0.26, fontSize: 9, bold: true, color: c, align: "center", valign: "middle", margin: 0 });
}
function status(slide, kind, x, y, w) {
  const [label, c, dash] = STATUS[kind]; w = w || 3.1;
  slide.addShape(pres.shapes.RECTANGLE, { x, y, w, h: 0.3, fill: { color: C.white }, line: { color: c, width: 1.5, dashType: dash } });
  txt(slide, label, { x, y, w, h: 0.3, fontSize: 9.5, bold: true, color: c, align: "center", valign: "middle", margin: 0 });
}
function live(slide, where, y) {
  y = y || 1.58;
  slide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y, w: 12.33, h: 0.4, fill: { color: C.navy }, line: { color: C.navy } });
  txt(slide, [{ text: "LIVE IN THE APP  ▶  ", options: { bold: true, color: "8FD3DA" } }, { text: where, options: { color: C.white } }],
    { x: 0.62, y, w: 12.1, h: 0.4, fontSize: 13, valign: "middle", margin: 0 });
}
function cue(slide, text, x, y, w) { // smaller "switch to" cue for under-the-hood stops
  slide.addShape(pres.shapes.RECTANGLE, { x, y, w, h: 0.34, fill: { color: C.navy }, line: { color: C.navy } });
  txt(slide, [{ text: "▶ SWITCH  ", options: { bold: true, color: "8FD3DA" } }, { text, options: { color: C.white } }],
    { x: x + 0.08, y, w: w - 0.12, h: 0.34, fontSize: 11, valign: "middle", margin: 0 });
}
function box(slide, x, y, w, h, fill, lineColor, o) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign({ x, y, w, h, rectRadius: 0.06, fill: { color: fill || C.light },
    line: { color: lineColor || fill || C.light, width: lineColor ? 1.25 : 0.75 } }, o || {}));
}
function card(slide, x, y, w, h, title, body, kind, o) {
  const k = { teal: [C.light, C.teal, C.navy], green: [C.greenF, C.greenE, C.greenI], amber: [C.amberF, C.amberE, C.amberI],
    stone: [C.stoneF, C.stoneE, C.stoneI], violet: [C.violetF, C.violetE, C.violetI], white: [C.white, C.rule, C.navy] }[kind || "teal"];
  box(slide, x, y, w, h, k[0], k[1], (o && o.dash) ? { line: { color: k[1], width: 1.25, dashType: "dash" } } : {});
  const runs = [{ text: title, options: { bold: true, color: k[2], breakLine: !!body } }];
  if (body) runs.push({ text: body, options: { color: C.ink } });
  txt(slide, runs, Object.assign({ x: x + 0.1, y: y + 0.05, w: w - 0.2, h: h - 0.1, fontSize: 12.5, valign: body ? "middle" : "top" }, (o && o.t) || {}));
}
function tile(slide, x, y, w, h, big, label, kind, ev) {
  const k = { teal: [C.light, C.navy], green: [C.greenF, C.greenI], amber: [C.amberF, C.amberI], violet: [C.violetF, C.violetI] }[kind || "teal"];
  box(slide, x, y, w, h, k[0]);
  txt(slide, big, { x: x + 0.1, y: y + 0.08, w: w - 0.2, h: 0.62, fontSize: 26, bold: true, color: k[1], valign: "middle" });
  txt(slide, label, { x: x + 0.1, y: y + 0.7, w: w - 0.2, h: h - 0.78, fontSize: 11.5, color: C.ink });
  if (ev) evid(slide, ev, x + w - 1.2, y + 0.1, 1.1);
}
function arrow(slide, x1, y1, x2, y2, color) {
  const o = { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.max(Math.abs(x2 - x1), 0.001), h: Math.max(Math.abs(y2 - y1), 0.001),
    line: { color: color || C.gray, width: 1.75, endArrowType: "triangle" } };
  if (x2 < x1) o.flipH = true;
  if (y2 < y1) o.flipV = true;
  slide.addShape(pres.shapes.LINE, o);
}
function bullets(slide, items, o) {
  const runs = items.map((t, i) => {
    const parts = Array.isArray(t) ? t : (typeof t === "string" ? [{ text: t }] : [t]);
    return parts.map((p, j) => ({ text: p.text, options: Object.assign({ bullet: j === 0 ? { indent: 14 } : undefined,
      breakLine: j === parts.length - 1 && i < items.length - 1, paraSpaceAfter: 5 }, p.options || {}) }));
  }).flat();
  slide.addText(runs, Object.assign({ isTextBox: true, fontFace: FONT, fontSize: 13.5, color: C.ink, valign: "top", margin: 0.04 }, o));
}
const B = (text) => ({ text, options: { bold: true } });
const T = (text) => ({ text });
function link(slide, label, target, o) {
  txt(slide, [{ text: label, options: { hyperlink: { slide: target, tooltip: "Go to slide " + target }, color: C.teal } }],
    Object.assign({ fontSize: 10, align: "right" }, o));
}
function img(slide, file, x, y, w, pxW, pxH, frame) {
  const h = w * pxH / pxW;
  slide.addImage({ path: file, x, y, w, h });
  if (frame !== false) slide.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { type: "none" }, line: { color: C.rule, width: 0.75 } });
  return h;
}
function lead(slide, text, o) { txt(slide, text, Object.assign({ x: 0.5, y: 1.0, w: 12.33, h: 0.52, fontSize: 14, color: C.teal, bold: true, valign: "middle" }, o)); }
function content(title, section, rubric, time, notes) {
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: section });
  slideNo++;
  txt(s, title, { x: 0.5, y: 0.22, w: 9.75, h: 0.8, fontSize: 22, bold: true, color: C.navy, valign: "middle" });
  // rubric + time chips (top right)
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 10.4, y: 0.26, w: 2.43, h: 0.3, rectRadius: 0.15, fill: { color: C.tealPillF }, line: { color: C.tealPillF } });
  txt(s, rubric, { x: 10.4, y: 0.26, w: 2.43, h: 0.3, fontSize: 9.5, bold: true, color: C.tealPillI, align: "center", valign: "middle", margin: 0 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 10.4, y: 0.62, w: 2.43, h: 0.3, rectRadius: 0.15, fill: { color: C.white }, line: { color: C.rule, width: 1 } });
  txt(s, time, { x: 10.4, y: 0.62, w: 2.43, h: 0.3, fontSize: 9.5, color: C.gray, align: "center", valign: "middle", margin: 0 });
  txt(s, String(slideNo), { x: 12.25, y: 7.06, w: 0.6, h: 0.26, fontSize: 9.5, color: C.gray, align: "right", valign: "middle", margin: 0 });
  const id = String(slideNo).padStart(2, "0");
  s.addNotes(`Script: speaking_script.md#s${id}. Handbook: slide_explanations.md#s${id}.` + (notes ? " " + notes : ""));
  return s;
}
const chartBase = (o) => Object.assign({ catAxisLabelFontFace: FONT, valAxisLabelFontFace: FONT, dataLabelFontFace: FONT, titleFontFace: FONT,
  catAxisLabelColor: C.ink, valAxisLabelColor: C.gray, valGridLine: { color: "E3E8EE", size: 0.5 }, catGridLine: { style: "none" },
  showLegend: false, showValue: true, dataLabelColor: C.ink, dataLabelFontSize: 11, catAxisLabelFontSize: 11, valAxisLabelFontSize: 9 }, o);
const hdr = (t) => ({ text: t, options: { bold: true, color: C.white, fill: { color: C.navy } } });
const TB = { fontFace: FONT, color: C.ink, border: { type: "solid", pt: 0.75, color: C.rule }, valign: "middle" };

// =====================================================================================================
// 1 TITLE                                                                                  0:00–0:20
pres.addSection({ title: "The officer's problem" });
let s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "The officer's problem" });
slideNo++;
txt(s, "Medication Safety Signal Monitor", { x: 0.7, y: 1.0, w: 11.9, h: 1.0, fontSize: 40, bold: true, color: C.white, valign: "bottom" });
txt(s, "A morning safety screen for a hospital pharmacy safety officer, built in Palantir Foundry from public FDA and NLM data. Every flag traces to its source.",
  { x: 0.7, y: 2.1, w: 11.6, h: 0.95, fontSize: 19, color: "C9D6DC" });
[["1", "Which drugs have side effects reported that the label does not mention?"], ["2", "Which drugs have an active recall?"], ["3", "What has changed since my last review?"]].forEach(([n, q], i) => {
  const x = 0.7 + i * 4.0;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 3.55, w: 3.75, h: 1.45, rectRadius: 0.08, fill: { color: "1C4562" }, line: { color: "8FD3DA", width: 1.25 } });
  txt(s, n, { x: x + 0.15, y: 3.65, w: 0.6, h: 0.6, fontSize: 28, bold: true, color: "8FD3DA" });
  txt(s, q, { x: x + 0.75, y: 3.65, w: 2.9, h: 1.25, fontSize: 15, color: C.white, valign: "middle" });
});
txt(s, `Pilot: ${formulary} · FAERS ${SC.faers_quarters} · numbers captured from Foundry ${capDate}`,
  { x: 0.7, y: 5.45, w: 11.9, h: 0.4, fontSize: 14, color: "C9D6DC" });
txt(s, "Soragence technical build brief · hand-in demo, 20 minutes: slides, then the live app, then under the hood",
  { x: 0.7, y: 6.75, w: 11.9, h: 0.35, fontSize: 12, color: "8FA6B8" });
s.addNotes("Script: speaking_script.md#s01. Handbook: slide_explanations.md#s01. Time 0:00–0:20.");

// 2 THE PROBLEM                                                                            0:20–1:30
s = content("Her three morning questions, and one trust rule", "The officer's problem", "Communication", "0:20–1:30 · slides");
lead(s, `Today she hears about drug safety problems late and from scattered places. We built one screen to answer her three questions: machine load ${TM.morning_brief_load} s; a human walk-through will be timed in rehearsal.`);
[["1 · Not in the label", "Which drugs have side effects being reported that their label does not mention?", "App page 1"],
 ["2 · Active recalls", "Which of my drugs are under an active FDA recall?", "App page 2"],
 ["3 · What changed", "What changed since my last review: new label versions, recalls, signals?", "App page 3"]].forEach(([h, b, p], i) => {
  const y = 1.75 + i * 1.12;
  card(s, 0.5, y, 6.6, 0.98, h, b, "teal", { t: { fontSize: 13.5 } });
  txt(s, p, { x: 5.9, y: y + 0.06, w: 1.1, h: 0.3, fontSize: 9.5, color: C.teal, bold: true, align: "right" });
});
card(s, 7.4, 1.75, 5.43, 1.2, "Trust rule", "Every flag traces to its source: the label versions searched (DailyMed) and the FDA recall record open in one click; the FAERS case reports are reachable by query, not yet from her screen.", "green", { t: { fontSize: 11.5 } });
card(s, 7.4, 3.08, 5.43, 1.55, "Scope we chose (narrow, working)", `${formulary} (D014, D018). Opioids: oxycodone, hydrocodone, morphine, fentanyl, hydromorphone, methadone, buprenorphine, tramadol. GLP-1s: semaglutide, liraglutide, dulaglutide, tirzepatide, exenatide.`, "stone", { t: { fontSize: 11 } });
evid(s, "DESIGNED", 11.6, 3.13, 1.15);
card(s, 7.4, 4.73, 5.43, 0.6, "Public data only", "No patient-level or proprietary data.", "white", { t: { fontSize: 12 } });
// glossary strip
const gl = [["FAERS", "FDA Adverse Event Reporting System: voluntary reports of side effects, released as quarterly files"],
  ["DailyMed (SPL)", "NLM site with the official drug labels, as Structured Product Labeling XML, every version"],
  ["openFDA", "FDA's public API; we use its recall (enforcement), Drugs@FDA and NDC endpoints"],
  ["RxNorm (RxCUI)", "NLM's standard drug names; one RxCUI id per ingredient joins all sources"]];
gl.forEach(([h, b], i) => {
  const x = 0.5 + i * 3.1;
  box(s, x, 5.7, 2.98, 1.1, C.white, C.rule);
  txt(s, [{ text: h, options: { bold: true, color: C.navy, breakLine: true } }, { text: b, options: { color: C.ink } }], { x: x + 0.1, y: 5.75, w: 2.8, h: 1.0, fontSize: 11 });
});
txt(s, "The four public sources", { x: 0.5, y: 5.42, w: 4, h: 0.28, fontSize: 10.5, bold: true, color: C.gray });
source(s, "docs/00-brief/brief-summary.md; DECISIONS D014 (8 opioids + 5 GLP-1), D018 (formulary = 13 RxCUIs); numbers.json scope.");

// 3 LIVE: MORNING BRIEF                                                                    1:30–3:00
pres.addSection({ title: "As the safety officer (live)" });
s = content("Morning brief: three numbers, and how fresh each source is", "As the safety officer (live)", "The application", "1:30–3:00 · app page 0");
lead(s, "One look answers all three questions. The table shows how old each source is: they update on different clocks.");
live(s, "Workshop module MSSM Safety Officer · tab “Morning brief” (page 0). Screenshot = fallback if the app is slow.");
let h = img(s, SCR("app-0-morning-brief.jpg"), 0.5, 2.15, 7.4, 1425, 840);
evid(s, "OBSERVED", 0.5, 2.25 + h, 1.15);
txt(s, `Timed (browser script, View mode): brief on screen in ${TM.morning_brief_load} s; page switches ${switchMin}–${switchMax} s. A human two-minute walk-through has not been run.`, { x: 1.75, y: 2.2 + h, w: 6.15, h: 0.4, fontSize: 10.5, color: C.ink, valign: "middle" });
tile(s, 8.4, 2.15, 4.43, 1.12, fmt(SG.ranked), "signals not in the label, ranked: a review queue, not findings", "teal", "OBSERVED");
tile(s, 8.4, 3.37, 4.43, 1.12, fmt(RC.active), `active recalls (status Ongoing) of ${fmt(RC.total)} recalls for our ${SC.drugs_formulary} drugs`, "teal", "OBSERVED");
tile(s, 8.4, 4.59, 4.43, 1.12, fmt(CH.last_30_days), "change events in the last 30 days (not “since yesterday”; page 3 narrows to “since my last review”)", "teal", "OBSERVED");
card(s, 8.4, 5.81, 4.43, 0.96, "Data as of",
  `FAERS through 2026Q2 (freshness check: ${MO.faers_age_days} days old); openFDA ${MO.openfda_age_days} days old at capture. Our pipeline refreshes when a build runs: no schedule yet.`, "amber", { t: { fontSize: 10 } });
source(s, `numbers.json (signals, recalls, changes, monitoring, app.timing_s), ${capDate}; screens/app-0-morning-brief.jpg; D045 proposed. The 30-day count is live.`);

// 4 LIVE: NOT IN LABEL                                                                     3:00–6:00
s = content("Not in label: from one flag to its evidence to a saved decision", "As the safety officer (live)", "Application · AI reliability", "3:00–6:00 · app page 1",
  `NAION a=${NA.a}, PRR ${NA.prr} (95% CI ${NA.prr_ci_low}–${NA.prr_ci_high}), chi2 ${NA.chi2_yates}.`);
lead(s, "NAION is semaglutide's top-ranked signal. Every number in its record traces to FAERS rows and the labels searched.");
live(s, "Page 1 → name the noise → semaglutide → NAION → Ozempic v20 on DailyMed, find “optic” → Triage.");
h = img(s, SCR("app-1c-labels-searched-naion.jpg"), 0.5, 2.15, 7.0, 1425, 840);
const steps4 = [
  [B("Flag "), T(`Filter to semaglutide; rank is within each drug. NAION (FAERS term “${NA.reaction}”), rank ${NA.rank}: sudden vision loss from poor blood flow to the optic nerve.`)],
  [B("Evidence "), T(`${fmt(NA.a)} of ${fmt(NA.all_reports_drug)} semaglutide reports name NAION. PRR ${NA.prr} (95% CI ${NA.prr_ci_low}–${NA.prr_ci_high}).`)],
  [B("Trace "), T(`${APP.labels_searched_naion} labels searched (Ozempic v20, Wegovy v19, oral v14): none mention it (exact text + synonyms; AI read 0). Open Ozempic v20 on DailyMed, find “optic”.`)],
  [B("Decide "), T("“Triage this signal”: decision saved with reviewer and time, never overwritten. Only the project owner can submit today.")]];
steps4.forEach((st, i) => {
  const y = 2.15 + i * 0.71;
  s.addShape(pres.shapes.OVAL, { x: 7.75, y: y + 0.05, w: 0.36, h: 0.36, fill: { color: C.teal }, line: { color: C.teal } });
  txt(s, String(i + 1), { x: 7.75, y: y + 0.05, w: 0.36, h: 0.36, fontSize: 12, bold: true, color: C.white, align: "center", valign: "middle", margin: 0 });
  txt(s, st, { x: 8.2, y, w: 4.63, h: 0.7, fontSize: 10.5 });
});
card(s, 7.75, 5.02, 5.08, 1.12, "Known positive, not a discovery", "EMA's PRAC called NAION a very rare side effect of semaglutide (6 Jun 2025); WHO alert (27 Jun 2025). Our 3 US labels do not mention it. Finding it from FAERS alone checks that the monitor works.", "green", { t: { fontSize: 10 } });
card(s, 7.75, 6.2, 5.08, 0.72, "Not proof of harm; the 394 reports do not open from her screen yet.", "Rehearsal check: “optic” must not land on the retinopathy warning; else search “ischemic optic”.", "amber", { t: { fontSize: 9.5 } });
txt(s, "PRR (proportional reporting ratio): how many times more common this reaction is among the drug's reports than among other drugs' reports — a reporting pattern, not risk. Evans rule: at least 3 reports, PRR ≥ 2, χ² ≥ 4.",
  { x: 1.75, y: 2.2 + h, w: 5.75, h: 0.62, fontSize: 10, color: C.gray });
evid(s, "OBSERVED", 0.5, 2.25 + h, 1.15);
source(s, "numbers.json signals.naion, app; screens/app-1c-labels-searched-naion.jpg; known positive: EMA/PRAC 6 Jun 2025; WHO 27 Jun 2025 (DECISIONS learning 2026-11-05).");

// 5 LIVE: RECALLS + WHAT CHANGED                                                           6:00–7:30
s = content("Recalls, and what changed since my last review", "As the safety officer (live)", "The application", "6:00–7:30 · app pages 2–3");
lead(s, "A recall says when it matches none of the FDA-listed products we track. “What changed” starts from the date of my last review.");
live(s, "Page 2 → newest row → openFDA record tab → Classification (Class I first). Page 3 → Start date = my last review.");
h = img(s, SCR("app-2-recalls.jpg"), 0.875, 2.1, 5.3, 1425, 840);
img(s, SCR("app-3b-what-changed-past-month.jpg"), 7.155, 2.1, 5.3, 1425, 840);
const yb5 = 2.1 + h + 0.1;
card(s, 0.5, yb5, 6.05, 6.9 - yb5, `Question 2 · ${fmt(RC.active)} active (Ongoing) of ${fmt(RC.total)} recalls`,
  `Newest: ${RC.newest} (${RC.newest_reported}), a compounded tirzepatide vial. It matches none of the ${PRODUCTS_TRACKED} FDA-listed products we track for our ${SC.drugs_formulary} drugs (we have no purchasing or inventory data). The FDA's own record opens in a second tab. Class I first: click Classification (count = rehearsal check, not measured).`, "teal", { t: { fontSize: 10.5 } });
card(s, 6.78, yb5, 6.05, 6.9 - yb5, `Question 3 · ${fmt(CH.total)} dated change events`,
  `${fmt(CH.recall_reported)} recalls reported, ${fmt(CH.recall_terminated)} terminated, ${fmt(CH.label_version_effective)} label versions effective (the ${fmt(CH.label_version_effective)} of ${fmt(N.labels.total)} label versions that carry an effective date), dated by the source; “past month” = the brief's ${CH.last_30_days}. A label row says a new version took effect, not what changed in it. Signals change only with each FAERS quarter (~${MO.faers_age_days} days behind).`, "teal", { t: { fontSize: 10.5 } });
evid(s, "OBSERVED", 5.3, yb5 + 0.06, 1.15);
evid(s, "OBSERVED", 11.58, yb5 + 0.06, 1.15);
source(s, "numbers.json recalls, changes, monitoring; 658 products: foundry/ontology/README.md (MSSM Product); screens/app-2-recalls.jpg, app-3b-…jpg; D045 (proposed).");

// 6 ARCHITECTURE                                                                           7:30–9:30
pres.addSection({ title: "Under the hood" });
s = content("Architecture: drug identity resolved once, reused everywhere", "Under the hood", "Architecture", "7:30–9:30 · diagram 38 + Lineage");
lead(s, "Four public sources → raw → clean (identity resolved once) → curated → Ontology → Workshop app, with write-back.");
h = img(s, DIA("38-handin-architecture-onepage-v1.png"), 0.5, 1.62, 5.6, 2220, 2034);
const layers = [["Raw", "Source replies kept as received: FAERS quarter files, openFDA JSON, DailyMed XML, RxNorm."],
  ["Clean", "clean_drug_identity maps every FAERS drug name to an RxNorm ingredient (RxCUI), then product (application number) and package (NDC). Done once; everyone joins on it (D020; D027 proposed)."],
  ["Curated", "Statistics, signals, change events, monitoring: the tables the app needs."],
  ["Ontology", "Business objects on top of curated tables: Drug, Label, Recall, Signal …"],
  ["Workshop", "The app; its button writes a decision back through an Action."]];
let yy = 1.62;
layers.forEach(([hh, b], i) => {
  const hgt = i === 1 ? 0.92 : 0.56;
  card(s, 6.35, yy, 6.48, hgt, hh, b, i === 1 ? "green" : "white", { t: { fontSize: 10.5 } });
  yy += hgt + 0.08;
});
txt(s, "Foundry terms: a dataset is a versioned table; a transform is the Python code that builds one, kept in a Code Repository; Data Lineage draws which dataset feeds which. Dashed boxes = incremental or cached.", { x: 6.35, y: yy, w: 6.48, h: 0.62, fontSize: 10, color: C.gray });
status(s, "TESTED", 6.35, yy + 0.7, 2.6);
cue(s, "Data Lineage: raw → clean → curated graph", 6.35, yy + 1.1, 6.48);
link(s, "Fallback screenshot: B12 →", BK.B12, { x: 9.8, y: yy + 1.5, w: 3.0, h: 0.28 });
source(s, "diagrams/png/38-handin-architecture-onepage-v1.png (from the one-page architecture note); detailed flow: diagram 30 v2; foundry/README.md; DECISIONS D020, D027 (proposed), D036.");

// 7 ONTOLOGY                                                                               9:30–11:30
s = content("Ontology: objects, links, and one create-only Action", "Under the hood", "Architecture", "9:30–11:30 · diagram 31 + OE");
lead(s, "The app reads objects, not tables. Links let the officer walk from a signal to its counts, its drug, its products and its labels.");
h = img(s, DIA("31-handin-ontology-v1.png"), 0.5, 1.62, 8.0, 4752, 2688);
bullets(s, [
  [B("Object type: "), T("a business thing backed by one curated dataset (e.g. MSSM Signal).")],
  [B("Link type: "), T("a typed relation with cardinality, e.g. many signals : 1 drug.")],
  [B("Action: "), T("the only way to write. Create MSSM Triage Decision is create-only: past decisions are never edited.")],
  [B("Survives rebuilds: "), T(`decisions live in their own object, so rebuilding signals does not erase them (${APP.triage_decisions} saved so far).`)],
], { x: 8.75, y: 1.62, w: 4.08, h: 3.2, fontSize: 12 });
card(s, 8.75, 4.88, 4.08, 1.05, "Mistake, left for the owner", "A duplicate Signal → Drug link was added by mistake in step 11. Nothing uses it; it should be deleted.", "amber", { t: { fontSize: 10.5 } });
cue(s, "Ontology Manager → MSSM Signal; Object Explorer → NAION → Links", 0.5, 1.75 + h, 8.0);
status(s, "TESTED", 8.75, 6.05, 2.6);
source(s, "diagrams/png/31-handin-ontology-v1.png; foundry/ontology/README.md; DECISIONS D040, D042; numbers.json app.triage_decisions.");

// 8 SIGNAL PIPELINE                                                                        11:30–12:50
s = content("From one FAERS report to a ranked signal", "Under the hood", "Data judgment · AI reliability", "11:30–12:50 · diagram 32");
lead(s, "Clean the reports (A), count and test (B), check the label three ways (C), then sort the queue (D).");
h = img(s, DIA("32-handin-signal-pipeline-v2.png"), 0.665, 1.6, 12.0, 2352, 963);
txt(s, "A: D022 latest case version + deletes · D021 suspect roles · D020 exact ingredient · D023 v2 duplicates and mass reports.   B: 2×2 table → PRR + Evans (D006, proposed).   C: AI term with a quote (D041) → exact text (D037, proposed) → reviewed synonym (D043); same outcome in any order.   D: buckets (D016 v3) decide ranked / possibly in label / tagged / caution.",
  { x: 0.5, y: 1.66 + h, w: 12.33, h: 6.98 - (1.66 + h), fontSize: 10, color: C.ink });
source(s, "diagrams/png/32-handin-signal-pipeline-v2.png (NAION counts from the local run, equal to Foundry, A014); foundry/pipelines/*/README.md.");

// 9 QUEUE                                                                                  12:50–13:30
s = content(`${fmt(SG.ranked)} ranked signals is a review queue, not ${fmt(SG.ranked)} findings`, "Under the hood", "Data judgment", "12:50–13:30 · slide");
lead(s, `Label checks and buckets shrank the queue by ${queueCut}% without hiding anything: removed items stay visible with a reason.`);
txt(s, "From statistics to the ranked queue", { x: 0.5, y: 1.65, w: 6.0, h: 0.3, fontSize: 12, bold: true, color: C.navy });
s.addChart(pres.charts.BAR, [{ name: "count", labels: ["drug × reaction stats", "signals (Evans + not / possibly in label)", "ranked (clinical bucket)"], values: [SG.ae_stats, SG.total, SG.ranked] }],
  chartBase({ x: 0.5, y: 1.95, w: 6.0, h: 2.7, barDir: "bar", chartColors: [C.teal], catAxisOrientation: "maxMin", valAxisHidden: true, valGridLine: { style: "none" },
    dataLabelFormatCode: "#,##0", barGapWidthPct: 45 }));
txt(s, "Ranked queue after each label-check or bucket change", { x: 6.85, y: 1.65, w: 6.0, h: 0.3, fontSize: 12, bold: true, color: C.navy });
s.addChart(pres.charts.BAR, [{ name: "ranked", labels: ["step 9 (first full build)", "synonyms v1", "buckets D016 v3", "synonyms v2"], values: [rh.step9, rh.syn_v1, rh.d016_v3, rh.syn_v2] }],
  chartBase({ x: 6.85, y: 1.95, w: 5.98, h: 2.7, barDir: "col", chartColors: [C.navy], valAxisMinVal: 0, dataLabelFormatCode: "#,##0", barGapWidthPct: 55, valAxisHidden: true, valGridLine: { style: "none" } }));
evid(s, "OBSERVED", 0.5, 4.62, 1.15);
evid(s, "DERIVED", 1.75, 4.62, 1.15);
txt(s, "counts from Foundry; the % is computed from them", { x: 2.98, y: 4.6, w: 5.0, h: 0.3, fontSize: 10, color: C.gray, valign: "middle" });
card(s, 0.5, 5.02, 4.0, 1.78, "Every signal keeps a label status", `${fmt(SG.not_in_label)} not in label · ${fmt(SG.possibly_in_label)} possibly in label (kept, never ranked). ${SC.drugs_with_signals} of ${SC.drugs_formulary} drugs have signals (exenatide has no reference label).`, "teal", { t: { fontSize: 12 } });
card(s, 4.67, 5.02, 4.0, 1.78, `Synonym table ${SY.version}: ${fmt(SY.rows)} rows`, `${SY.high} high (same idea → in label) · ${SY.medium} medium (→ possibly) · ${SY.rejected} rejected, kept for audit. Drafted by Claude; a pharmacist has not reviewed it yet.`, "amber", { t: { fontSize: 12 } });
card(s, 8.84, 5.02, 3.99, 1.78, "Why not MedDRA groupings?", "MedDRA's term hierarchy needs a licence we do not have, so a hand-reviewed synonym table and keyword buckets stand in (D043, D016 v3).", "stone", { t: { fontSize: 12 } });
source(s, `numbers.json signals (ae_stats, total, ranked, ranked_history, not_in_label, possibly_in_label), synonyms; ${queueCut}% = (${rh.step9} − ${rh.syn_v2}) / ${rh.step9}.`);

// 10 AI RELIABILITY                                                                        13:30–14:45
pres.addSection({ title: "AI, monitoring, optimization" });
s = content("AI extraction: quotes are real; accuracy on a small key", "AI, monitoring, optimization", "AI reliability", "13:30–14:45 · eval + AI dataset");
lead(s, `Claude Sonnet 5.5 (via AIP) read ${AI.sections} label sections (${AI.pilot_labels} pilot labels), listing each side effect with an exact quote.`);
tile(s, 0.5, 1.7, 2.95, 1.55, `${AI.grounded} / ${AI.reactions}`, `quotes found word-for-word, all ${AI.sections} sections (no invented quotes)`, "green", "OBSERVED");
tile(s, 3.6, 1.7, 2.95, 1.55, `${recN} / ${recD}`, `answer-key items found (first prompt: ${p1N} of ${recD})`, "teal", "OBSERVED");
tile(s, 6.7, 1.7, 2.95, 1.55, `F1 ${AI.gold_f1}`, `only on ${recD} items (${AI.pilot_labels} oxycodone labels, short sections, Claude-written key); proposed target ${AI.d015_target_f1} (D015)`, "teal", "DERIVED");
tile(s, 9.8, 1.7, 3.03, 1.55, `${AI.model_calls_on_rebuild} calls`, `on rebuild: ${AI.from_cache_on_rebuild} / ${AI.sections} sections served from cache`, "violet", "OBSERVED");
card(s, 0.5, 3.38, 4.0, 2.3, "How we know", "", "white", { t: { fontSize: 11.5 } });
bullets(s, [
  [B("Grounding: "), T("code checks each quote is in that section's text. Catches invented text.")],
  [B("Answer key: "), T("frozen before the model ran. Catches wrong or missing items.")],
  [B("Cache key: "), T("label, version, section, text hash, prompt and model. Unchanged text never calls the model.")],
], { x: 0.58, y: 3.68, w: 3.85, h: 2.0, fontSize: 10.5 });
card(s, 4.67, 3.38, 4.0, 2.3, "What this does not show", "", "amber", { t: { fontSize: 11.5 } });
bullets(s, [
  T(`A small key (${recD} reactions, short sections only), written by Claude; no pharmacist has checked it.`),
  T("The long sections (Warnings and Precautions, Adverse Reactions) are not scored."),
  T("A real quote can still be the wrong item. Grounding is not correctness."),
], { x: 4.75, y: 3.68, w: 3.85, h: 2.0, fontSize: 10.5 });
card(s, 8.84, 3.38, 3.99, 2.3, "Where the AI meets the screen: not yet", "", "amber", { t: { fontSize: 11.5 } });
bullets(s, [
  T(`The AI read only the ${AI.pilot_labels} oxycodone pilot labels. For NAION the screen says “Labels also read by AI: 0”.`),
  T("It does not change the signal list today; text matching already finds its terms."),
  T("Why: we would not widen a model we cannot yet score independently (D041). Widening + a quote panel = D041 v2, your call."),
], { x: 8.92, y: 3.68, w: 3.85, h: 2.0, fontSize: 10.5 });
status(s, "TESTED", 0.5, 5.78, 2.7);
status(s, "PLANNED", 3.35, 5.78, 2.6);
txt(s, "planned = pharmacist-labelled key incl. long sections", { x: 6.05, y: 5.78, w: 5.0, h: 0.3, fontSize: 10.5, color: C.amberI, valign: "middle" });
cue(s, "Optional: ai_label_section_extractions in SQL (from_cache = true)", 0.5, 6.25, 6.6);
link(s, "Details: B5 →", BK.B5, { x: 10.8, y: 6.3, w: 2.0, h: 0.3 });
source(s, "numbers.json ai; eval/ai-eval-v1.md; DECISIONS D015 (target, proposed), D041; F1 computed from recall and precision.");

// 11 MONITORING                                                                            14:45–15:30
s = content(`Monitoring: ${MO.checks_per_build} checks per build caught two real shifts`, "AI, monitoring, optimization", "AI reliability · monitoring", "14:45–15:30 · monitoring data");
lead(s, "Each build appends one row per check: keys, row counts, freshness, AI grounding, cache hits, field fill rates. History is kept.");
h = img(s, ASSET("monitoring-checks-sql-crop.png"), 0.5, 1.7, 7.3, 855, 220);
txt(s, "monitoring_checks, latest run (Code Repository SQL panel): the warn row first, then AI checks, then key checks.", { x: 0.5, y: 1.75 + h, w: 7.3, h: 0.3, fontSize: 10, color: C.gray });
tile(s, 0.5, 4.25, 2.35, 1.4, String(MO.checks_per_build), "computed checks appended per build", "teal", null);
tile(s, 2.98, 4.25, 2.35, 1.4, String(MO.data_health_checks), "Foundry Data Health checks (alert the owner)", "teal", null);
tile(s, 5.46, 4.25, 2.34, 1.4, String(MO.runs), "monitoring runs so far", "teal", null);
card(s, 8.05, 1.7, 4.78, 1.75, `Warning 1 · reporter type blank ${pct(MO.reporter_type_blank_q1)} → ${pct(MO.reporter_type_blank_q2)}`,
  "Share of FAERS reports with no reporter type, 2026Q1 → Q2 (DQ38; likely FDA's switch to a new intake system). Lawyer / consumer tagging would break silently, so we show “unknown”.", "amber", { t: { fontSize: 11 } });
card(s, 8.05, 3.55, 4.78, 1.4, `Warning 2 · recalls ×${driftX}`,
  `${MO.recalls_last4w} recalls reported for our drugs in the last 4 weeks vs ${MO.recalls_prev4w} in the 4 before (D009 window).`, "amber", { t: { fontSize: 11 } });
evid(s, "OBSERVED", 11.6, 1.75, 1.15);
card(s, 8.05, 5.05, 4.78, 1.15, "Honest limit", "Drift is a historical replay from source dates, not weeks of live builds. No schedules or health page yet.", "stone", { t: { fontSize: 11 } });
status(s, "TESTED", 0.5, 5.85, 2.7);
cue(s, "monitoring_checks; signals → Health tab", 3.4, 5.83, 4.4);
link(s, "Diagram: B9 →", BK.B9, { x: 10.8, y: 6.3, w: 2.0, h: 0.3 });
source(s, `numbers.json monitoring; screens/hood-monitoring-checks-sql.jpg (cropped); DECISIONS D046 (proposed), D009, D025 (proposed); DQ38. ×${driftX} = ${MO.recalls_last4w} / ${MO.recalls_prev4w}.`);

// 12 OPTIMIZATION                                                                          15:30–16:45
s = content("Optimization log: four measured tries, two helped, two did not", "AI, monitoring, optimization", "Optimization", "15:30–16:45 · optimization log");
lead(s, "Rule: measured, not asserted. Every entry has a before and an after number, and failed tries stay in the log.");
const yes = { text: "Yes", options: { bold: true, color: C.greenE } }, no = { text: "No", options: { bold: true, color: C.red } };
s.addTable([
  [hdr("#"), hdr("Pipeline · change"), hdr("Before"), hdr("After"), hdr("Helped?")],
  ["O1", "AI extraction · cache by content hash", `${OP.O1.before_calls} model calls, ${fmt(OP.O1.before_tokens)} tokens`, `${OP.O1.after_calls} calls, ${OP.O1.after_tokens} tokens`, yes],
  ["O2", "FAERS clean · incremental by quarter", `full rebuild ${OP.O2.full_rebuild_s} s`, `${OP.O2.incremental_add_q2_s} s (×${o2slower} slower)`, no],
  ["O3", "DailyMed pull · reuse unchanged XML", `${mmss(OP.O3.before_s)}, ${fmt(OP.O3.before_downloads)} XML downloads`, `${mmss(OP.O3.after_s)}, ${OP.O3.after_downloads} XML downloads (−${o3cut}% time; index still pulled)`, yes],
  ["O3a", "FAERS clean · parse fewer columns", `${OP.O3a.local_run_before_s} s (local)`, `${OP.O3a.local_run_after_s} s (local)`, no],
], Object.assign({ x: 0.5, y: 1.7, w: 7.6, colW: [0.55, 2.55, 1.8, 1.85, 0.85], fontSize: 11, rowH: 0.52 }, TB));
txt(s, "Build time, seconds (Foundry)", { x: 8.4, y: 1.65, w: 4.4, h: 0.3, fontSize: 12, bold: true, color: C.navy });
s.addChart(pres.charts.BAR, [
  { name: "before / full", labels: ["O2 FAERS", "O3 DailyMed"], values: [OP.O2.full_rebuild_s, OP.O3.before_s] },
  { name: "after / incremental", labels: ["O2 FAERS", "O3 DailyMed"], values: [OP.O2.incremental_add_q2_s, OP.O3.after_s] }],
  chartBase({ x: 8.4, y: 1.95, w: 4.43, h: 2.75, barDir: "col", chartColors: [C.rule, C.teal], showLegend: true, legendPos: "b", legendFontSize: 10,
    legendFontFace: FONT, valAxisHidden: true, valGridLine: { style: "none" }, barGapWidthPct: 50 }));
evid(s, "OBSERVED", 0.5, 4.55, 1.15);
evid(s, "DERIVED", 1.75, 4.55, 1.15);
txt(s, "×, % computed from the two numbers", { x: 2.98, y: 4.53, w: 3.5, h: 0.3, fontSize: 10, color: C.gray, valign: "middle" });
card(s, 0.5, 5.05, 2.95, 1.75, "Where it paid", "Skipping unchanged input: the AI cache (O1) and DailyMed XML reuse (O3, D047 proposed; fewer HTTP 429 risks).", "green", { t: { fontSize: 10.5 } });
card(s, 3.58, 5.05, 2.95, 1.75, "Where it did not", "O2: at 2 quarters the kept state costs more than it saves. O3a: parsing is not the bottleneck; reverted.", "amber", { t: { fontSize: 10.5 } });
card(s, 6.66, 5.05, 2.95, 1.75, "Partitioning: not done, on purpose", `Largest table ${fmt(F.case_reactions)} rows; clean builds ≤ ${OP.O2.full_rebuild_s} s. Revisit at 8+ quarters or a 5-minute build (D048, proposed).`, "stone", { t: { fontSize: 10.5 } });
card(s, 9.74, 5.05, 3.09, 1.75, "Caveats", "Each timing is one run. O3's baseline is an earlier build. O3a timed locally only.", "stone", { t: { fontSize: 10.5 } });
source(s, "numbers.json optimization; docs/08-optimization-log/optimization-log.md (O1–O3a); DECISIONS D044 (accepted), D047, D048 (proposed).");

// 13 INCREMENTAL FAERS                                                                     16:45–17:30
s = content("Incremental FAERS: proven correct, but slower at two quarters", "AI, monitoring, optimization", "Optimization", "16:45–17:30 · diagram 33");
lead(s, "It runs beside the full rebuild. Signals keep reading the full rebuild (D044, accepted) until it is faster.");
h = img(s, ASSET("33v2-faers-panel-crop.png"), 0.5, 1.65, 12.33, 4752, 1425);
const y13 = 1.65 + h + 0.15;
card(s, 0.5, y13, 4.0, 6.88 - y13, "Correct", `Same output as the full rebuild, row for row (EXCEPT ALL both ways = 0): ${fmt(F.cases_current)} cases, ${fmt(F.case_reactions)} reactions, ${fmt(F.drug_reaction_rows)} drug-reaction rows.`, "green", { t: { fontSize: 11.5 } });
card(s, 4.67, y13, 4.0, 6.88 - y13, "Slower", `Adding Q2: state (three state datasets + one quarter log) ${OP.O2.state_s} s + outputs ${OP.O2.outputs_s} s = ${OP.O2.incremental_add_q2_s} s, vs ${OP.O2.full_rebuild_s} s full (×${o2slower}).`, "amber", { t: { fontSize: 11.5 } });
card(s, 8.84, y13, 3.99, 6.88 - y13, "Next", "Re-measure at 4+ quarters, when re-reading history costs more. Try one build for state + outputs.", "stone", { t: { fontSize: 11.5 } });
source(s, "diagrams/png/33-handin-incremental-faers-v2.png (FAERS panel, cropped); A015; numbers.json faers, optimization.O2. Full diagram: B2.");

// 14 DATA JUDGMENT                                                                         17:30–19:00
pres.addSection({ title: "Judgment and next steps" });
s = content("Data judgment: what we found, and what we chose not to do", "Judgment and next steps", "Data judgment", "17:30–19:00 · slide (+ monitoring)");
lead(s, "The brief warned the data is messier than documented. Four messes we fixed or flagged, and noise we left, said plainly.");
s.addTable([
  [hdr("What we found"), hdr("Evidence"), hdr("What we did"), hdr("Ref")],
  ["FAERS sends new versions of old cases and deletes old cases in later quarters. Appending quarters creates phantom rows.",
    `Q2 replaced ${fmt(F.q2_cases_replaced)} Q1 cases and deleted ${fmt(F.q2_cases_deleted)}`, "Keep the latest version per case; apply deletes to the full history", "DQ36 · D022"],
  ["One patient filed by many companies; reports listing dozens of drugs inflate odd signals.", "Fold rule removes them from the main count (diagram 32)", "Person-key fold; reports with 30+ drugs leave the main count but stay as evidence; caution flag", "DQ37 · D023 v2"],
  ["Reporter type went blank for most reports.", `${pct(MO.reporter_type_blank_q1)} → ${pct(MO.reporter_type_blank_q2)} blank, Q1 → Q2`, "Show “unknown”, do not guess; checked on every build", "DQ38 · D046 (proposed)"],
  ["DailyMed answered HTTP 200 with the text “None” instead of a label.", `${OP.O3.after_downloads} of ${fmt(RAW.dailymed_labels)} labels`, "Keep the reply as received; mark has_xml = false; retry next build", "DQ42 · D047 (proposed)"],
  [{ text: "Noise we left: indication terms count as reactions; reports spike after news or lawsuits.", options: { fill: { color: C.amberF } } }, { text: "Liraglutide's rank 1 is “Diabetic metabolic decompensation” (page 1)", options: { fill: { color: C.amberF } } }, { text: "Not handled; the pharmacist's triage decides. NAION's reporter split not measured", options: { fill: { color: C.amberF } } }, { text: "DQ06 · DQ04", options: { fill: { color: C.amberF } } }],
], Object.assign({ x: 0.5, y: 1.65, w: 8.4, colW: [3.0, 2.05, 2.35, 1.0], fontSize: 11, rowH: [0.38, 1.0, 1.0, 0.72, 0.72, 0.95] }, TB));
card(s, 9.1, 1.65, 3.73, 2.4, "What we chose not to do", "", "stone", { t: { fontSize: 12 } });
bullets(s, [
  [B("No MedDRA licence: "), T("no term hierarchy; a reviewed synonym table and keyword buckets instead.")],
  [B("No patient data: "), T("public sources only.")],
  [B("Cut for depth: "), T("ClinicalTrials.gov, OnSIDES, daily FAERS, label-change backtest (D031).")],
], { x: 9.2, y: 2.0, w: 3.55, h: 2.0, fontSize: 11.5 });
evid(s, "OBSERVED", 9.1, 4.2, 1.15);
txt(s, "Evidence column = measured in Foundry. Full register: DQ01–DQ42.", { x: 9.1, y: 4.5, w: 3.73, h: 0.55, fontSize: 10, color: C.gray });
cue(s, "Optional: reporter-type check row", 9.1, 5.2, 3.73);
link(s, "Identity and FAERS rules: B3 →", BK.B3, { x: 9.8, y: 5.65, w: 3.0, h: 0.3 });
source(s, "data-issues-register.md (DQ04, DQ06, DQ36–38, DQ42); screens/app-1-not-in-label-naion.jpg; numbers.json; D022, D023 v2, D031, D043, D046, D047.");

// 15 ANOTHER MONTH                                                                         19:00–19:40
s = content("With another month: a pharmacist review loop first", "Judgment and next steps", "Communication", "19:00–19:40 · slide");
lead(s, "Only Claude has checked the synonym bands, answer key and ranked signals. A named pharmacist is the gap.");
const loop = [["Claude prepares", "an evidence packet: label quote, FAERS counts, PubMed, ClinicalTrials.gov, FDA safety notices, OnSIDES. Every claim linked."],
  ["Pharmacist decides", "confirm, re-band or reject, with a one-line reason and at least one evidence link."],
  ["Action records it", "create-only Review Decision: who, when, which evidence. Claude cannot submit."],
  ["Pipelines rebuild", `synonyms v3, answer key v3, triage labels; then report agreement and pharmacist-scored F1.`]];
loop.forEach(([hh, b], i) => {
  const x = 0.5 + i * 2.25;
  card(s, x, 1.75, 2.05, 1.95, hh, b, i === 1 ? "green" : "teal", { t: { fontSize: 11, valign: "top" } });
  if (i < 3) arrow(s, x + 2.06, 2.72, x + 2.24, 2.72, C.teal);
});
txt(s, `To review: ${fmt(SY.rows)} synonym rows, AI items from the long label sections, the top ranked signals per drug.`, { x: 0.5, y: 3.85, w: 8.9, h: 0.5, fontSize: 12, color: C.ink });
card(s, 0.5, 4.5, 8.85, 1.1, "Rules", "No patient data in the loop (connectors are not covered by Anthropic's BAA, the HIPAA contract). Hide Claude's draft on a random sample to measure automation bias.", "amber", { t: { fontSize: 11.5 } });
card(s, 9.6, 1.75, 3.23, 3.4, "Then", "", "white", { t: { fontSize: 12 } });
bullets(s, ["Schedules: builds run on a timer", "Live drift over 3–4 weeks (D009), not only replay", "Workshop health page", "Re-measure incremental FAERS at 4+ quarters", `Widen AI extraction past the ${AI.pilot_labels} pilot labels`],
  { x: 9.7, y: 2.1, w: 3.05, h: 3.0, fontSize: 11.5 });
status(s, "PLANNED", 9.6, 5.3, 3.23);
evid(s, "ASSUMED", 9.6, 5.75, 1.15);
txt(s, "Effort is an estimate (≈ 7–8 build days + 3–4 pharmacist days)", { x: 9.6, y: 6.03, w: 3.23, h: 0.55, fontSize: 10, color: C.gray });
link(s, "Sources and risks: B10 →", BK.B10, { x: 9.6, y: 6.55, w: 3.2, h: 0.3 });
source(s, "docs/09-roadmap/another-month-sources-and-pharmacist-review.md (§3 loop, §3.3 estimate, §4 risks); numbers.json synonyms.");

// 16 CLOSE                                                                                 19:40–20:00
s = content("What to take away", "Judgment and next steps", "Communication", "19:40–20:00 · then Q&A");
const take = [["Answers her questions", "Three questions on one screen; every flag traces to its source: labels searched and the FDA recall record in one click; FAERS case reports by query, not yet from her screen."],
  ["Built to be extended", "Identity resolved once. Incremental where it paid (AI cache, XML reuse); full rebuild where it did not, by measurement."],
  ["Honest about limits", "A review queue, not findings. A small, Claude-written answer key. Drift as a replay. A pharmacist is the next step."]];
take.forEach(([hh, b], i) => card(s, 0.5 + i * 4.15, 1.1, 3.98, 1.6, hh, b, "teal", { t: { fontSize: 12.5 } }));
box(s, 0.5, 2.8, 12.33, 0.38, C.greenF, C.greenE);
txt(s, [{ text: "New here? Start with R00 “Start here” ", options: { bold: true, color: C.greenI } }, { text: "(docs/11-handin/reports/pdf/R00-start-here.pdf): which report to read for which question.", options: { color: C.ink } }], { x: 0.62, y: 2.8, w: 12.1, h: 0.38, fontSize: 11.5, valign: "middle" });
card(s, 0.5, 3.3, 6.05, 3.5, "What did not work, or is not finished", "", "amber", { t: { fontSize: 12.5, valign: "top" } });
bullets(s, [
  `Incremental FAERS is slower at 2 quarters (${OP.O2.incremental_add_q2_s} s vs ${OP.O2.full_rebuild_s} s).`,
  "Parsing fewer columns (O3a) did not help; reverted.",
  "The AI does not change the signal list yet.",
  "Answer key written by Claude; pharmacist review pending.",
  "A duplicate Signal → Drug link is left for the owner to delete.",
  "D045 change feed, D046 monitoring, D047 XML reuse, D048 no partitioning: proposed.",
  "The AI has not read the hero drug's labels; no quote panel on screen yet.",
], { x: 0.62, y: 3.7, w: 5.85, h: 3.05, fontSize: 12 });
txt(s, "Questions: jump to a backup (type the slide number + Enter in slide show)", { x: 6.8, y: 3.3, w: 6.0, h: 0.35, fontSize: 12, bold: true, color: C.navy });
const qa = [["Architecture · how to extend", "B1"], ["Optimization · full diagram", "B2"], ["Data judgment · identity rules", "B3"], ["Application · trace + write-back", "B4"],
  ["AI reliability · eval details", "B5"], ["Communication · decisions", "B6"], ["Ripple map", "B7"], ["Change feed", "B8"], ["Monitoring", "B9"],
  ["Another month · sources", "B10"], ["Demo map", "B11"], ["Under-the-hood screenshots", "B12"]];
qa.forEach(([lab, b], i) => {
  const col = i % 2, row = Math.floor(i / 2);
  link(s, `${b} (${BK[b]}) · ${lab}`, BK[b], { x: 6.8 + col * 3.0, y: 3.72 + row * 0.5, w: 2.95, h: 0.4, align: "left", fontSize: 11 });
});
source(s, "numbers.json optimization.O2; DECISIONS D045–D048 (proposed); foundry/ontology/README.md (duplicate link); eval/ai-eval-v1.md.");

// =====================================================================================================
// 17 BACKUP DIVIDER
pres.addSection({ title: "Backup" });
s = pres.addSlide({ masterName: "SECTION", sectionTitle: "Backup" });
slideNo++;
txt(s, "Backup slides for questions", { x: 0.8, y: 1.2, w: 11.7, h: 0.9, fontSize: 32, bold: true, color: C.navy });
txt(s, "One per rubric row, then the ripple map, change feed, monitoring, another month, the demo map and screenshots. New to the project? Start with R00 “Start here” (docs/11-handin/reports/pdf/R00-start-here.pdf).", { x: 0.8, y: 2.05, w: 11.7, h: 0.6, fontSize: 14, color: C.ink });
qa.forEach(([lab, b], i) => {
  const col = i % 2, row = Math.floor(i / 2);
  link(s, `${b} · slide ${BK[b]} · ${lab}`, BK[b], { x: 0.8 + col * 5.8, y: 2.85 + row * 0.6, w: 5.6, h: 0.45, align: "left", fontSize: 15 });
});
txt(s, "17", { x: 12.25, y: 7.06, w: 0.6, h: 0.26, fontSize: 9.5, color: C.gray, align: "right", margin: 0 });
s.addNotes("Backup divider. Handbook: slide_explanations.md#backups.");

function backupTitle(id, title, rubric) { return content(`${id} · ${title}`, "Backup", rubric, "Q&A backup"); }

// B1 ARCHITECTURE — HOW TO EXTEND
s = backupTitle("B1", "How another engineer would extend it", "Architecture");
lead(s, "Each kind of change has one place to make it. The rest follows by rebuild (see the ripple map, B7).");
s.addTable([
  [hdr("I want to …"), hdr("Change this"), hdr("Where"), hdr("Decision")],
  ["add a drug to the formulary", "the RxCUI list in clean_drug_identity, and its copies in the 4 raw pull files (raw pulls take no dataset inputs)", "clean_drug_identity.py + raw_*.py", "D018, D020, D027 (proposed), D038"],
  ["add a public source", "a raw pull that stores the reply as received, then a clean transform", "pipelines_raw_ingest → pipelines_clean", "D038, D039 (contracts)"],
  ["say a FAERS term is in the label", "a synonym row with a band (high / medium / rejected)", "label_synonyms.py", "D043"],
  ["stop ranking a kind of reaction", "a bucket keyword (tag, don't remove)", "ontology_signals.py", "D016 v3"],
  ["change the statistical rule", "rule version in the signal key and evaluation id", "ontology_signals.py", "D006 (proposed), D042"],
  ["add a check", "one row per check per build", "monitoring.py", "D046 (proposed)"],
  ["show a new object in the app", "curated dataset → object type → Workshop widget", "Ontology Manager, Workshop", "D040"],
], Object.assign({ x: 0.5, y: 1.7, w: 12.33, colW: [2.9, 4.3, 3.13, 2.0], fontSize: 11.5, rowH: 0.5 }, TB));
txt(s, "Layers: Data/raw → Data/clean → Data/curated → Ontology → Workshop. Names, grains and keys follow the conventions in A007 / D036.",
  { x: 0.5, y: 6.05, w: 12.33, h: 0.5, fontSize: 12, color: C.ink });
source(s, "foundry/README.md; foundry/pipelines/*/README.md; foundry/ontology/README.md; docs/04-architecture/foundry-conventions; DECISIONS.");

// B2 OPTIMIZATION — FULL DIAGRAM 33
s = backupTitle("B2", "Incremental pieces in full (diagram 33 v2)", "Optimization");
lead(s, "Both incremental pieces, both measured in Foundry: FAERS (O2, correct but slower) and DailyMed XML reuse (O3, faster).");
h = img(s, DIA("33-handin-incremental-faers-v2.png"), 0.5, 1.6, 8.3, 4752, 2910);
card(s, 9.05, 1.6, 3.78, 1.9, "O3 in numbers", `XML downloads ${fmt(OP.O3.before_downloads)} → ${OP.O3.after_downloads} (${fmt(OP.O3.reused)} reused); ${mmss(OP.O3.before_s)} → ${mmss(OP.O3.after_s)}. D047 proposed.`, "green", { t: { fontSize: 11 } });
card(s, 9.05, 3.6, 3.78, 1.6, "O1 in tokens", `First run: ${fmt(AI.run1_tokens_prompt)} prompt + ${fmt(AI.run1_tokens_completion)} completion tokens. Rebuild with unchanged text: ${OP.O1.after_tokens}.`, "green", { t: { fontSize: 11 } });
card(s, 9.05, 5.3, 3.78, 1.5, "Freshness unchanged", "The DailyMed index is still pulled every build, so a new label version is fetched the same day.", "white", { t: { fontSize: 11 } });
source(s, "diagrams/png/33-handin-incremental-faers-v2.png; optimization-log.md O1, O3; numbers.json ai, optimization.");

// B3 DATA JUDGMENT — IDENTITY AND FAERS RULES
s = backupTitle("B3", "Drug identity and FAERS counting rules", "Data judgment");
lead(s, "These rules run before any counting. Each fixes a problem we measured on the real quarterly files.");
s.addTable([
  [hdr("Rule"), hdr("Problem it fixes"), hdr("What we do"), hdr("Status")],
  ["D020 identity", "Substring matching pulls in other drugs (“morphine” matches apomorphine) (DQ34)", "Split the product ingredient field, strip salts, exact RxNorm ingredient; never substring", "Accepted (G6)"],
  ["D021 suspect roles", "The secondary-suspect role often repeats the primary drug; primary-only drops real reports (DQ35)", "Suspect = primary + secondary + interacting; count each ingredient once per report", "Accepted (G6)"],
  ["D022 versions + deletes", "New case versions and deletes arrive in later quarters (DQ36)", `Keep the latest version; apply deletes to full history (Q2: ${fmt(F.q2_cases_replaced)} replaced, ${fmt(F.q2_cases_deleted)} deleted)`, "Accepted (G6)"],
  ["D023 v2 duplicates", "Same patient filed by many companies; mass polypharmacy re-filings (DQ37)", "Person-key fold; reports with 30+ drugs out of the main count, kept as evidence with a caution", "Accepted"],
  ["D037 + D043 label check", "“Is it in the label?” is a string question; synonyms differ", "AI term with a code-found quote, exact term or US spelling in 6 safety sections, reviewed synonym (code order)", "D037 proposed (built and running; owner acceptance pending); D043 accepted"],
], Object.assign({ x: 0.5, y: 1.7, w: 12.33, colW: [2.1, 4.1, 4.4, 1.73], fontSize: 11, rowH: 0.75 }, TB));
source(s, "DECISIONS D020–D023 (accepted for the pilot via D039 G6), D023 v2, D037, D043; data-issues-register DQ34–DQ37; numbers.json faers.");

// B4 APPLICATION — TRACE + WRITE-BACK
s = backupTitle("B4", "Trace and write-back: the trust rule in practice", "The application");
lead(s, "The triage form fills the signal and its evaluation id for her; she only chooses a decision and writes why.");
h = img(s, SCR("app-1b-triage-action-form.jpg"), 0.5, 1.65, 6.05, 1425, 840);
img(s, SCR("hood-object-explorer-naion-links.jpg"), 6.78, 1.65, 6.05, 1388, 868);
const y4 = 1.65 + h + 0.2;
card(s, 0.5, y4, 6.05, 6.88 - y4, "Write-back", `Create-only Action → MSSM Triage Decision. Reviewer and time come from the system. ${APP.triage_decisions} decisions saved; both survived a full rebuild at the baseline gate. App: ${APP.pages} pages, Workshop ${APP.workshop_version}.`, "green", { t: { fontSize: 11.5 } });
card(s, 6.78, y4, 6.05, 6.88 - y4, "Trace by hand", "At the baseline gate, 5 random ranked signals were re-counted from FAERS rows and their reference labels re-searched: all matched (baseline-gate.md). Object Explorer: Signal → AE Stat → Drug.", "teal", { t: { fontSize: 11.5 } });
source(s, "screens/app-1b-triage-action-form.jpg, hood-object-explorer-naion-links.jpg; docs/11-handin/baseline-gate.md; numbers.json app.");

// B5 AI RELIABILITY — DETAILS
s = backupTitle("B5", "AI evaluation details", "AI reliability");
lead(s, `The first prompt returned long phrases; prompt p2 asks for single terms. Answer-key items found: ${p1N} of ${recD} → ${recN} of ${recD}.`);
h = img(s, ASSET("ai-cache-sql-crop.png"), 0.5, 1.65, 8.0, 997, 190);
txt(s, "ai_label_section_extractions: one row per label section; status ok, every reaction grounded, from_cache = true on rebuild.", { x: 0.5, y: 1.7 + h, w: 8.0, h: 0.3, fontSize: 10, color: C.gray });
card(s, 8.75, 1.65, 4.08, 2.1, "Numbers", `Grounded ${AI.grounded}/${AI.reactions} (all ${AI.sections} sections). On the ${recD}-item key (${AI.pilot_labels} oxycodone labels, short sections, Claude-written): found ${recN} of ${recD}; precision ≥ ${AI.gold_precision_upper}; F1 ${AI.gold_f1} vs target ${AI.d015_target_f1}.`, "teal", { t: { fontSize: 11.5 } });
card(s, 0.5, 3.7, 6.05, 3.1, "If it got worse, how we would notice", "", "white", { t: { fontSize: 12, valign: "top" } });
bullets(s, [
  "Every build: grounded rate (fail below 0.95), section errors, cache hit rate in monitoring_checks.",
  "A new model, prompt or parser changes the cache key, so every section is re-extracted and re-scored against the key before it is accepted.",
  "With another month: a pharmacist-labelled sample of long sections, scored each release; drift = F1 drop > 0.05.",
], { x: 0.62, y: 4.05, w: 5.85, h: 2.7, fontSize: 11.5 });
card(s, 6.78, 3.9, 6.05, 2.9, "Limits, said plainly", "Small key, short sections only, written by Claude and frozen before the run, not yet checked by a pharmacist. The model: Claude Sonnet 5.5 via AIP. The AI does not change the signal list today.", "amber", { t: { fontSize: 11.5 } });
source(s, "eval/ai-eval-v1.md; numbers.json ai; screens/hood-ai-extractions-cache-sql.jpg (cropped); DECISIONS D041, D015 (proposed).");

// B6 COMMUNICATION — DECISIONS
s = backupTitle("B6", "Where the reasoning lives, and what is still proposed", "Communication");
lead(s, "Every choice where the brief was silent is written down. Changed decisions get a new version; nothing is edited in place.");
s.addTable([
  [hdr("Decision"), hdr("What"), hdr("Status")],
  ["D014 · D018", `Formulary: ${formulary}, as an explicit RxCUI list`, "Accepted"],
  ["D020–D024", "Identity, suspect roles, versions + deletes, duplicates, FAERS → label join", "Accepted (G6)"],
  ["D016 v3 · D043", "Buckets (MedDRA stand-in); label ↔ FAERS synonym table", "Accepted"],
  ["D005 · D041 · D044", "AI only on new label versions, cached; exact quotes; incremental FAERS beside the full rebuild", "Accepted"],
  ["D006 · D015 · D025–D029 · D037", `Evans rule; AI target F1 ≥ ${AI.d015_target_f1}; field fill-rate monitoring, bridge sources, two-level identity, since-last-review, FAERS quarterly; label-mention rule (most built and running; owner acceptance pending)`, "Proposed"],
  ["D045 – D048", "Change feed; monitoring; DailyMed XML reuse; no partitioning", "Proposed"],
], Object.assign({ x: 0.5, y: 1.7, w: 8.4, colW: [1.9, 4.6, 1.9], fontSize: 11.5, rowH: 0.55 }, TB));
status(s, "PROPOSED", 0.5, 6.2, 3.6);
card(s, 9.15, 1.7, 3.68, 4.25, "Read in this order", "R00 Start here → architecture note (one page) → COMPASS.md → DECISIONS.md (D001–D048, changes, learnings) → approaches A000–A017 (kept and dropped) → data issues DQ01–DQ42 → optimization log → eval/ai-eval-v1.md → roadmap.", "teal", { t: { fontSize: 11.5, valign: "top" } });
source(s, "docs/11-handin/architecture-note/; docs/06-decisions/DECISIONS.md; docs/05-approaches/INDEX.md; COMPASS.md.");

// B7 RIPPLE MAP
s = backupTitle("B7", "Ripple map: change this here, this changes there", "Architecture");
h = img(s, DIA("37-handin-ripple-v2.png"), 0.5, 1.1, 10.0, 4752, 2322);
card(s, 10.7, 1.1, 2.13, 2.9, "How to read it", "Nine changes, checked against the code. Existing triage decisions stay linked in every row (by signal key); some end up on an older evaluation id.", "teal", { t: { fontSize: 10.5 } });
card(s, 10.7, 4.1, 2.13, 1.6, "Known gap", "No stale flag: the screen does not say when a decision's evidence has moved.", "amber", { t: { fontSize: 10.5 } });
status(s, "PLANNED", 10.7, 5.8, 2.13);
source(s, "diagrams/png/37-handin-ripple-v2.png (checked against the code); numbers in the diagram from the build history (A014, D016 v3).");

// B8 CHANGE FEED
s = backupTitle("B8", "Change feed: two ways to know something changed", "The application");
h = img(s, DIA("34-handin-change-feed-v1.png"), 0.5, 1.1, 9.0, 4752, 2415);
card(s, 9.75, 1.1, 3.08, 2.4, "Dated by the source", `${fmt(CH.recall_reported)} recalls reported, ${fmt(CH.recall_terminated)} terminated, ${fmt(CH.label_version_effective)} label versions: real history on day one.`, "teal", { t: { fontSize: 11 } });
card(s, 9.75, 3.6, 3.08, 2.0, "Found by comparing builds", `Signals new / gone / changed. A no-change rebuild added ${CH.snapshot_diff_after_rebuild}.`, "teal", { t: { fontSize: 11 } });
status(s, "PROPOSED", 9.75, 5.75, 3.08);
txt(s, "D045, change feed", { x: 9.75, y: 6.1, w: 3.08, h: 0.3, fontSize: 10, color: C.gray });
source(s, "diagrams/png/34-handin-change-feed-v1.png; numbers.json changes; A016.");

// B9 MONITORING
s = backupTitle("B9", "Monitoring: what is watched, and who finds out", "AI reliability · monitoring");
h = img(s, DIA("35-handin-monitoring-v1.png"), 0.5, 1.1, 12.33, 4752, 1995);
txt(s, `${MO.checks_per_build} computed checks per build + drift replay + ${MO.data_health_checks} Foundry Data Health checks. Only Data Health alerts the owner today; the builder reads the check rows. Not built: health page, schedules, pharmacist-scored AI check.`,
  { x: 0.5, y: 1.2 + h, w: 12.33, h: 0.65, fontSize: 11.5 });
source(s, "diagrams/png/35-handin-monitoring-v1.png; numbers.json monitoring; A017; D046 (proposed).");

// B10 ANOTHER MONTH — SOURCES AND RISKS
s = backupTitle("B10", "Another month: sources researched for the review loop", "Communication");
lead(s, "Read-only web scan, 2026-11-05. Fit = how much it helps a pharmacist decide. Nothing here is in pilot scope.");
s.addTable([
  [hdr("Source"), hdr("Gives us"), hdr("Licence / cost"), hdr("Fit")],
  ["OnSIDES", "Label side effects, 4 regions, quarterly", "CC BY 4.0", "High"],
  ["FDA Drug Safety Communications + SrLC", "Has FDA warned? When did the label change?", "Free", "High"],
  ["Claude connectors (PubMed, ClinicalTrials.gov)", "Cited lookups for the evidence packet", "Free connectors; not under BAA", "High"],
  ["Palantir Ontology MCP", "Claude reads our signals (read-only tools)", "Part of Foundry", "Medium-high"],
  ["ClinicalTrials.gov", "Trial side effects vs placebo", "Free", "Medium"],
  ["FDA Orange Book", "Reference listed drug, interchangeable generics", "Free", "Medium"],
  ["MedDRA", "Term hierarchy and standard groupings", "Licence; $0 non-profit", "High (production)"],
  ["DrugBank · NIDA · “ClinHub”", "Commercial API · population misuse · sponsor trial hub", "Paid / restricted", "Low"],
], Object.assign({ x: 0.5, y: 1.65, w: 8.6, colW: [2.75, 3.0, 1.75, 1.1], fontSize: 10.5, rowH: 0.48 }, TB));
card(s, 9.35, 1.65, 3.48, 4.4, "Risks we would manage", "", "amber", { t: { fontSize: 12, valign: "top" } });
bullets(s, ["Patient data creeping in: written rule, no case narratives in packets.", "Automation bias: hide Claude's draft on a blind sample.", "Hallucinated evidence: link required and opened; quotes checked by code.", "Licences: MedDRA, DrugBank and SIDER limits.", "Audit: create-only Action, system-set reviewer and time."],
  { x: 9.45, y: 2.0, w: 3.3, h: 4.0, fontSize: 10.5 });
evid(s, "ASSUMED", 9.35, 6.2, 1.15);
txt(s, "fit ratings are our judgment", { x: 10.55, y: 6.18, w: 2.3, h: 0.3, fontSize: 10, color: C.gray, valign: "middle" });
source(s, "docs/09-roadmap/another-month-sources-and-pharmacist-review.md §2 (comparison), §4 (risks); licence facts as found on the linked pages.");

// B11 DEMO MAP
s = backupTitle("B11", "Demo map: the 23 stops", "Communication");
h = img(s, DIA("36-handin-demo-map-v2.png"), 0.5, 1.1, 9.4, 4752, 2826);
card(s, 10.1, 1.1, 2.73, 3.0, "How the talk uses it", "A0–A7: the officer's morning (slides 1–5, mostly live in the app). H1–H15: under the hood (slides 6–16, with live Foundry switches).", "teal", { t: { fontSize: 11 } });
source(s, "diagrams/png/36-handin-demo-map-v2.png; docs/11-handin/AGENT-BRIEF.md agenda; demo navigation guide.");

// B12 SCREENSHOTS
s = backupTitle("B12", "Under the hood: fallback screenshots", "Architecture");
const shots = [[ASSET("data-lineage-crop.png"), 912, 664, "Data Lineage (cropped): raw → clean → curated → ontology_signal_signals"],
  [SCR("hood-ontology-manager-signal.jpg"), 1388, 868, "Ontology Manager: MSSM Signal object type"],
  [SCR("hood-data-health-signals.jpg"), 1388, 868, "Data Health: build status + primary key checks, both passed"],
  [SCR("hood-code-repo-ontology-signals.jpg"), 1512, 806, "Code Repository pipelines_clean: ontology_signals.py"]];
shots.forEach(([f, pw, ph, cap], i) => {
  const col = i % 2, row = Math.floor(i / 2);
  const ih = 2.45, w = ih * pw / ph, x = 0.5 + col * 6.28 + (6.05 - w) / 2, y = 1.1 + row * 2.95;
  img(s, f, x, y, w, pw, ph);
  txt(s, cap, { x: 0.5 + col * 6.28, y: y + ih + 0.04, w: 6.05, h: 0.3, fontSize: 11, align: "center" });
});
source(s, "docs/11-handin/screens/hood-*.jpg (captured 2026-11-05); lineage cropped to the graph (deck/assets).");

pres.writeFile({ fileName: OUT }).then((f) => console.log("wrote", f, "slides:", slideNo));
