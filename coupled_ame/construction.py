"""Build explicit graph-branch AME certificates, using only exact integers."""
import hashlib
import itertools as it
import json
import random
import time
from collections import Counter
from pathlib import Path
from .codes import *

HERE=Path(__file__).resolve().parents[1]/"results"
def save(name,x): (HERE/name).write_text(json.dumps(x,indent=2)+'\n')
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

def graph_form(S,n):
    mask=(1<<n)-1
    T=S[:]
    # Extend to a maximal isotropic space deterministically.
    while len(T)<n:
        central=nullspace([(g>>n)|((g&mask)<<n) for g in T],2*n)
        g=next(g for g in central if len(basis(T+[g]))>len(T))
        T.append(g)
    rng=random.Random(31019+n)
    for trial in range(100000):
        hs=rng.getrandbits(n)
        def swap(g):
            x=g&mask;z=g>>n;v=(x^z)&hs
            return (x^v)|((z^v)<<n)
        U=[swap(g) for g in T]
        if len(basis([g&mask for g in U]))==n:break
    else:raise RuntimeError('no graph chart')
    for j in range(n):
        t=next(i for i in range(j,n) if U[i]>>j&1)
        U[j],U[t]=U[t],U[j]
        for i in range(n):
            if i!=j and U[i]>>j&1:U[i]^=U[j]
    A=[[U[i]>>(n+j)&1 for j in range(n)] for i in range(n)]
    assert all(A[i][j]==A[j][i] for i in range(n) for j in range(n))
    diagonal=[A[i][i] for i in range(n)]
    for i in range(n):A[i][i]=0
    H=[swap(g)&mask for g in S]
    labels=nullspace(H,n)
    graphS=[x | (xor(sum(A[i][j]<<j for j in range(n)) for i in range(n) if x>>i&1)<<n) for x in H]
    c=certify(graphS,n)
    assert c['weight_enumerator']==certify(S,n)['weight_enumerator']
    return dict(adjacency=A,subgroup_x_masks=H,label_generators=labels,branch_labels=span(labels),certificate=c,local_H_mask=hs,removed_diagonal=diagonal,chart_trials=trial+1)

def prime_at_least(m):
    while any(m%q==0 for q in range(2,int(m**.5)+1)):m+=1
    return m

def parent_graph(n,p):
    # Cauchy matrix using the p finite points and infinity if n=p+1.
    m=n//2
    B=[[pow((i-j)%p,-1,p) if j<p else 1 for j in range(m,n)] for i in range(m)]
    return [[0 if (i<m)==(j<m) else (B[i][j-m] if i<m else B[j][i-m]) for j in range(n)] for i in range(n)]

def cuts(A,p):
    n=len(A);m=n//2;hist=Counter();sha=hashlib.sha256()
    # Deliberately check both orientations, all binomial(n,m) balanced cuts.
    for C in it.combinations(range(n),m):
        D=[i for i in range(n) if i not in C]
        r=modrank([[A[i][j] for j in D] for i in C],p)
        hist[r]+=1;sha.update((','.join(map(str,C))+':'+str(r)+'\n').encode())
    assert hist=={m:__import__('math').comb(n,m)}
    return dict(cut_size=m,all_balanced_cuts=sum(hist.values()),rank_histogram=dict(hist),ordered_cut_rank_sha256=sha.hexdigest(),matrix_sha256=digest(A))

def extension_search(S,n,d):
    mask=(1<<n)-1
    central=nullspace([(g>>n)|((g&mask)<<n) for g in S],2*n)
    allbasis=S[:];Q=[]
    for g in central:
        if len(basis(allbasis+[g]))>len(allbasis):Q.append(g);allbasis.append(g)
    W=span(S);hist=Counter();hits=[]
    for v in span(Q)[1:]:
        low=min(weight(v^w,n) for w in W)
        hist[low]+=1
        if low>=d:hits.append(v)
    return dict(N=n,target_distance=d,base_generators=S,quotient_basis=Q,cosets_examined=2**len(Q)-1,coset_minimum_histogram=dict(sorted(hist.items())),extension_representatives=hits)
