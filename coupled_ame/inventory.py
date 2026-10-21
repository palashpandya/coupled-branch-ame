"""Check data integrity, catalogue and claim-map links; not external source theorems."""
from ._paths import ROOT, DATA, RESULTS
import hashlib
import json
import re

manifest=json.loads((ROOT/'docs/import-manifest.json').read_text())
for entry in manifest['files']:
    path=ROOT/entry['destination']
    assert path.is_file(), path
    assert hashlib.sha256(path.read_bytes()).hexdigest()==entry['packaged_sha256'], path
print('[PASS] imported inputs and ported sources match manifest:',len(manifest['files']))
checksums=json.loads((DATA/'SHA256SUMS.json').read_text())
for name,digest in checksums.items():
    assert hashlib.sha256((DATA/name).read_bytes()).hexdigest()==digest,name
print('[PASS] frozen data checksums:',len(checksums))
spec=json.loads((DATA/'o3_external_spec.json').read_text())['constructions']
cat=json.loads((DATA/'catalogue.json').read_text())
assert {c['key'] for c in cat['finite_examples']}==set(spec)
for c in cat['finite_examples']:
    s=spec[c['key']]
    assert all(c[k]==s[k] for k in ['N','K','p']) and c['d']==2*s['p']
assert [(x['N'],x['prime_threshold'],x['K']) for x in cat['infinite_families']]==[(13,17,16),(15,11,8),(17,67,64)]
print('[PASS] catalogue agrees with nine specifications and stated analytic thresholds')
readme=(ROOT/'README.md').read_text()
for name in re.findall(r'`([a-z_]+\.py)`',readme):
    assert (ROOT/'coupled_ame'/name).is_file(),name
assert not (ROOT/'manuscript').exists() and not (ROOT/'paper').exists()
assert not list(ROOT.rglob('*.tex'))
print('[PASS] README verifier references exist; no manuscript files')
print('[CITED] Source links in data/reference/README.md. No Lean build or external theorem verification performed.')
(RESULTS/'inventory.json').write_text(json.dumps({'status':'PASS','manifest_files':len(manifest['files']),'data_files':len(checksums),'finite_cells':len(spec),'cited_sources':'metadata only; not proof verification'},indent=2)+'\n')
