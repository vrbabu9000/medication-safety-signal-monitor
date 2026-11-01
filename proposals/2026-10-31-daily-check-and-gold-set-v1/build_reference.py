"""Build a frozen question pack and Codex's independent candidate answers.

No network; uses only captured public sources in this task folder.
Claude must not inspect this script or codex/: both contain Codex annotations.
"""
from pathlib import Path
import collections
import datetime as dt
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parent
SHARED=ROOT/'shared'
OUT=ROOT/'codex'
OUT.mkdir(exist_ok=True)
manifest=json.loads((SHARED/'source-manifest.json').read_text())
sources={r['source_id']:r for r in manifest['sources']}
def load(key): return json.loads((SHARED/sources[key]['evidence_file']).read_text())
def jp(data,path):
    for part in path.strip('/').split('/') if path else []:
        part=part.replace('~1','/').replace('~0','~')
        data=data[int(part)] if isinstance(data,list) else data[part]
    return data
def section(key,prefix):
    data=json.loads((SHARED/'evidence'/f'{key}.sections.json').read_text())
    matches=[r for r in data['sections'] if r['heading'].startswith(prefix+' ')]
    assert len(matches)==1,(key,prefix,len(matches))
    return matches[0]

questions=[];answers=[]
def add(category,question,source_ids,answer,locators,evidence,rationale,uncertainty='',input_scope=None,answer_format=None):
    cid=f'G{len(questions)+1:02d}'
    question_row={'case_id':cid,'category':category,'question':question,'source_ids':source_ids,
        'evidence_locators':locators,'answer_format':answer_format or 'Use the natural JSON scalar/object required by the question.'}
    if input_scope: question_row['input_scope']=input_scope
    questions.append(question_row)
    rows=[sources[s] for s in source_ids]
    assert all(r['status']=='captured' for r in rows)
    answers.append(dict(question_row,answer=answer,answer_status='resolved',
        evidence=evidence,rationale=rationale,uncertainty=uncertainty,
        source_sha256={r['source_id']:r['sha256'] for r in rows},
        source_effective_or_updated_at={r['source_id']:r.get('source_metadata',{}) for r in rows},
        retrieved_at_utc={r['source_id']:r['retrieved_at_utc'] for r in rows},
        human_review_status='pending',annotator='codex',verification='source_anchored; not clinician_adjudicated'))

enum=['reaction_or_warning','underlying_condition_or_risk_factor','symptom_of_other_condition',
      'administration_instruction','contraindicated_population','exposure_factor','co_medication_risk_factor']
label_cases=[
('dm_oxy','5.2','respiratory depression','reaction_or_warning','respiratory depression',
 'The passage explicitly describes reported respiratory depression with opioid use.',''),
('dm_oxy','5.13','opioid-induced esophageal dysfunction','reaction_or_warning','opioid-induced esophageal dysfunction',
 'The selected passage explicitly describes reported OIED in people taking opioids.','This does not attribute every dysphagia report to OIED or prove causality.'),
('dm_oxy','5.12','esophageal cancer','underlying_condition_or_risk_factor','esophageal cancer',
 'The passage identifies underlying GI disorders that increase complication risk; it does not state oxycodone causes esophageal cancer.','Bounded passage classification only.'),
('dm_oxy','5.9','nausea','symptom_of_other_condition','Presentation of adrenal insufficiency',
 'In this passage nausea is a symptom/sign of adrenal insufficiency.','Nausea may be a listed adverse reaction elsewhere; this answer is not global label absence.'),
('dm_oxy','5.12','the direction not to pre-soak, lick or wet tablets','administration_instruction','Instruct patients not to pre-soak',
 'This is an administration instruction; it is not an adverse reaction term.',''),
('dm_oxy','5.7','opioid-induced hyperalgesia','reaction_or_warning','Opioid-Induced Hyperalgesia',
 'The passage describes paradoxically increased pain/sensitivity associated with opioid analgesics.','The passage distinguishes the condition from tolerance and other explanations.'),
('dm_fentanyl_patch','5.8','external heat exposure','exposure_factor','Exposure to heat',
 'Heat is an exposure factor that can increase absorption; overdose/death are the described harmful outcomes.','Do not extract heat exposure itself as an adverse reaction.'),
('dm_fentanyl_patch','5.2','respiratory depression','reaction_or_warning','respiratory depression',
 'The patch label explicitly describes serious, potentially fatal respiratory depression.','This is a transdermal formulation, not an injection label.'),
('dm_fentanyl_patch','4','patients who are not opioid-tolerant','contraindicated_population','patients who are not opioid-tolerant',
 'The contraindication identifies a patient population, not a newly reported adverse reaction.','Do not infer anything about an individual patient.'),
('dm_fentanyl_patch','5.11','the listed serotonergic drugs','co_medication_risk_factor','serotonergic drugs',
 'These are concomitant medicines associated with the warning; the warned reaction is serotonin syndrome.','A named co-medication must not be extracted as an adverse reaction.'),
('dm_tramadol','5.9','serotonin syndrome','reaction_or_warning','serotonin syndrome',
 'The passage describes reported serotonin syndrome with tramadol, particularly with concomitant serotonergic drugs.','Selected extended-release label only; preserve interaction context.'),
('dm_tramadol','5.10','seizures','reaction_or_warning','Seizures have been reported',
 'The passage explicitly describes reported seizures within the recommended dosage range and additional risk factors.','This is evidence of label mention, not an incidence estimate.'),
]
for key,prefix,term,answer,quote,rationale,uncertainty in label_cases:
    r=section(key,prefix)
    assert quote.lower() in r['text'].lower(),(key,quote)
    add('DailyMed',f'In the specified passage only, classify {term}.', [key],answer,
        {key:f"HL7 v3 XML //section whose title is {r['heading']!r}; direct section text; derived section_index={r['section_index']}"},
        {'supporting_quote':quote},rationale,uncertainty,
        input_scope={'section_index':r['section_index'],'heading':r['heading'],'target_phrase':term,
            'derived_view':f'evidence/{key}.sections.json','allowed_classes':enum},answer_format='One allowed_classes string; explain the context separately.')

