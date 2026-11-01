"""Recreate the input-only local ZIP without exposing either annotator's answers."""
from pathlib import Path
import hashlib
import json
import zipfile

root=Path(__file__).resolve().parent
shared=root/'shared'
ready=json.loads((shared/'READY.json').read_text())
for relative,expected in ready['sha256_by_file'].items():
    assert hashlib.sha256((shared/relative).read_bytes()).hexdigest()==expected,relative
with zipfile.ZipFile(root/'claude-inputs.zip','w',zipfile.ZIP_DEFLATED) as archive:
    archive.write(root/'CLAUDE-PROMPT.md','CLAUDE-PROMPT.md')
    for p in sorted(shared.rglob('*')):
        if p.is_file(): archive.write(p,str(p.relative_to(root)))
with zipfile.ZipFile(root/'claude-inputs.zip') as archive:
    assert all(name=='CLAUDE-PROMPT.md' or name.startswith('shared/') for name in archive.namelist())
    assert not any('answers.jsonl' in name for name in archive.namelist())
print(root/'claude-inputs.zip')
