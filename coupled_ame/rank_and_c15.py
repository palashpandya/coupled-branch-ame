"""Short exact checks for the draft; source inputs are read only."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import hashlib
import json

from ._paths import DATA as SRC, RESULTS as OUT

def kr(n, j, i):
    return sum((-1)**t * 3**(j-t) * comb(i, t) * comb(n-i, j-t)
               for t in range(j+1) if t <= i and j-t <= n-i)

def system(r):
    n = 13
    variables = list(range(7, 14))
    bcoef = [[F(kr(n,j,i), 2**n) for i in variables] for j in range(n+1)]
    bconst = [F(kr(n,j,0), 2**n) for j in range(n+1)]
    rows, rhs = [], []
    for j in range(n+1):
        rows.append([F(i == j) - r*c for i,c in zip(variables,bcoef[j])])
        rhs.append(r*bconst[j] - F(j == 0))
        rows.append([-F((-1)**i*kr(n,j,i),2**n) for i in variables])
        rhs.append(bconst[j])
    rows.append(bcoef[0]); rhs.append(1-bconst[0])
    for s in range(n+1):
        rows.append([sum(comb(n-j,s-j)*bcoef[j][t] for j in range(s+1))
                     - r*(comb(n-i,s-i) if i <= s else 0)
                     for t,i in enumerate(variables)])
        rhs.append(r*comb(n,s)-sum(comb(n-j,s-j)*bconst[j] for j in range(s+1)))
        rows.append([F(comb(n-i,s-i)) if i <= s else F(0) for i in variables])
        rhs.append(F(comb(n,s)*(2**s-1)))
    return rows, rhs

def mm(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

records = []
path = SRC/'o4_lp_certificates.json'
for c in json.loads(path.read_text()):
    a,b = system(c['rank_upper_bound'])
    assert a == [[F(x) for x in row] for row in c['A']]
    assert b == list(map(F,c['b']))
    y = {int(i):F(v) for i,v in c['y'].items()}
    columns = [sum(v*a[i][j] for i,v in y.items()) for j in range(7)]
    value = sum(v*b[i] for i,v in y.items())
    assert all(v >= 0 for v in y.values()) and all(v >= 0 for v in columns)
    assert value < 0 and str(value) == c['contradiction']
    records.append(dict(rank_upper_bound=c['rank_upper_bound'],rows_reconstructed=len(a),
                        column_slacks=list(map(str,columns)),contradiction=str(value)))

spec = json.loads((SRC/'sym1_external_spec.json').read_text())['family_witness']
iso = spec['isometry']
assert iso['eta_exponent'] == 0 and iso['D'] == 1
assert all(v[1] == 0 for row in iso['Q'] for v in row)
q = [[v[0] for v in row] for row in iso['Q']]
ident = [[int(i==j) for j in range(8)] for i in range(8)]
assert mm(q,list(map(list,zip(*q)))) == ident
assert mm(mm(q,q),q) == ident
trace = sum(q[i][i] for i in range(8))
assert trace == 2
# A real order-three representation: multiplicities d0,d1,d1 satisfy
# d0+2*d1=8 and d0-d1=trace=2.
assert ((8+2*trace)//3, (8-trace)//3) == (4,2)

result = dict(status='PASS',arithmetic='exact rational/integer; no solver',
              general_rank_certificates=records,
              C15_binary=dict(order=3,trace=trace,multiplicities=[4,2,2],
                              signed_column_images=[next((i,q[i][j]) for i in range(8) if q[i][j]) for j in range(8)]),
              input_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                            [path,SRC/'sym1_external_spec.json']})
(OUT/'rank_and_c15.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