rxoxy=load('rx_oxycodone');rxm=load('rx_morphine');rxa=load('rx_apomorphine')
add('RxNorm','What ingredient RxCUI does the captured exact-name request for oxycodone return?', ['rx_oxycodone'],jp(rxoxy,'/idGroup/rxnormId/0'),
    {'rx_oxycodone':'/idGroup/rxnormId/0'}, {'source_value':jp(rxoxy,'/idGroup/rxnormId/0')},'Read the actual response; the exact query is recorded in the manifest.',answer_format='Identifier string.')
add('RxNorm','What ingredient RxCUI does the captured exact-name request for morphine return?', ['rx_morphine'],jp(rxm,'/idGroup/rxnormId/0'),
    {'rx_morphine':'/idGroup/rxnormId/0'},{'source_value':jp(rxm,'/idGroup/rxnormId/0')},'Read the actual response.',answer_format='Identifier string.')
add('RxNorm','Do the captured apomorphine and morphine requests return the same RxCUI?', ['rx_apomorphine','rx_morphine'],
    jp(rxa,'/idGroup/rxnormId/0')==jp(rxm,'/idGroup/rxnormId/0'),
    {'rx_apomorphine':'/idGroup/rxnormId/0','rx_morphine':'/idGroup/rxnormId/0'},
    {'apomorphine_rxcui':jp(rxa,'/idGroup/rxnormId/0'),'morphine_rxcui':jp(rxm,'/idGroup/rxnormId/0')},
    'Their identifiers differ; substring overlap is not ingredient equivalence.',answer_format='Boolean.')
ingredients=[]
for group in load('rx_percocet_ingredients')['relatedGroup']['conceptGroup']:
    if group.get('tty')=='IN': ingredients.extend({'rxcui':r['rxcui'],'name':r['name']} for r in group.get('conceptProperties',[]))
ingredients.sort(key=lambda r:r['name'])
add('RxNorm','Which ingredient names and RxCUIs are returned for the captured Percocet brand relationship lookup?',
    ['rx_percocet','rx_percocet_ingredients'],ingredients,
    {'rx_percocet':'/idGroup/rxnormId/0','rx_percocet_ingredients':'/relatedGroup/conceptGroup/*[tty=IN]/conceptProperties'},
    {'source_value':ingredients},'Keep both ingredients in a combination product; do not treat the brand as one ingredient.',answer_format='Array of {rxcui,name}, sorted by name.')

fa=load('faers_counts_unfiltered');top=fa['results'][0]
add('FAERS','What last_updated date does the captured unfiltered FAERS aggregate response report?', ['faers_counts_unfiltered'],fa['meta']['last_updated'],
    {'faers_counts_unfiltered':'/meta/last_updated'},{'source_value':fa['meta']['last_updated']},'This is response dataset metadata, not the retrieval time or date of a reaction.',answer_format='YYYY-MM-DD string.')
