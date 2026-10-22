"""Check caller-supplied pinned Kitamura data; third-party matrices not distributed."""
import ast, itertools, json, re, hashlib, os
from pathlib import Path
import numpy as np
from .finite_field import field
from ._paths import DATA, RESULTS
def digits(base,N):return (np.arange(base**N)[:,None]//base**np.arange(N-1,-1,-1))%base


def read_data(source):
    text=source.read_text();matrices={}
    for name,modulus in [('G',2),('B',3),('H',3),('C',3)]:
        match=re.search(r'def '+name+r'\s*:.*?:=\s*(.*?)(?=\ndef |\ntheorem |\nend)',text,re.S)
        assert match is not None;A=np.array(ast.literal_eval(match.group(1).replace('!','')),dtype=np.int64)
        assert A.shape==(9,9) and np.all((0<=A)&(A<modulus))
        if name!='B':assert np.array_equal(A,A.T) and np.all(np.diag(A)==0)
        matrices[name]=A
    return matrices


def exact_check(matrices):
    G,B,H,C=[matrices[name] for name in ['G','B','H','C']]
    ternary=digits(3,4);signed=ternary.copy();signed[signed==2]=-1
    d=np.repeat(signed,81,axis=0);e=np.tile(ternary,(81,1));nonzero=np.any(d!=0,axis=1)|np.any(e!=0,axis=1)
    multiplicity=2**np.sum(d==0,axis=1)*3**4;records=[]
    for cut in itertools.combinations(range(9),4):
        rest=tuple(i for i in range(9) if i not in cut)
        alpha=(d@B[np.ix_(cut,rest)]+e@C[np.ix_(cut,rest)])%3
        binary=(np.asarray(d!=0,dtype=np.int64)@G[np.ix_(cut,rest)])%2
        beta=(e@B[np.ix_(rest,cut)].T+d@H[np.ix_(cut,rest)])%3
        ternary_zero=np.any(alpha!=0,axis=1)
        binary_zero=np.any((binary==1)&(beta==0),axis=1)
        violations=nonzero&~ternary_zero&~binary_zero
        binary_squared=np.where(beta==0,np.where(binary==0,4,0),np.where(binary==0,1,3))
        numerator=int(np.sum(multiplicity[nonzero&~ternary_zero]*3**10*np.prod(binary_squared[nonzero&~ternary_zero],axis=1)))
        records.append(dict(cut=cut,difference_types=int(np.sum(nonzero)),
            ternary_cancellations=int(np.sum(nonzero&ternary_zero)),
            binary_only_cancellations=int(np.sum(nonzero&~ternary_zero&binary_zero)),
            violations=int(np.sum(violations)),exact_squared_Frobenius_numerator=numerator))
    return dict(cuts=126,difference_types=sum(r['difference_types'] for r in records),
        ternary_cancellations=sum(r['ternary_cancellations'] for r in records),
        binary_only_cancellations=sum(r['binary_only_cancellations'] for r in records),
        violations=sum(r['violations'] for r in records),squared_Frobenius_denominator=6**18,cut_records=records)




def main():
 pin=json.loads((DATA/'kitamura96-source.json').read_text())
 name=os.environ.get('KITAMURA96_DATA')
 if not name:
  result=dict(status='NOT_RUN',reason='Set KITAMURA96_DATA to pinned Data.lean; see docs/R10-prime-powers.md',source_sha256=pin['sha256'])
  (RESULTS/'kitamura96.json').write_text(json.dumps(result,indent=2)+'\n')
  print('[NOT RUN] external Kitamura data not supplied; no verification claimed');return
 source=Path(name);assert hashlib.sha256(source.read_bytes()).hexdigest()==pin['sha256']
 m=read_data(source);out=exact_check(m)
 assert out['violations']==0 and all(x['exact_squared_Frobenius_numerator']==0 for x in out['cut_records'])
 bad={k:v.copy() for k,v in m.items()};bad['B'][:]=0;bad['H'][:]=0
 negative=exact_check(bad);assert negative['violations']==160
 B,H,C=m['B'],m['H'],m['C'];active=[i for i in range(9) if np.any(B[i])]
 assert active==[0,1,2,3] and field(3).rank(B[:4].tolist())==4
 assert all(H[i,j]==0 for i in range(9) for j in range(9) if i not in active or j not in active)
 labels={tuple((np.array(bits)@B[:4]%3).tolist()) for bits in itertools.product([0,1],repeat=4)}
 assert len(labels)==16
 out.update(status='PASS',source_sha256=pin['sha256'],negative_control_violations=160,active_binary_sites=active,ternary_graph=field(3).cuts(C.tolist()),branches=16,distinct_ternary_labels=len(labels),structure='Binary branches have disjoint support on four fixed bits and normalized flat remaining amplitudes; H phase absorbed. Ternary rays form distinct graph-basis labels. No all-cut erasure or LU-equivalence assertion.')
 (RESULTS/'kitamura96.json').write_text(json.dumps(out,indent=2)+'\n');print('[PASS] Kitamura126 cuts;826560 differences;16-branch structure; negative control')
if __name__=='__main__':main()
