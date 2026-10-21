"""Exact support/intensity verifier and algebraic export; produces no graphics.
Frozen clone-relative input. Integer polynomial arithmetic only.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import hashlib
import json
import math
from ._paths import DATA, RESULTS

source=DATA/'o3_external_spec.json'; output=RESULTS/'support.json'
spec=json.loads(source.read_text())['constructions']; results={}
for key,c in spec.items():
    n,k,p=c['N'],c['K'],c['p'];gens=c['binary_label_generators'];m=len(gens)
    assert p>=2 and k==2**m and k<p and all(p%d for d in range(2,math.isqrt(p)+1))
    words={}
    for coef in range(k):
        w=0
        for j,g in enumerate(gens):
            if coef>>j&1:w^=g
        assert w not in words
        words[w]=coef
    labels=c['branch_labels']; cs=c['prime_branch_labels']
    assert len(labels)==len(cs)==k and set(labels)==set(words)
    assert len(set(cs))==k and all(0<=a<p for a in cs)
    assert all(0<=g<2**n for g in gens)
    h=c['prime_parent_graph'][0][1:]
    assert len(h)==n and any(x%p for x in h)
    # Explicit fibre counts for b; prime fibre count follows from nonzero h.
    fibres=Counter(sum(((b&g).bit_count()%2)<<j for j,g in enumerate(gens)) for b in range(2**n))
    assert fibres==dict.fromkeys(range(k),2**(n-m))
    # A root of unity of prime order has minimal polynomial 1+...+x^(p-1).
    # A vector v (degree<=p-1) reduces by subtracting v[p-1] from v[0:p-1].
    zero=(0,)*(p-1); cells=[]; grid=[]; classes=Counter(); total=[0]*(p-1)
    columns=[[0]*(p-1) for _ in range(p)]
    for sigma in range(k):
        row_total=[0]*(p-1); row=[]
        signs=[(-1)**((words[l]&sigma).bit_count()%2) for l in labels]
        corr=[0]*p
        for i,a in enumerate(cs):
            for j,b in enumerate(cs):corr[(a-b)%p]+=signs[i]*signs[j]
        for t in range(p):
            coefficients=[0]*p
            for d,value in enumerate(corr):coefficients[(d*t)%p]+=value
            canonical=tuple(value-coefficients[-1] for value in coefficients[:-1])
            classes[canonical]+=1
            row.append(canonical)
            for i,value in enumerate(canonical):
                total[i]+=value; row_total[i]+=value; columns[t][i]+=value
            if canonical==zero:cells.append([sigma,t])
        grid.append(row)
        assert row_total==[p*k]+[0]*(p-2)
    assert all(col==[k*k]+[0]*(p-2) for col in columns)
    assert cells==[[sigma,0] for sigma in range(1,k)]
    assert total==[k*k*p]+[0]*(p-2)
    assert sum(classes.values())==k*p
    results[key]={'N':n,'p':p,'K':k,'m':m,'compressed_cells':k*p,
      'zero_cells':cells,'number_zero_cells':len(cells),'distinct_intensities_including_zero':len(classes),
      'distinct_positive_intensities':len(classes)-1,'support_fraction':str(Fraction(k*p-k+1,k*p)),
      'basis_states_per_cell':2**(n-m)*p**(n-1),
      'normalization_sum_squared_S':k*k*p,
      'syndrome_marginal':str(Fraction(1,k)),'prime_label_marginal':str(Fraction(1,p)),
      'intensity_class_multiplicities':sorted(classes.values()),
      'squared_S_canonical':grid if key=='15_26' else None}
    print(key, 'zeros',len(cells),'distinct incl zero',len(classes),'support',results[key]['support_fraction'])
output.write_text(json.dumps({'status':'PASS','method':'exact integer autocorrelation modulo Phi_p; no numerical zero tolerance',
                             'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'cells':results},indent=2)+'\n')
