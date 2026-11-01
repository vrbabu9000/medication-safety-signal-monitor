"""Capture original public evidence for a blind 30-case candidate reference set.

Run explicitly; no schedules, credentials, Git mutations or report-level patient data.
Existing snapshots are retained. Only this task folder is written.
"""
from pathlib import Path
import concurrent.futures as cf
import datetime as dt
import hashlib
import html
import json
import re
import time
import urllib.parse as up
import urllib.request as ur
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SHARED = ROOT / 'shared'
EVIDENCE = SHARED / 'evidence'
EVIDENCE.mkdir(parents=True, exist_ok=True)
MANIFEST = SHARED / 'source-manifest.json'
OLD = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {'sources': []}
SOURCES = {r['source_id']: r for r in OLD['sources']}
UA = 'MedicationSafetyReferencePilot/1.0 (public-source verification; no patient records)'

def capture(source_id, url, kind='json'):
    if source_id in SOURCES and SOURCES[source_id].get('status') == 'captured':
        return SOURCES[source_id]
    extension = {'json': 'json', 'xml': 'xml', 'html': 'html', 'text': 'txt'}[kind]
    out = EVIDENCE / (source_id + '.' + extension)
    row = {'source_id': source_id, 'requested_url': url, 'method': 'GET', 'kind': kind}
    for attempt in range(3):
        try:
            req = ur.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
            with ur.urlopen(req, timeout=45) as response:
                body = response.read()
                row.update(final_url=response.url, http_status=response.status,
                    http_headers={k: response.headers.get(k) for k in
                        ['Content-Type', 'Last-Modified', 'ETag', 'Date'] if response.headers.get(k)})
            if kind == 'json':
                parsed = json.loads(body)
                row['source_metadata'] = parsed.get('meta', parsed.get('metadata', {}))
            elif kind == 'xml':
                t = ET.fromstring(body); ns = {'s': 'urn:hl7-org:v3'}
                row['source_metadata'] = {k: t.find('s:'+k, ns).attrib
                    for k in ['setId', 'versionNumber', 'effectiveTime'] if t.find('s:'+k, ns) is not None}
                row['source_metadata']['title'] = ''.join(t.find('s:title', ns).itertext()) if t.find('s:title', ns) is not None else None
            out.write_bytes(body)
            row.update(status='captured', evidence_file=str(out.relative_to(SHARED)),
                sha256=hashlib.sha256(body).hexdigest(), bytes=len(body),
                retrieved_at_utc=dt.datetime.now(dt.timezone.utc).isoformat())
            print(f'captured {source_id}: {len(body)} bytes', flush=True)
            return row
        except Exception as error:
            if hasattr(error, 'read'):
                error_body = error.read()
                failure_path = EVIDENCE / (source_id + '.http-error.txt')
                failure_path.write_bytes(error_body)
                row['error_evidence_file'] = str(failure_path.relative_to(SHARED))
            row.update(status='fetch_failed', error=f'{type(error).__name__}: {error}',
                retrieved_at_utc=dt.datetime.now(dt.timezone.utc).isoformat())
            if attempt < 2: time.sleep(1 + 2*attempt)
    print(f"failed {source_id}: {row['error']}", flush=True)
    return row

def save():
    MANIFEST.write_text(json.dumps({'capture_policy': 'Original public evidence; no expected answers. Source metadata is not retrieval time.',
        'sources': sorted(SOURCES.values(), key=lambda r:r['source_id'])}, indent=2)+'\n')

def batch(jobs):
    with cf.ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(capture,*job) for job in jobs]
        for future in cf.as_completed(futures):
            row=future.result(); SOURCES[row['source_id']]=row; save()

def api(base, params): return base+'?'+up.urlencode(params)

