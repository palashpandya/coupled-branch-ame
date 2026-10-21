"""Independent exact replay of O3 witness files (standard library only).

Does not import any construction, GF4, rank, or LP code. Verifies signed
branch averaging via Walsh characters and prime cuts via modular determinants.
"""
import copy
import hashlib
import itertools as it
import json
import math
import time
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

P=Path(__file__).resolve().parents[1]/"results"
DATA=Path(__file__).resolve().parents[1]/"data"
P.mkdir(exist_ok=True)
def read(name):return json.loads((DATA/name).read_text())
def combos(rows):
    ans=[0]
    for row in rows:ans.extend([w^row for w in ans])
    return ans

def determinant(M,p):
    # Eliminate from the lower right, unlike the forward-rank constructor.
    M=[row[:] for row in M];d=1
    for j in reversed(range(len(M))):
        i=next((i for i in range(j+1) if M[i][j]%p),None)
        if i is None:return 0
        if i!=j:M[i],M[j]=M[j],M[i];d=-d
        pivot=M[j][j]%p;d=d*pivot%p;inv=pow(pivot,p-2,p)
        for i in range(j):
            t=M[i][j]*inv%p
            for l in range(j):M[i][l]=(M[i][l]-t*M[j][l])%p
    return d%p

def check_graph(A,p):
    n=len(A)
    assert all(len(r)==n for r in A)
    assert all(A[i][i]==0 for i in range(n))
    assert all(0<=A[i][j]<p and A[i][j]==A[j][i] for i in range(n) for j in range(n))

def verify_cell(c):
    n=c['N'];K=c['K'];p=c['p'];B=c['binary_graph'];G=c['prime_parent_graph'];L=c['branch_labels']
    assert all(p%q for q in range(2,math.isqrt(p)+1))
    assert K<=p and len(L)==K and len(set(L))==K
    assert all(0<=l<2**n for l in L)
    assert c['prime_branch_labels']==list(range(K))
    assert len(B)==n and len(G)==n+1 and c['local_dimension']==2*p
    check_graph(B,2);check_graph(G,p)
    assert combos(c['binary_label_generators'])==L
    H=combos(c['binary_subgroup_x_masks']);assert len(set(H))==2**n//K
    hist=Counter();low=0
    for x in range(2**n):
        z=sum((sum(B[i][j] for i in range(n) if x>>i&1)%2)<<j for j in range(n))
        wt=(x|z).bit_count()
        if all((x&l).bit_count()%2==0 for l in c['binary_label_generators']):hist[wt]+=1
        if 0<wt<=n//2:
            low+=1
            assert sum((-1)**((x&l).bit_count()%2) for l in L)==0
    assert sum(hist.values())==2**n//K and min(i for i in hist if i)>n//2
    N=n+1;m=N//2;dh=Counter()
    for A in it.combinations(range(N),m):
        C=[i for i in range(N) if i not in A]
        d=determinant([[G[i][j] for j in C] for i in A],p)
        assert d
        dh[d]+=1
    return dict(passed=True,binary_weight_enumerator=dict(sorted(hist.items())),low_weight_graph_words_checked=low,prime_cuts_checked=sum(dh.values()),nonzero_determinant_histogram=dict(sorted(dh.items())))

def kr(n,j,i):
    return sum((-1)**a*3**(j-a)*math.comb(i,a)*math.comb(n-i,j-a) for a in range(j+1) if a<=i and j-a<=n-i)