add('FAERS','What term and count are returned by the captured unfiltered, limit=1 reaction-count request?', ['faers_counts_unfiltered'],top,
    {'faers_counts_unfiltered':'/results/0'},{'source_value':top},'The query has no drug or date filter. Preserve that scope; this is not an oxycodone count.',answer_format='Object {term,count}.')
add('FAERS','Does this unfiltered aggregate establish an oxycodone-specific count for the returned term?', ['faers_counts_unfiltered'],False,
    {'faers_counts_unfiltered':'manifest.requested_url; /results/0'},{'scope':'Unfiltered; no search parameter'},
    'A global aggregate cannot be relabeled as a drug-specific result. The separate drug-filtered requests failed with API_KEY_MISSING.',answer_format='Boolean.')
add('FAERS','Does a reported adverse-event count alone establish causation or an incidence rate?', ['docs_faers'],False,
    {'docs_faers':'About FAERS data; Responsible use of the data; Disclaimer'},
    {'supporting_quote':'cannot be used to estimate the incidence of these events'},
    'Reports lack a usage denominator and do not establish that a drug caused the event.',answer_format='Boolean.')

rec=load('recall_0338')['results'][0]
add('FDA enforcement','What reason_for_recall is recorded for D-0338-2026?', ['recall_0338'],rec['reason_for_recall'],
    {'recall_0338':'/results/0/reason_for_recall'},{'source_value':rec['reason_for_recall']},'Read the specific captured recall record; preserve the reason.',answer_format='Exact source string.')
add('FDA enforcement','What status is reported in the captured record D-0338-2026?', ['recall_0338'],rec['status'],
    {'recall_0338':'/results/0/status'},{'source_value':rec['status']},'This is the status in this feed, not independently verified present-day lifecycle status.',answer_format='Exact source string.')
add('FDA enforcement','Can current active recall status be established from the captured reported status alone? Answer yes/no/unknown for current active status.',
    ['recall_0338','docs_recalls'],'unknown',{'recall_0338':'/results/0/status','docs_recalls':'Disclaimer; status not updated after classification'},
    {'reported_status':rec['status'],'supporting_quote':'FDA does not update the status of a recall after the recall has been classified'},
    'Current lifecycle status requires additional official verification; reported Ongoing is insufficient.',answer_format='One of yes, no, unknown for current active status, not a boolean about inferability.')
add('FDA enforcement','With no hospital inventory or lot records supplied, is hospital exposure to D-0338-2026 established? Answer yes/no/unknown.',
    ['recall_0338'],'unknown',{'recall_0338':'/results/0/product_description; /results/0/code_info'},
    {'lot_codes':rec['code_info']},'The source supplies affected product/lots, not hospital stock. Unknown is the resolved expected abstention.',answer_format='One of yes, no, unknown.')

dr=load('drugsfda_oxy')['results'][0]
add('Drugs@FDA','What sponsor_name does the captured Drugs@FDA record for NDA022272 give?', ['drugsfda_oxy'],dr['sponsor_name'],
    {'drugsfda_oxy':'/results/0/sponsor_name'}, {'source_value':dr['sponsor_name']},'Application sponsor is a source fact; do not assume every manufacturer/package is the same.',answer_format='Exact source string.')
prod=next(p for p in dr['products'] if p['product_number']=='001')
idx=dr['products'].index(prod)
val={k:prod[k] for k in ['brand_name','dosage_form','route','active_ingredients']}
add('Drugs@FDA','For NDA022272 product_number 001, return brand, dosage form, route and active ingredient/strength.', ['drugsfda_oxy'],val,
    {'drugsfda_oxy':f'/results/0/products/{idx}'},{'source_value':val},'Use the specified product number, not array order or another strength.',answer_format='Object with brand_name,dosage_form,route,active_ingredients exactly as recorded.')

nd=load('ndc_oxy')['results'][0]
pkg=next(p for p in nd['packaging'] if p['package_ndc']=='59011-410-10')
pidx=nd['packaging'].index(pkg)
add('NDC Directory','What package description is recorded for package_ndc 59011-410-10?', ['ndc_oxy'],pkg['description'],
    {'ndc_oxy':f'/results/0/packaging/{pidx}/description'},{'source_value':pkg['description']},'Product NDC and package NDC are different identifiers; preserve packaging.',answer_format='Exact source string.')