if __name__ == '__main__':
    jobs=[
        ('dm_oxy','https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/bfdfe235-d717-4855-a3c8-a13d26dadede.xml','xml'),
        ('dm_fentanyl_patch','https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/e15a7e9b-8025-49dd-9a6d-bafcccf1959f.xml','xml'),
        ('dm_tramadol','https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/83367367-5654-4078-831a-69ade48bc795.xml','xml'),
        ('rx_oxycodone','https://rxnav.nlm.nih.gov/REST/rxcui.json?name=oxycodone','json'),
        ('rx_morphine','https://rxnav.nlm.nih.gov/REST/rxcui.json?name=morphine','json'),
        ('rx_apomorphine','https://rxnav.nlm.nih.gov/REST/rxcui.json?name=apomorphine','json'),
        ('rx_percocet','https://rxnav.nlm.nih.gov/REST/rxcui.json?name=Percocet','json'),
        ('rx_version','https://rxnav.nlm.nih.gov/REST/version.json','json'),
        ('faers_oxy_counts',api('https://api.fda.gov/drug/event.json',{
            'search':'patient.drug.openfda.generic_name:"oxycodone" AND receivedate:[20260101 TO 20260630]',
            'count':'patient.reaction.reactionmeddrapt.exact','limit':1000}),'json'),
        ('recall_0338',api('https://api.fda.gov/drug/enforcement.json',{'search':'recall_number:"D-0338-2026"','limit':1}),'json'),
        ('drugsfda_oxy',api('https://api.fda.gov/drug/drugsfda.json',{'search':'application_number:"NDA022272"','limit':1}),'json'),
        ('ndc_oxy',api('https://api.fda.gov/drug/ndc.json',{'search':'product_ndc:"59011-410"','limit':5}),'json'),
        ('trial_oxy','https://clinicaltrials.gov/api/v2/studies/NCT01162304','json'),
        ('trial_version','https://clinicaltrials.gov/api/v2/version','json'),
        ('srlc_oxy_verified','https://www.accessdata.fda.gov/scripts/cder/safetylabelingchanges/index.cfm?event=searchdetail.page&DrugNameID=685','html'),
        ('faers_oxy_counts_alltime',api('https://api.fda.gov/drug/event.json',{
            'search':'patient.drug.openfda.generic_name:"oxycodone"',
            'count':'patient.reaction.reactionmeddrapt.exact','limit':1000}),'json'),
        ('faers_counts_unfiltered','https://api.fda.gov/drug/event.json?count=patient.reaction.reactionmeddrapt.exact&limit=1','json'),
        ('docs_faers','https://open.fda.gov/apis/drug/event/','html'),
        ('docs_recalls','https://open.fda.gov/apis/drug/enforcement/','html'),
        ('docs_ndc','https://www.fda.gov/drugs/drug-approvals-and-databases/national-drug-code-directory','html'),
        ('docs_drugsfda','https://www.fda.gov/drugs/drug-approvals-and-databases/drugsfda-data-files','html'),
        ('docs_rxnorm','https://www.nlm.nih.gov/research/umls/rxnorm/overview.html','html'),
        ('docs_rx_api','https://lhncbc.nlm.nih.gov/RxNav/APIs/','html'),
        ('docs_dailymed','https://dailymed.nlm.nih.gov/dailymed/spl-resources-all-drug-labels.cfm','html'),
        ('docs_trials','https://clinicaltrials.gov/data-api/api','html'),
        ('docs_srlc','https://www.fda.gov/drugs/drug-safety-and-availability/drug-safety-related-labeling-changes-srlc-database-overview-updates-safety-information-fda-approved','html'),
    ]
    batch(jobs)
    perc=SOURCES.get('rx_percocet',{})
    if perc.get('status')=='captured':
        data=json.loads((SHARED/perc['evidence_file']).read_text())
        ids=data.get('idGroup',{}).get('rxnormId',[])
        if ids:
            batch([('rx_percocet_ingredients',f'https://rxnav.nlm.nih.gov/REST/rxcui/{ids[0]}/related.json?tty=IN','json')])
    # Stable deterministic views support both independent annotators; these are not answers.
    views={}
    for key,row in sorted(SOURCES.items()):
        if row.get('status')!='captured': continue
        original=SHARED/row['evidence_file']
        if row['kind']=='xml':
            ns={'s':'urn:hl7-org:v3'}; tree=ET.parse(original); t=tree.getroot()
            sections=[]
            for index,section in enumerate(t.findall('.//s:section',ns)):
                title=section.find('s:title',ns); text=section.find('s:text',ns)
                if text is None: continue
                sections.append({'section_index':index,'heading':re.sub(r'\s+',' ',''.join(title.itertext())).strip() if title is not None else '',
                    'code':section.find('s:code',ns).attrib if section.find('s:code',ns) is not None else {},
                    'text':re.sub(r'\s+',' ',' '.join(text.itertext())).strip()})
            payload={'source_id':key,'original_sha256':row['sha256'],'source_metadata':row['source_metadata'],'sections':sections}
            target=EVIDENCE/(key+'.sections.json');target.write_text(json.dumps(payload,indent=2)+'\n')
            views[key]=str(target.relative_to(SHARED))
        elif row['kind']=='html':
            text=original.read_text(errors='replace')
            text=re.sub(r'<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>',' ',text,flags=re.S|re.I)
            text=re.sub(r'<[^>]+>',' ',text)
            text=re.sub(r'\s+',' ',html.unescape(text)).strip()
            target=EVIDENCE/(key+'.text.txt');target.write_text(text+'\n');views[key]=str(target.relative_to(SHARED))
    (SHARED/'derived-views.json').write_text(json.dumps({'description':'Deterministic parsing aids only; original bytes and manifest are authoritative. No expected answers.', 'views':views},indent=2)+'\n')
    print(json.dumps({'captured':sum(r.get('status')=='captured' for r in SOURCES.values()),
        'failed':[k for k,r in SOURCES.items() if r.get('status')!='captured']},indent=2),flush=True)
