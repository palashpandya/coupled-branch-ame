"""Replay N9/N11 ingredients, F49 parents and all eight assembled states."""
from ._paths import DATA, RESULTS
from .small_exact import assembled, parent
from .o3_verify import determinant
from itertools import combinations
import copy,json

def read(name):return json.loads((DATA/name).read_text())
def cauchy(n,p):
    m=(n+1)//2
    cols=list(range(m,2*m)) if p>=2*m else list(range(m,2*m-1))+[None]
    assert p>=2*m-1
    c=[[1 if j is None else pow((i-j)%p,-1,p) for j in cols] for i in range(m)]
    return [[0]*m+c[i] for i in range(m)]+[[c[j][i] for j in range(m)]+[0]*m for i in range(m)]

def main():
    states=read('small_families_spec.json');certs=read('small_families_certificates.json')
    original=read('o1_external_spec.json')['constructions'];out={};parents={}
    for length in (10,12):
        parents[length]=parent(read(f'parent{length}_7.json'))
        assert parents[length]['cut_count']==(252 if length==10 else 924)
    for key,s in states.items():
        n,p=s['N'],s['p'];o=original[f'{n}_10']
        if n==9:
            b=o['binary_graph'];labels=[sum(x<<i for i,x in enumerate(a['binary_Z_mask'])) for a in o['branches']]
        else:
            b=[row[1:] for row in o['binary_parent_graph'][1:]]
            labels=[0,sum(x<<i for i,x in enumerate(o['binary_parent_graph'][0][1:]))]
        assert (s['binary_graph'],s['binary_labels'])==(b,labels)
        assert s['K']==len(labels)==(4 if n==9 else 2)
        expected=o['quinary_parent_graph'] if p==5 else parents[n+1]['graph'] if p==7 else cauchy(n,p)
        assert s['prime_parent_graph']==expected
        out[key]=assembled(s);assert out[key]==certs[key]
        # Second elimination direction independently certifies every determinant.
        for cut in combinations(range(n+1),(n+1)//2):
            other=[i for i in range(n+1) if i not in cut]
            assert determinant([[expected[i][j] for j in other] for i in cut],p)
        bad=copy.deepcopy(s);bad['prime_labels'][1]=bad['prime_labels'][0]
        try:assembled(bad)
        except AssertionError:pass
        else:raise AssertionError('duplicate-label control accepted')
        bad=copy.deepcopy(s);bad['prime_parent_graph']=[[0]*(n+1) for _ in range(n+1)]
        try:assembled(bad)
        except AssertionError:pass
        else:raise AssertionError('zero-parent control accepted')
        print('[PASS]',key,out[key]['parent_cuts'],'oriented cuts, exact binary average, negative controls')
    result=dict(status='PASS',constructions=out,parents=parents,oriented_cuts=sum(v['parent_cuts'] for v in out.values()))
    assert result['oriented_cuts']==4704
    (RESULTS/'small_families.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