add('NDC Directory','Is carton NDC 68084-354-01 named in recall D-0338-2026 the same package as the selected OxyContin package 59011-410-10?',
    ['recall_0338','ndc_oxy'],False,{'recall_0338':'/results/0/product_description','ndc_oxy':f'/results/0/packaging/{pidx}/package_ndc'},
    {'recall_carton_ndc':'68084-354-01','selected_package_ndc':'59011-410-10'},
    'The package codes differ. An ingredient-level relationship is not this package match; this does not prove all OxyContin products are recall-free.',answer_format='Boolean.')

srlc=(SHARED/'evidence/srlc_oxy_verified.text.txt').read_text()
assert 'OXYCONTIN (NDA-022272)' in srlc and '12/22/2025 (SUPPL-52)' in srlc
latest=srlc.split('12/22/2025 (SUPPL-52)',1)[1].split('04/13/2023',1)[0]
assert '5.13 Risks of Gastrointestinal Complications' in latest and 'opioid-induced esophageal dysfunction' in latest
add('SrLC','Does the OXYCONTIN NDA-022272 entry dated 12/22/2025 (SUPPL-52), section 5.13, include opioid-induced esophageal dysfunction?',
    ['srlc_oxy_verified'],True,{'srlc_oxy_verified':'OXYCONTIN (NDA-022272) > 12/22/2025 (SUPPL-52) > 5.13 Risks of Gastrointestinal Complications'},
    {'supporting_quote':'Cases of opioid-induced esophageal dysfunction (OIED)'},
    'The specific regulatory change entry includes this wording; source date is not when every product label changed.',answer_format='Boolean.')

trial=load('trial_oxy');groups=trial['resultsSection']['adverseEventsModule']['eventGroups']
g=next(g for g in groups if g['id']=='EG000');gidx=groups.index(g)
tv={'group_id':g['id'],'group_title':g['title'],'seriousNumAffected':g['seriousNumAffected'],'seriousNumAtRisk':g['seriousNumAtRisk']}
add('ClinicalTrials.gov','For NCT01162304 adverse-event group EG000, what serious-adverse-event affected and at-risk counts are reported? Preserve the group title.',
    ['trial_oxy'],tv,{'trial_oxy':f'/resultsSection/adverseEventsModule/eventGroups/{gidx}'},
    {'source_value':tv,'study_status':trial['protocolSection']['statusModule']['overallStatus']},
    'These are trial-summary counts for the specified arm; the captured study is terminated. Zero reported events does not establish general safety.',answer_format='Object with group_id,group_title,seriousNumAffected,seriousNumAtRisk.')

assert len(questions)==30 and len(answers)==30
assert {q['case_id'] for q in questions}=={f'G{i:02d}' for i in range(1,31)}
counts=dict(collections.Counter(q['category'] for q in questions))
case_doc={'dataset_id':'MSSM-30-v1','purpose':'Candidate system reference set, not a clinician-approved gold standard.',
    'independence':'Shared evidence/cases; answers produced independently. Do not inspect codex/ or this build script before freezing Claude answers.',
    'selection_limits':'Purposive sample: 12 context cases from three opioid product labels, plus source/identity/abstention checks. Not representative of clinical safety or full-label recall.',
    'case_counts':counts,'cases':questions}
(SHARED/'cases.json').write_text(json.dumps(case_doc,indent=2)+'\n')
(OUT/'answers.jsonl').write_text(''.join(json.dumps(a,ensure_ascii=False)+'\n' for a in answers))

# Validate provenance, original hashes and literal evidence anchors. This is a source check,
# not an independent human review of Codex's interpretation.
verified=[]
for key,row in sources.items():
    if row.get('status')!='captured':continue
    actual=hashlib.sha256((SHARED/row['evidence_file']).read_bytes()).hexdigest()
    assert actual==row['sha256'],key
    verified.append(key)
for q,a in zip(questions,answers):
    assert q['case_id']==a['case_id'] and a['source_ids']
    if q['category']=='DailyMed':
        v=json.loads((SHARED/q['input_scope']['derived_view']).read_text())
        sec=next(s for s in v['sections'] if s['section_index']==q['input_scope']['section_index'])
        assert a['evidence']['supporting_quote'].lower() in sec['text'].lower()

