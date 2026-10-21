"""Reconstruct and certify the GF121 bordered-circulant AME(16,11) parent."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json,random,hashlib,time,sys
from ._paths import DATA, RESULTS
from .codes import modrank as rank_mod
P=11;NU=2

def add(x,y):return (x%P+y%P)%P+P*((x//P+y//P)%P)
def neg(x):return (-x%P)+P*((- (x//P))%P)
def mul(x,y):return ((x%P)*(y%P)+NU*(x//P)*(y//P))%P+P*(((x%P)*(y//P)+(x//P)*(y%P))%P)
def conj(x):return x%P+P*((- (x//P))%P)
def inv(x):
 assert x
 n=mul(x,conj(x));assert 0<n<P
 return mul(conj(x),pow(n,-1,P))
def total(xs):
 s=0
 for x in xs:s=add(s,x)
 return s
def determinant(a):
 a=[r[:] for r in a];d=1
 for j in range(len(a)):
  z=next((i for i in range(j,len(a)) if a[i][j]),None)
  if z is None:return 0
  if z!=j:a[z],a[j]=a[j],a[z];d=neg(d)
  v=a[j][j];d=mul(d,v)
  for i in range(j+1,len(a)):
   f=mul(a[i][j],inv(v))
   for k in range(j+1,len(a)):a[i][k]=add(a[i][k],neg(mul(f,a[j][k])))
 return d

def build():
 t=time.monotonic()
 assert pow(NU,5,P)==10 and all(mul(x,inv(x))==1 for x in range(1,121))
 stored=json.loads((DATA/'parent11_certificate.json').read_text());witness=stored['search_witness'];a,b,kap=witness['corner'],witness['border'],witness['kernel']
 B=[[a]+[b]*7]+[[b]+[kap[(j-i)%7] for j in range(7)] for i in range(7)]
 herm=[[total(mul(x,conj(y)) for x,y in zip(r,s)) for s in B] for r in B]
 assert herm==[[10*int(i==j) for j in range(8)] for i in range(8)]
 minors={}
 for size in range(1,9):
  count=0
  for r in combinations(range(8),size):
   for c in combinations(range(8),size):
    assert determinant([[B[i][j] for j in c] for i in r]);count+=1
  minors[size]=count
 assert sum(minors.values())==12869
 G=[[int(i==j) for j in range(8)]+B[i] for i in range(8)]
 expanded=[[mul(s,x) for x in row] for row in G for s in [1,11]]
 X=[[x%11 for x in row] for row in expanded];Z=[[x//11 for x in row] for row in expanded]
 assert all(sum(X[i][k]*Z[j][k]-Z[i][k]*X[j][k] for k in range(16))%11==0 for i in range(16) for j in range(16))
 rng=random.Random(152216)
 for trial in range(10000):
  mask=rng.getrandbits(16)
  T=[[Z[i][j] if mask>>j&1 else X[i][j] for j in range(16)]+[(-X[i][j])%11 if mask>>j&1 else Z[i][j] for j in range(16)] for i in range(16)]
  if rank_mod([r[:16] for r in T],11)==16:break
 else:raise RuntimeError('No graph chart')
 for j in range(16):
  z=next(i for i in range(j,16) if T[i][j]);T[j],T[z]=T[z],T[j]
  iv=pow(T[j][j],-1,11);T[j]=[x*iv%11 for x in T[j]]
  for i in range(16):
   if i!=j:
    v=T[i][j];T[i]=[(x-v*y)%11 for x,y in zip(T[i],T[j])]
 graph=[r[16:] for r in T];diagonal=[graph[i][i] for i in range(16)]
 assert all(graph[i][j]==graph[j][i] for i in range(16) for j in range(16))
 for i in range(16):graph[i][i]=0
 ranks=Counter();cut_records=[]
 for cut in combinations(range(16),8):
  other=[i for i in range(16) if i not in cut]
  rank=rank_mod([[graph[i][j] for j in other] for i in cut],11)
  assert rank==8;ranks[rank]+=1;cut_records.append({'cut':cut,'rank':rank})
 assert sum(ranks.values())==12870
 broken=[r[:] for r in graph];broken[0][1]=(broken[0][1]+1)%11;broken[1][0]=broken[0][1]
 failing=None
 for cut in combinations(range(16),8):
  other=[i for i in range(16) if i not in cut];rank=rank_mod([[broken[i][j] for j in other] for i in cut],11)
  if rank<8:failing={'cut':cut,'complement':other,'rank':rank};break
 assert failing is not None
 certificate=dict(status='PASS',p=11,field='a+11*b encodes a+b*theta; theta^2=2',search_witness=witness,B=B,
   hermitian_product=herm,all_square_minor_counts=minors,generator_GF121=G,
   stabilizer_X=X,stabilizer_Z=Z,local_Fourier_mask=mask,graph_chart_trial=trial+1,removed_diagonal=diagonal,
   graph=graph,balanced_cut_rank_histogram=dict(ranks),cut_orientations=12870,
   negative_control={'edge':[0,1],'increment':1,'graph':broken,'failure':failing},seconds=time.monotonic()-t)
 for key in ['B','hermitian_product','generator_GF121','stabilizer_X','stabilizer_Z','local_Fourier_mask','removed_diagonal','graph']:
  assert certificate[key]==stored[key],key
 state=json.loads((DATA/'o3_external_spec.json').read_text())['constructions']['15_22']
 assert state['prime_parent_graph']==graph
 from .o3_verify import determinant as prime_det
 assert prime_det([[broken[i][j] for j in failing['complement']] for i in failing['cut']],11)==0
 (RESULTS/'parent11.json').write_text(json.dumps(certificate,indent=2)+'\n')
 print('[PASS] GF121 parent: Hermitian product, 12869 minors, 12870 graph cuts and perturbed-edge control')
 return graph
if __name__=='__main__':build()
