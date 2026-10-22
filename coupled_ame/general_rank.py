"""Exact arbitrary-spectrum rank bounds; no LP solver is needed for replay."""
from fractions import Fraction as F
from math import comb
import json
from ._paths import DATA, RESULTS

def system(n,r):
    variables=list(range(n//2+1,n+1))
    def coeff(j,i):
        return F(sum((-1)**a*3**(j-a)*comb(i,a)*comb(n-i,j-a)
                     for a in range(j+1) if a<=i and j-a<=n-i),2**n)
    b=[[coeff(j,i) for i in [0]+variables] for j in range(n+1)]
    A=[];rhs=[]
    def row(values):rhs.append(values[0]);A.append([-v for v in values[1:]])
    for j in range(n+1):
        row([r*v-int(i==j) for i,v in zip([0]+variables,b[j])])
        row([(-1)**i*v for i,v in zip([0]+variables,b[j])])
    row([1-b[0][0]]+[-v for v in b[0][1:]])
    for s in range(n+1):
        row([r*(comb(n-i,s-i) if i<=s else 0)-sum(comb(n-j,s-j)*b[j][t] for j in range(s+1)) for t,i in enumerate([0]+variables)])
        row([comb(n,s)*(2**s-1)]+[-comb(n-i,s-i) if i<=s else 0 for i in variables])
    return variables,A,rhs

def main():
    records=json.loads((DATA/'general_rank_certificates.json').read_text());out=[]
    for c in records:
        var,A,b=system(c['N'],c['excluded_rank']);y=list(map(F,c['multipliers']))
        assert len(y)==len(b) and all(v>=0 for v in y)
        columns=[sum(y[j]*A[j][i] for j in range(len(y))) for i in range(len(var))]
        value=sum(v*w for v,w in zip(y,b))
        assert all(v>=0 for v in columns) and value==F(c['value'])<0
        # Explicit exact point at the next rank: necessary conditions only.
        _,A1,b1=system(c['N'],c['excluded_rank']+1);x=list(map(F,c['next_rank_point']))
        assert len(x)==len(var) and all(v>=0 for v in x)
        assert all(sum(a*v for a,v in zip(row,x))<=rhs for row,rhs in zip(A1,b1))
        out.append(dict(N=c['N'],minimum_rank=c['excluded_rank']+1,value=str(value),status='PASS',next_rank='exact LP-feasible point; no state asserted'))
        print('[PASS]',out[-1])
    (RESULTS/'general_rank.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