validation={'dataset_id':'MSSM-30-v1','annotator':'codex','cases':30,'unique_case_ids':30,'category_counts':counts,
    'resolved_cases':30,'unresolved_cases':0,'intentional_unknown_cases':[a['case_id'] for a in answers if a['answer']=='unknown'],
    'source_hashes_verified':len(verified),'label_quote_anchors_verified':12,
    'source_family_count':8,'live_drug_filtered_faers_available':False,
    'source_failures':[{k:r.get(k) for k in ['source_id','requested_url','status','error','error_evidence_file']} for r in sources.values() if r.get('status')!='captured'],
    'all_human_reviews':'pending','interpretation_review':'Codex source review only; no independent human/clinical adjudication',
    'claude_answers_seen':False,'clinical_accuracy_claim':None,'full_label_recall_claim':None}
(OUT/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')

lines=['# Codex candidate answers — 30 cases','',
    '**Status:** source-anchored candidate reference set. Every human review is pending. No Claude answers were read.',
    '', '**Coverage:** eight source families; 12 bounded interpretation cases from three opioid labels. Remaining cases test data facts and justified abstention. Do not combine these into a clinical AI accuracy score.',
    '', '**FAERS limitation:** drug-filtered queries returned HTTP 403/API_KEY_MISSING. G17–G19 use a successful unfiltered aggregate, never an oxycodone-specific count. G20 tests documented interpretation. Failure responses are preserved.',
    '', '| ID | Source | Question / target | Candidate answer | Evidence |','|---|---|---|---|---|']
for a in answers:
    ans=json.dumps(a['answer'],ensure_ascii=False)
    ev=json.dumps(a['evidence'],ensure_ascii=False)
    def esc(s):return s.replace('|','\\|').replace('\n',' ')
    lines.append(f"| {a['case_id']} | {a['category']} | {esc(a['question'])} | {esc(ans)} | {esc(ev)} |")
lines+=['','## Human adjudication checklist','',
    'Check the original source, label/product/version, bounded passage context, query or trial arm, and the exact answer. Mark approve/correct/uncertain. Keep uncertainty; do not force agreement.',
    '', 'A correct unknown is not missing work. Source-dependent counts may change live, so score the frozen evidence first and record source drift separately.',
    '', '## What this set cannot establish','',
    '- Sensitivity/recall over all adverse reactions in full labels. Only selected terms/passages are tested.',
    '- Accuracy for every drug class, route, table format or clinical question.',
    '- Drug causation, adverse-event incidence, current active recall status or hospital lot exposure.',
    '- Foundry/AIP runtime, cost, optimization or production validation; no Foundry execution occurred here.',
    '', '## Freeze and comparison','',
    'Codex output is now fixed. Give Claude only CLAUDE-PROMPT.md and shared/. After Claude freezes its answers, compare IDs, answers, source locators and abstentions. Human review settles disagreements; agreement alone does not make gold.']
(OUT/'findings.md').write_text('\n'.join(lines)+'\n')
(OUT/'review-notes.md').write_text('''# Review notes

- G03: esophageal cancer is an underlying-condition example, not a claim that oxycodone causes cancer.
- G04: nausea is a symptom of adrenal insufficiency in the specified passage. Nausea can appear as an adverse reaction elsewhere; do not convert context exclusion into global absence.
- G07: heat is an exposure factor; overdose/death are outcomes.
- G10: a co-medication name is not a reaction.
- G19: unfiltered source counts are not drug-specific evidence.
- G23 and G24: unknown is the supported expected answer; current recall status and stock exposure are not established.
- G28: different package codes do not match; this is not a global claim of no recall.
- G29: regulatory change date and actual product label publication date are distinct.
- G30: retain the exact study arm and denominator; a terminated study with zero reported events does not prove general safety.

All clinical/context annotations require independent human review before use as a gold standard. No model disagreement analysis has been performed yet.
''')

# Do not change input after READY is written. Fingerprint all shared files except READY itself.
hashes={str(p.relative_to(SHARED)):hashlib.sha256(p.read_bytes()).hexdigest()
    for p in sorted(SHARED.rglob('*')) if p.is_file() and p.name!='READY.json'}
digest=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
ready={'dataset_id':'MSSM-30-v1','case_count':30,'source_family_count':8,
    'created_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'sha256_by_file':hashes,
    'pack_sha256':digest,'limitations':['Two drug-filtered FAERS requests failed; successful FAERS evidence is unfiltered.','Human clinical/context adjudication pending.'],
    'answer_files_included':False,'source_capture_does_not_imply_clinical_truth':True}
(SHARED/'READY.json').write_text(json.dumps(ready,indent=2)+'\n')
print(json.dumps(validation,indent=2))
