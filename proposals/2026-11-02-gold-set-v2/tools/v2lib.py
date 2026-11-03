"""Shared helpers for MSSM-30-v2 (cross-source drug traces).

Public sources only; aggregate FAERS counts only; no patient-level records are stored.
The openFDA key is read from OPENFDA_API_KEY when set and is never written to disk:
every URL that is saved or printed goes through redact().
"""
from pathlib import Path
import datetime as dt
import hashlib
import html
import http.cookiejar
import json
import os
import re
import time
import urllib.error
import urllib.parse as up
import urllib.request as ur

ROOT = Path(__file__).resolve().parents[1]
SHARED = ROOT / "shared"
EVIDENCE = SHARED / "evidence"
MANIFEST = SHARED / "source-manifest.json"
UA_TOOL = "MedicationSafetyReferencePilot/2.0 (public-source verification; no patient records)"
# SrLC rejects non-browser user agents with an abuse-detection redirect (see prototypes/explore/label_atlas.py).
UA_BROWSER = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

OPENFDA = "https://api.fda.gov/drug"
RXNAV = "https://rxnav.nlm.nih.gov/REST"
DAILYMED = "https://dailymed.nlm.nih.gov/dailymed/services/v2"
SRLC = "https://www.accessdata.fda.gov/scripts/cder/safetylabelingchanges/index.cfm"
CTGOV = "https://clinicaltrials.gov/api/v2"

# FAERS saved-query window: one closed calendar year so the scope is fixed and stated.
FAERS_WINDOW = ("20250101", "20251231")

def faers_substance_query(substance):
    """The saved FAERS query: reports listing this FAERS-coded active substance (any drug role) in the window.

    Combination products are coded as one string joined by backslashes (e.g. SACUBITRIL\\VALSARTAN);
    the backslash must be escaped inside the quoted openFDA term.
    """
    lo, hi = FAERS_WINDOW
    term = substance.replace("\\", "\\\\")
    return f'patient.drug.activesubstance.activesubstancename.exact:"{term}" AND receivedate:[{lo} TO {hi}]'


def faers_brand_query(brand):
    """Reports in the window where any listed drug's reporter-entered product name is exactly the brand."""
    lo, hi = FAERS_WINDOW
    return f'patient.drug.medicinalproduct.exact:"{brand.upper()}" AND receivedate:[{lo} TO {hi}]'


_jar = http.cookiejar.CookieJar()
_opener = ur.build_opener(ur.HTTPCookieProcessor(_jar))


def now_utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def api_key():
    return os.environ.get("OPENFDA_API_KEY") or None


def redact(url):
    return re.sub(r"(api_key=)[^&]+", r"\1REDACTED", url)


def url(base, params):
    return base + "?" + up.urlencode(params, safe=':"[]+')


def with_key(u):
    k = api_key()
    if k and u.startswith(OPENFDA):
        return u + ("&" if "?" in u else "?") + "api_key=" + up.quote(k)
    return u


class Fetch:
    """One HTTP response. ok=False keeps the error body so a failure is never mistaken for 'no data'."""
    def __init__(self, ok, status, body, headers, requested_url, error=None):
        self.ok, self.status, self.body, self.headers = ok, status, body, headers
        self.requested_url, self.error, self.retrieved_at_utc = requested_url, error, now_utc()

    def json(self):
        return json.loads(self.body)

    def text(self):
        return self.body.decode("utf-8", "replace")


