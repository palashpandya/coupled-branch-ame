"""Certify the available AME(14,13) parent; does not assert AME(13,26)."""
from ._paths import DATA, RESULTS
from coupled_ame.rank_parent import verify_parent
import json
spec=json.loads((DATA/'o4_external_spec.json').read_text())['target_parent']
print('Parent keys:',list(spec))
graph=spec['graph'] if 'graph' in spec else spec['prime_parent_graph']
result=verify_parent(graph,13)
(RESULTS/'parent13.json').write_text(json.dumps(result,indent=2)+'\n')
print('[PASS] AME(14,13) parent',result)
print('No rank9..13 binary ingredient is supplied; AME(13,26) remains unresolved here.')
