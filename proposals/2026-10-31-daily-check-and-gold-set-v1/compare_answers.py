"""Compare independently frozen annotations. Agreement is not clinical accuracy."""
from pathlib import Path
import argparse
import datetime as dt
import hashlib
import json

ROOT=Path(__file__).resolve().parent

def read_jsonl(path):
    rows=[json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    by_id={}
    for row in rows:
        if row['case_id'] in by_id: raise ValueError(f'Duplicate case ID: {row["case_id"]}')
        by_id[row['case_id']]=row
    return by_id

def compare(codex_path,claude_path,output):
    shared=ROOT/'shared';ready=json.loads((shared/'READY.json').read_text())
    for rel,expected in ready['sha256_by_file'].items():
        if hashlib.sha256((shared/rel).read_bytes()).hexdigest()!=expected:
            raise ValueError(f'Shared evidence changed after freeze: {rel}')
    cases=json.loads((shared/'cases.json').read_text())['cases'];ids={r['case_id'] for r in cases}
    c=read_jsonl(codex_path);h=read_jsonl(claude_path)
    if set(c)!=ids or set(h)!=ids:
        raise ValueError(json.dumps({'codex_missing':sorted(ids-set(c)), 'codex_extra':sorted(set(c)-ids),
            'claude_missing':sorted(ids-set(h)), 'claude_extra':sorted(set(h)-ids)}))
    output.mkdir(parents=True,exist_ok=False)
    rows=[]
    for case in cases:
        cid=case['case_id'];a,b=c[cid],h[cid]
        same=a.get('answer')==b.get('answer') and a.get('answer_status')==b.get('answer_status')
        rows.append({'case_id':cid,'category':case['category'],'codex_answer':a.get('answer'),
            'claude_answer':b.get('answer'),'exact_answer_agreement':same,
            'codex_answer_status':a.get('answer_status'),'claude_answer_status':b.get('answer_status'),
            'codex_source_ids':a.get('source_ids'),'claude_source_ids':b.get('source_ids'),
            'codex_evidence_locators':a.get('evidence_locators'),'claude_evidence_locators':b.get('evidence_locators'),
            'human_verdict':'pending','human_note':''})
    summary={'created_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'shared_pack_sha256':ready['pack_sha256'],
        'codex_file_sha256':hashlib.sha256(codex_path.read_bytes()).hexdigest(),
        'claude_file_sha256':hashlib.sha256(claude_path.read_bytes()).hexdigest(),
        'case_count':30,'exact_agreements':sum(r['exact_answer_agreement'] for r in rows),
        'disagreements':[r['case_id'] for r in rows if not r['exact_answer_agreement']],
        'interpretation':'Agreement only; not gold-standard accuracy. Independently check evidence, even where answers agree.'}
    (output/'comparison.json').write_text(json.dumps({'summary':summary,'cases':rows},indent=2)+'\n')
    lines=['# Independent annotation comparison','',json.dumps(summary,indent=2),'',
        '| ID | Category | Codex | Claude | Exact agreement | Human verdict |',
        '|---|---|---|---|---|---|']
    for r in rows:
        def esc(x):return json.dumps(x,ensure_ascii=False).replace('|','\\|').replace('\n',' ')
        lines.append(f"| {r['case_id']} | {r['category']} | {esc(r['codex_answer'])} | {esc(r['claude_answer'])} | {r['exact_answer_agreement']} | pending |")
    (output/'comparison.md').write_text('\n'.join(lines)+'\n')
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--claude',type=Path,default=ROOT/'claude/answers.jsonl')
    p.add_argument('--codex',type=Path,default=ROOT/'codex/answers.jsonl')
    p.add_argument('--output',type=Path,default=ROOT/'comparison')
    args=p.parse_args()
    if not args.claude.exists():p.error('Claude answers do not exist yet. Run the Claude prompt independently first; no comparison has been performed.')
    print(json.dumps(compare(args.codex,args.claude,args.output),indent=2))