def fetch(u, data=None, browser=False, cache_dir=None, pause=0.25, tries=3):
    """GET (or POST form when data is a dict). Optional disk cache for screening only.

    openFDA 404 'No matches found!' is a valid empty answer, returned with ok=True and status 404.
    """
    body_data = up.urlencode(data).encode() if data else None
    key = hashlib.sha256((redact(u) + "|" + (body_data or b"").decode()).encode()).hexdigest()
    if cache_dir:
        cp = Path(cache_dir) / key
        if cp.exists():
            c = json.loads(cp.read_text())
            return Fetch(c["ok"], c["status"], bytes.fromhex(c["body"]), c["headers"], c["url"], c["error"])
    last = None
    for attempt in range(tries):
        req = ur.Request(with_key(u), data=body_data,
                         headers={"User-Agent": UA_BROWSER if browser else UA_TOOL, "Accept": "*/*"})
        try:
            with _opener.open(req, timeout=90) as r:
                f = Fetch(True, r.status, r.read(),
                          {k: r.headers.get(k) for k in ("Content-Type", "Last-Modified", "ETag", "Date") if r.headers.get(k)},
                          redact(u))
            break
        except urllib.error.HTTPError as e:
            b = e.read()
            empty = e.code == 404 and u.startswith(OPENFDA) and b"No matches found" in b
            f = Fetch(empty, e.code, b, {}, redact(u), None if empty else f"HTTP {e.code}")
            if empty or e.code in (400, 403, 404):
                break
            last = f
        except Exception as e:  # network errors: retry
            f = last = Fetch(False, None, b"", {}, redact(u), f"{type(e).__name__}: {e}")
        time.sleep(2 * (attempt + 1))
    time.sleep(pause)
    if cache_dir:
        Path(cache_dir).mkdir(parents=True, exist_ok=True)
        (Path(cache_dir) / key).write_text(json.dumps({"ok": f.ok, "status": f.status, "body": f.body.hex(),
                                                       "headers": f.headers, "url": f.requested_url, "error": f.error}))
    return f


def srlc_session(cache_dir=None):
    fetch(SRLC, browser=True, pause=0.5)  # sets the session cookie; never cached


def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def srlc_search_rows(page_html):
    """Rows of an SrLC search result page: drug, ingredient, application number, DrugNameID."""
    rows = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", page_html, flags=re.S):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S)
        idm = re.search(r"DrugNameID=(\d+)", tr)
        if len(tds) >= 6 and idm:
            rows.append({"drug": strip_tags(tds[0]), "ingredient": strip_tags(tds[1]), "appl_no": strip_tags(tds[2]),
                         "appl_type": strip_tags(tds[3]), "supp_date": strip_tags(tds[4]),
                         "db_updated": strip_tags(tds[5]), "drug_name_id": idm.group(1)})
    return rows


def srlc_header(page_html):
    """The detail page's own identity line, e.g. 'OXYCONTIN (NDA-022272)'. Used by the identity guard."""
    m = re.search(r"([A-Z0-9][A-Z0-9 \-/,.&]+?)\s*\((NDA|BLA)-(\d+)\)", strip_tags(page_html))
    return {"brand": m.group(1).strip(), "appl_type": m.group(2), "appl_no": m.group(3)} if m else None


def srlc_entries(page_html):
    """Dated entries on an SrLC detail page with per-section plain text and underlined (added/revised) text."""
    parts = re.split(r"<h3[^>]*accordion-header[^>]*>", page_html)[1:]
    out = []
    for p in parts:
        m = re.match(r"\s*(\d\d/\d\d/\d{4})\s*</a>\s*<small>\((\w+)-(\d+)\)</small>", p)
        if not m:
            continue
        secs = []
        for sm in re.finditer(r"<h4>(.*?)</h4>(.*?)(?=<h4>|$)", p, flags=re.S):
            body = sm.group(2)
            subs = []
            # Subsection headings appear as <strong>8.4 Title</strong> or <p><b>5.13 Title</b></p>; the title itself
            # may contain markup when the heading was revised (e.g. <b>5.3 <u>Genitourinary Infections, including</u> ...</b>).
            head = r"(?:<strong>|<p[^>]*>\s*<b>)\s*(\d+(?:\.\d+)+\s(?:(?!</strong>|</b>\s*</p>).)*?)\s*(?:</strong>|</b>\s*</p>)"
            for pm in re.finditer(head + r"(.*?)(?=" + head.replace("(\\d", "(?:\\d") + r"|$)", body, flags=re.S):
                subs.append({"subsection": strip_tags(pm.group(1)),
                             "underlined": [u for u in (strip_tags(x) for x in re.findall(r"<u>(.*?)</u>", pm.group(2), flags=re.S)) if u],
                             "text": strip_tags(pm.group(2))})
            secs.append({"section": strip_tags(sm.group(1)), "subsections": subs, "text": strip_tags(body)})
        out.append({"date": m.group(1), "supplement": f"{m.group(2)}-{int(m.group(3))}", "sections": secs})
    return out


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def sha256(b):
    return hashlib.sha256(b).hexdigest()
