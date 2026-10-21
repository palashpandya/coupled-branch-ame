"""Independent exact all-cut check plus explicitly scoped numerical corroboration."""
from ._paths import DATA, RESULTS
from . import independent_core as v
import argparse
import itertools
import json

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--all-marginals', action='store_true', help='Slow: check every binary marginal for N<=15 instead of three deterministic cuts per cell.')
args = parser.parse_args()
spec = json.loads((DATA/'o3_external_spec.json').read_text())['constructions']
out = {}
for name, c in spec.items():
    n, p, k = c['N'], c['p'], c['N']//2
    row = dict(N=n, p=p, K=c['K'], **v.binary_exact(c))
    g = c['prime_parent_graph']
    assert len(g) == n+1 and all(len(r)==n+1 for r in g)
    assert all(g[i][j]==g[j][i] for i in range(n+1) for j in range(n+1))
    assert all(g[i][i]==0 for i in range(n+1))
    cuts = [a for a in itertools.combinations(range(n+1), (n+1)//2) if 0 in a]
    assert all(v._cut((g,a,p)) for a in cuts)
    assert row['binary_k_uniform'] and c['K']<=p
    row.update(exact_status='PASS', prime_cuts=len(cuts))
    if n <= 15:
        allcuts = list(itertools.combinations(range(n), k))
        chosen = allcuts if args.all_marginals else [allcuts[0], allcuts[len(allcuts)//2], allcuts[-1]]
        v._U.clear(); v._U[name] = v._u(c)
        error = max(v._marg((name,a)) for a in chosen)
        assert error < 1e-12
        row.update(numerical_marginals=len(chosen), numerical_max_error=error,
                   numerical_scope='all' if args.all_marginals else 'first, middle, last cuts in lexicographic order')
    else:
        row['numerical_scope'] = 'not computed; exact check covers all cuts'
    out[name]=row
    print(name, json.dumps(row), flush=True)
(RESULTS/'independent_o3.json').write_text(json.dumps(out,indent=2)+'\n')
print('[PASS] all eight exact certifications; numerical checks are corroboration only')
