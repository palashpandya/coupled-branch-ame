"""Exact Hermitian parent replay, with no search entry point."""
import itertools
from .finite_field import field
def verify_parent(b):
 f=field(81);q=field(9);m=len(b);n=2*m
 assert all(f.sum(f.mul[b[i][l]][f.pow(b[j][l],9)] for l in range(m))==(f.neg[1] if i==j else 0) for i in range(m) for j in range(m))
 counts={}
 for s in range(1,m+1):
  ct=0
  for rr in itertools.combinations(range(m),s):
   for cc in itertools.combinations(range(m),s):assert f.rank([[b[i][j] for j in cc] for i in rr])==s;ct+=1
  counts[s]=ct
 # Embed our F9=t^2+1 representation in F81.
 u=next(x for x in range(3,81) if f.pow(x,2)==2 and f.pow(x,9)==x)
 emb=[f.add[a%3][f.mul[a//3][u]] for a in range(9)]
 assert all(emb[q.mul[a][b]]==f.mul[emb[a]][emb[b]] and emb[q.add[a][b]]==f.add[emb[a]][emb[b]] for a in range(9) for b in range(9))
 theta=next(x for x in range(1,81) if f.pow(x,9)==f.neg[x])
 dec={f.add[emb[a]][f.mul[theta][emb[z]]]:(a,z) for a in range(9) for z in range(9)};assert len(dec)==81
 rows=[[int(i==j) for j in range(m)]+b[i] for i in range(m)]
 expanded=[[dec[f.mul[scalar][x]] for x in row] for row in rows for scalar in [1,theta]]
 x=[[v[0] for v in row] for row in expanded];z=[[v[1] for v in row] for row in expanded]
 assert all(q.sum(q.add[q.mul[x[i][l]][z[j][l]]][q.neg[q.mul[z[i][l]][x[j][l]]]] for l in range(n))==0 for i in range(n) for j in range(n))
 for mask in range(1<<n):
  t=[[z[i][j] if mask>>j&1 else x[i][j] for j in range(n)]+[q.neg[x[i][j]] if mask>>j&1 else z[i][j] for j in range(n)] for i in range(n)]
  if q.rank([r[:n] for r in t])==n:break
 else:raise AssertionError('graph chart absent')
 for j in range(n):
  i=next(i for i in range(j,n) if t[i][j]);t[i],t[j]=t[j],t[i];scale=q.inv[t[j][j]];t[j]=[q.mul[v][scale] for v in t[j]]
  for i in range(n):
   if i!=j:
    scale=t[i][j];t[i]=[q.add[v][q.neg[q.mul[scale][w]]] for v,w in zip(t[i],t[j])]
 g=[r[n:] for r in t];diag=[g[i][i] for i in range(n)]
 for i in range(n):g[i][i]=0
 return dict(PASS=True,B=b,field81_polynomial=f.poly,field9_polynomial=q.poly,embedding=emb,theta=theta,graph=g,Fourier_mask=mask,removed_diagonal=diag,minor_counts=counts,graph_check=q.cuts(g))
