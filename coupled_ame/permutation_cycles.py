"""R02 cycle check, reconstructed directly from the stored permutations."""
from ._paths import DATA, RESULTS
import json
spec=json.loads((DATA/'sym1_external_spec.json').read_text())
expected={'13_34':[1,4,4,4], '13_38':[1,6,6], '13_46':[1]+[2]*6,
          '15_34':[1]+[2]*7, '15_38':[3]*5, '15_46':[1]+[2]*7}
out={}
for key, lengths in expected.items():
    perm=spec['constructions'][key]['symmetry_generators'][0]['perm']
    assert sorted(perm)==list(range(len(perm)))
    remaining=set(range(len(perm))); cycles=[]
    while remaining:
        start=min(remaining); x=start; cycle=[]
        while x in remaining:
            remaining.remove(x); cycle.append(x); x=perm[x]
        assert x==start
        cycles.append(cycle)
    assert sorted(map(len,cycles))==lengths
    out[key]=dict(cycles=cycles,lengths=lengths)
    print('[PASS]',key,lengths)
(RESULTS/'permutation_cycles.json').write_text(json.dumps(out,indent=2)+'\n')