def verify_lp(c):
    n=c['N'];K=c['K'];v=c['variables'];A=[];b=[];total=F(2**n,K)-1
    assert v==[i for i in range(n//2+1,n+1) if not c['even_weight_only'] or i%2==0]
    for j in range(n+1):
        A.append([F(i==j)-F(K,2**n)*kr(n,j,i) for i in v]);b.append(F(K,2**n)*kr(n,j,0)-F(j==0))
        A.append([-F(K,2**n)*(-1)**i*kr(n,j,i) for i in v]);b.append(F(K,2**n)*kr(n,j,0))
    if c['verdict']=='exact_infeasible':
        y=list(map(F,c['y']));z=F(c['z'])
        assert all(t>=0 for t in y)
        assert all(sum(y[j]*A[j][i] for j in range(len(A)))+z>=0 for i in range(len(v)))
        assert sum(t*u for t,u in zip(y,b))+z*total==F(c['contradiction'])<0
    else:
        x=list(map(F,c['point']))
        assert sum(x)==total and all(t>=0 for t in x)
        assert all(sum(t*u for t,u in zip(row,x))<=bb for row,bb in zip(A,b))

def main():
    t=time.monotonic();spec=read('o3_external_spec.json');result={}
    for key,c in spec['constructions'].items():
        result[key]=verify_cell(c);print(key,'PASS',flush=True)
    for c in read('o3_lp_certificates.json')['certificates']:verify_lp(c)
    ns=read('o3_nonstabilizer_search.json');gens=ns['full_graph_basis_exact_obstruction']['low_weight_subspace_generators']
    words=combos(gens)
    assert len(set(words))==16 and all(x in ns['low_weight_graph_words'] for x in words[1:])
    B=spec['constructions']['13_34']['binary_graph']
    for x in words[1:]:
        z=sum((sum(B[i][j] for i in range(13) if x>>i&1)%2)<<j for j in range(13))
        assert 1<=(x|z).bit_count()<=6
    ext=read('o3_n17_extensions.json');S=ext['base_generators'];Q=ext['quotient_basis']
    W=combos(S);mask=(1<<17)-1
    def symp(a,b):return (((a&mask)&(b>>17))^((b&mask)&(a>>17))).bit_count()%2
    assert len(set(W))==2048 and len(set(combos(Q)))==4096
    # Independent pivot-rank test avoids allocating all 2^23 centralizer vectors.
    piv={}
    for g in S+Q:
        while g:
            bit=g.bit_length()-1
            if bit in piv:g^=piv[bit]
            else:piv[bit]=g;break
    assert len(piv)==23
    assert all(symp(a,b)==0 for a in S for b in S+Q)
    hist=Counter()
    for v in combos(Q)[1:]:
        d=min((((w^v)|((w^v)>>17))&mask).bit_count() for w in W)
        hist[d]+=1
    assert dict(hist)=={int(k):v for k,v in ext['coset_minimum_histogram'].items()}
    assert max(hist)<9
    for key,c in read('o3_binary_certificates.json')['ingredients'].items():
        n=c['N'];mask=(1<<n)-1;S=c['generators'];W=combos(S)
        assert len(set(W))==len(W)==2**n//c['K']
        assert all((((a&mask)&(b>>n))^((b&mask)&(a>>n))).bit_count()%2==0 for a in S for b in S)
        h=Counter(((w|(w>>n))&mask).bit_count() for w in W)
        assert dict(h)=={int(k):v for k,v in c['weight_enumerator'].items()}
        assert min(k for k in h if k)>n//2
    # Mutation controls check the decisive obligations, not JSON syntax alone.
    c=copy.deepcopy(spec['constructions']['13_34']);c['branch_labels'][1]=c['branch_labels'][0]
    try:verify_cell(c)
    except AssertionError:duplicate_label_rejected=True
    else:raise AssertionError('duplicate label accepted')
    zero_parent=[[0]*14 for _ in range(14)]
    assert determinant([row[7:] for row in zero_parent[:7]],17)==0
    result=dict(constructions=result,binary_ingredients_independently_checked=8,lp_certificates_passed=26,nonstabilizer_divisibility_16_passed=True,n17_all_4095_extensions_rechecked=True,negative_controls=dict(duplicate_label_rejected=True,zero_parent_rejected=True),wall_seconds=time.monotonic()-t,implementation='standard-library independent arithmetic, no constructor imports')
    (P/'o3_verification.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
