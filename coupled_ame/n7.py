"""Exact Steane/all-cut N7 construction and arbitrary-K shadow obstruction."""
from ._paths import DATA, RESULTS
from .small_exact import assembled, parent, code
from .small_families import cauchy
from itertools import combinations, permutations
from fractions import Fraction as F
from math import comb
from collections import Counter
import copy,json

def read(name):return json.loads((DATA/name).read_text())
def determinant(a,p):
    n=len(a);value=0
    for order in permutations(range(n)):
        term=(-1)**sum(order[i]>order[j] for i in range(n) for j in range(i+1,n))
        for i,j in enumerate(order):term*=a[i][j]
        value+=term
    return value%p

def shadow_sum(n,p):return sum((-1)**s*F(comb(n,s),p**s) for s in range(n//2+1))
def shifted_coefficients(n):
    # p^k S(N,p), expanded in q=p-5: all coefficients positive proves p>=5.
    k=n//2
    return [sum((-1)**s*comb(n,s)*comb(k-s,j)*5**(k-s-j) for s in range(k-j+1)) for j in range(k+1)]
def main():
    g=read('steane_graph.json');gens=[85,102,120]+[x<<7 for x in (85,102,120)]
    assert g['original_generators']==gens and g['Fourier_mask']==15
    steane=code(dict(N=7,rank=6,distance=4,generators=gens))
    assert steane['weight_enumerator']=={0:1,4:21,6:42} and steane['K']==2
    span={0}
    for v in gens:span|={x^v for x in list(span)}
    def fourier(v):
        x,z=v&127,v>>7;t=(x^z)&15
        return (x^t)|((z^t)<<7)
    transformed={fourier(v) for v in span}
    graphwords=set()
    for x in range(128):
        z=sum((sum(g['graph'][i][j] for i in range(7) if x>>i&1)%2)<<j for j in range(7))
        if (x&7).bit_count()%2==0:graphwords.add(x|(z<<7))
    assert transformed==graphwords
    pc=parent(read('parent8_5.json'))
    assert json.loads(json.dumps(pc))==read('parent8_5_certificate.json')
    assert sum(pc['minor_counts'].values())==69
    states=read('n7_spec.json');certs=read('n7_certificates.json');out={}
    for key,s in states.items():
        p=s['p'];assert (s['binary_graph'],s['binary_labels'])==(g['graph'],g['labels'])
        assert s['prime_parent_graph']==(pc['graph'] if p==5 else cauchy(7,p))
        out[key]=assembled(s);assert out[key]==certs[key]
        cuts=[]
        for triple in combinations(range(7),3):
            a=[0]+[i+1 for i in triple];b=[j for j in range(8) if j not in a]
            value=determinant([[s['prime_parent_graph'][i][j] for j in b] for i in a],p);assert value
            cuts.append(value)
        out[key]['independent_35_cut_determinants']=cuts
        for field in ('prime_labels','binary_labels','prime_parent_graph'):
            bad=copy.deepcopy(s)
            if field=='prime_parent_graph':bad[field]=[[0]*8 for _ in range(8)]
            else:bad[field][1]=bad[field][0]
            try:assembled(bad)
            except AssertionError:pass
            else:raise AssertionError('negative control accepted: '+field)
        print('[PASS]',key,'70 parent cuts, 35 independent determinants and three negative controls')
    shadow=read('n7_shadow_certificate.json');shadow_out=[]
    for rec in shadow['results']:
        p,K=rec['p'],rec['K'];u=[]
        for mask in range(256):
            # Complement down to <=3 physical sites; reference is bit7.
            m=mask if (mask&127).bit_count()<=3 else 255^mask
            u.append(F(1,p**((m&127).bit_count())*(K if m&128 else 1)))
        assert u==list(map(F,rec['purities']))
        sv=[sum(v*(-1)**((t&m).bit_count()) for m,v in enumerate(u)) for t in range(256)]
        assert sv==list(map(F,rec['shadow_values'])) and all(x>=0 for x in sv)==rec['feasible']
        assert sv[255]==2*(1-F(1,K))*shadow_sum(7,p)
        shadow_out.append(dict(p=p,K=K,all_party_row=str(sv[255]),feasible=rec['feasible']))
    assert shadow_sum(7,3)==-F(8,27)
    signs={}
    for n in range(7,20,2):
        coeff=shifted_coefficients(n);assert all(c>0 for c in coeff)
        excluded=[p for p in (2,3) if shadow_sum(n,p)<0]
        assert excluded==([2,3] if n%4==3 else [])
        signs[n]=dict(excluded_primes=excluded,S2=str(shadow_sum(n,2)),S3=str(shadow_sum(n,3)),shifted_coefficients=coeff)
    assert shadow_sum(27,5)<0 # Do not extrapolate the finite sign table to all N.
    result=dict(status='PASS',steane=steane,parent=pc,constructions=out,oriented_cuts=210,shadow_rows=shadow_out,sign_table=signs,counterexample_to_all_N_extrapolation={'N':27,'p':5,'S':str(shadow_sum(27,5))})
    (RESULTS/'n7.json').write_text(json.dumps(result,indent=2)+'\n')
    print('[PASS] exact shadow replay; S(7,3)=-8/27; all-prime sign table for N=7..19')
if __name__=='__main__':main()
