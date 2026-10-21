#!/usr/bin/env python3
"""Standalone SYM1 exact verifier. Python standard library only; no constructor imports.
Reads O3 and SYM1 JSON; writes only sym1_verification.json. No network, git or GPU.
The spectral isometry is verified through exact projector-rank identities in
Q[z]/Phi_M, not floating eigenvectors. See docs/sym1_notes.md for completeness proofs.
"""
import copy,hashlib,itertools,json,math,time,resource
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"results"
DATA=Path(__file__).resolve().parents[1]/"data"
P.mkdir(exist_ok=True)

def read(name):return json.loads((DATA/name).read_text())
def span(gs):
 out=[0]
 for g in gs:out += [v^g for v in out]
 return out

def nullp(rows,n,p):
 if p==2:
  piv={}
  for row in rows:
   x=sum((v%2)<<j for j,v in enumerate(row))
   while x:
    b=x.bit_length()-1
    if b in piv:x^=piv[b]
    else:piv[b]=x;break
  out=[]
  for j in range(n):
   if j in piv:continue
   x=1<<j
   for b in sorted(piv):
    if (piv[b]&x).bit_count()%2:x^=1<<b
   out.append([x>>i&1 for i in range(n)])
  return out
 a=[[x%p for x in row] for row in rows];piv=[];r=0
 for j in range(n):
  k=next((k for k in range(r,len(a)) if a[k][j]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];a[r]=[v*pow(a[r][j],-1,p)%p for v in a[r]]
  for i in range(len(a)):
   if i!=r and a[i][j]:
    t=a[i][j];a[i]=[(x-t*y)%p for x,y in zip(a[i],a[r])]
  piv.append(j);r+=1
 out=[]
 for j in range(n):
  if j in piv:continue
  v=[0]*n;v[j]=1
  for i,k in enumerate(piv):v[k]=-a[i][j]%p
  out.append(v)
 return out

def determinant(a,p):
 a=[row[:] for row in a];ans=1;n=len(a)
 for j in range(n):
  k=next((k for k in range(j,n) if a[k][j]%p),None)
  if k is None:return 0
  if k!=j:a[k],a[j]=a[j],a[k];ans=-ans
  pivot=a[j][j]%p;ans=ans*pivot%p;inv=pow(pivot,-1,p)
  for i in range(j+1,n):
   t=a[i][j]*inv%p
   for k in range(j+1,n):a[i][k]=(a[i][k]-t*a[j][k])%p
 return ans%p

def graphcheck(A,p):
 assert all(len(row)==len(A) for row in A)
 assert all(A[i][i]==0 for i in range(len(A)))
 assert all(0<=A[i][j]<p and A[i][j]==A[j][i] for i in range(len(A)) for j in range(len(A)))

def gpauli(B,x):
 n=len(B);z=sum((sum(B[i][j] for j in range(n) if x>>j&1)%2)<<i for i in range(n))
 q=2*(sum(B[i][j] for i in range(n) for j in range(i) if (x>>i&1) and (x>>j&1))%2)
 return x,z,q

def ame(c,cache):
 n=c['N'];p=c['p'];K=c['K'];B=c['binary_graph'];G=c['prime_parent_graph'];ls=c['binary_label_generators']
 assert len(B)==n and len(G)==n+1 and c['local_dimension']==2*p
 assert all(p%j for j in range(2,math.isqrt(p)+1));graphcheck(B,2);graphcheck(G,p)
 assert span(ls)==c['branch_labels'] and len(set(span(ls)))==K
 H=span(c['binary_subgroup_x_masks']);assert len(set(H))==len(H)==2**n//K
 assert all((h&l).bit_count()%2==0 for h in H for l in ls)
 hist=Counter((x|gpauli(B,x)[1]).bit_count() for x in H);assert min(w for w in hist if w)>n//2
 fingerprint=json.dumps([p,G]);cuts=0
 if fingerprint not in cache:
  for A0 in itertools.combinations(range(1,n+1),n//2):
   A=(0,)+A0;C=[i for i in range(n+1) if i not in A]
   assert determinant([[G[i][j] for j in C] for i in A],p)!=0
   cuts+=1
  cache.add(fingerprint)
 return {'binary_weights':dict(hist),'new_parent_cut_orientations':cuts}

def local_space(D,H,L,perm,p):
 n=len(D);rows=[]
 for x in H:
  z=[sum(a*b for a,b in zip(row,x))%p for row in D];xx=[0]*n;zz=[0]*n
  for j,k in enumerate(perm):xx[k]=x[j];zz[k]=z[j]
  for i in range(n):
   row=[0]*(4*n);row[4*i+2]=xx[i];row[4*i+3]=zz[i]
   for j in range(n):row[4*j]-=D[i][j]*xx[j];row[4*j+1]-=D[i][j]*zz[j]
   rows.append(row)
  for l in L:
   row=[0]*(4*n)
   for i in range(n):row[4*i]=l[i]*xx[i];row[4*i+1]=l[i]*zz[i]
   rows.append(row)
 return nullp(rows,4*n,p)

def binary_data(c):
 n=c['N'];return c['binary_graph'],[[x>>j&1 for j in range(n)] for x in c['binary_subgroup_x_masks']],[[x>>j&1 for j in range(n)] for x in c['binary_label_generators']]

def prime_data(c):
 n=c['N'];G=c['prime_parent_graph'];h=G[0][1:];return [r[1:] for r in G[1:]],nullp([h],n,c['p']),[h]

def symplectic_solutions(bs,p):
 if not bs:return []
 out=[];n=len(bs[0])//4
 for co in itertools.product(range(p),repeat=len(bs)):
  v=[sum(a*b[j] for a,b in zip(co,bs))%p for j in range(4*n)]
  if all((v[i]*v[i+3]-v[i+1]*v[i+2])%p==1 for i in range(0,4*n,4)):out.append(v)
 return out

def in_span(v,bs,p):
 # Rank test, independent of the constructor's basis choice.
 return len(nullp(bs,len(v),p))==len(nullp(bs+[v],len(v),p))

def support_colors(c):
 n=c['N'];hist=[[0]*(n+1) for _ in range(1<<n)]
 for x in span(c['binary_subgroup_x_masks']):
  w=x|gpauli(c['binary_graph'],x)[1];hist[w][w.bit_count()]+=1
 for j in range(n):
  for x in range(1<<n):
   if not x>>j&1:hist[x]=[a+b for a,b in zip(hist[x],hist[x|(1<<j)])]
 colors={t:i for i,t in enumerate(sorted(set(map(tuple,hist))))}
 return [colors[tuple(x)] for x in hist]

def automorphisms(col,n):
 out=[];perm=[0]*n;mapped=[0]*(1<<n)
 def dfs(d,used):
  if d==n:out.append(perm[:]);return
  for v in range(n):
   if used>>v&1:continue
   bit=1<<v
   if any(col[s|(1<<d)]!=col[mapped[s]|bit] for s in range(1<<d)):continue
   perm[d]=v
   for s in range(1<<d):mapped[s|(1<<d)]=mapped[s]|bit
   dfs(d+1,used|bit)
 dfs(0,0);return out

def conjugate(v,perm,maps):
 x,z,q=v;xx=zz=0
 for i,j in enumerate(perm):
  a,b,c,d=maps[4*j:4*j+4];xi=x>>i&1;zi=z>>i&1
  q+=a*c*xi+b*d*zi+2*c*b*xi*zi;xx|=((a*xi+b*zi)%2)<<j;zz|=((c*xi+d*zi)%2)<<j
 return xx,zz,q%4

def verify_logical(c,perm,maps,corr,images=None):
 n=c['N'];B=c['binary_graph'];ls=c['binary_label_generators'];m=len(ls);cx,cz=corr
 ts=[]
 for j in range(m):
  ts.append(next(t for t in range(1<<n) if all((t&l).bit_count()%2==int(i==j) for i,l in enumerate(ls))))
 def image(v):
  x,z,q=conjugate(v,perm,maps);q=(q+2*(((cx&z)^(cz&x)).bit_count()%2))%4;return x,z,q
 for h in c['binary_subgroup_x_masks']:
  x,z,q=image(gpauli(B,h));assert (x,z,q)==gpauli(B,x)
 computed=[]
 for v in [(0,l,0) for l in ls]+[gpauli(B,t) for t in ts]:
  x,z,q=image(v);_,gz,gq=gpauli(B,x);a=c['branch_labels'].index(z^gz);b=sum(((x&l).bit_count()%2)<<j for j,l in enumerate(ls));qq=(q-gq+2*((a&b).bit_count()%2))%4
  computed.append([a,b,qq])
 if images is not None:assert images==computed
 return computed

# Gaussian integer matrix arithmetic, represented by exact (real, imaginary) pairs.
def ga(a,b):return (a[0]+b[0],a[1]+b[1])
def gm(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def gc(a):return (a[0],-a[1])
def mm(A,B):
 n=len(A);out=[[(0,0) for _ in B[0]] for _ in A]
 for i in range(n):
  for k in range(len(B)):
   if A[i][k]!=(0,0):
    for j in range(len(B[0])):out[i][j]=ga(out[i][j],gm(A[i][k],B[k][j]))
 return out

def eye(n):return [[(int(i==j),0) for j in range(n)] for i in range(n)]
def dagger(A):return [[gc(A[j][i]) for j in range(len(A))] for i in range(len(A[0]))]
def pmat(K,x,z,q):
 A=[[(0,0)]*K for _ in range(K)];phase=[(1,0),(0,1),(-1,0),(0,-1)][q]
 for j in range(K):A[j^x][j]=gm(phase,(-1 if (j&z).bit_count()%2 else 1,0))
 return A

# All needed normalization fields are Q(zeta_8), Q(zeta_16), Q(zeta_24).
class Field:
 def __init__(self,M):
  self.M=M;self.mod={8:[1,0,0,0,1],16:[1,0,0,0,0,0,0,0,1],24:[1,0,0,0,-1,0,0,0,1]}[M];self.d=len(self.mod)-1
 def red(self,a):
  a=list(map(F,a))+[F(0)]*max(0,self.d-len(a))
  for j in range(len(a)-1,self.d-1,-1):
   v=a[j]
   for k in range(self.d):a[j-self.d+k]-=v*self.mod[k]
  return tuple(a[:self.d])
 def const(self,x):return self.red([x])
 def add(self,a,b):return tuple(x+y for x,y in zip(a,b))
 def mul(self,a,b):
  v=[F(0)]*(2*self.d-1)
  for i,x in enumerate(a):
   for j,y in enumerate(b):v[i+j]+=x*y
  return self.red(v)
 def scale(self,a,x):return tuple(y*x for y in a)
 def z(self,e):return self.red([0]*(e%self.M)+[1])
 def pow(self,a,e):
  v=self.const(1)
  for _ in range(e):v=self.mul(v,a)
  return v

def spectral_check(iso):
 Q=[[tuple(x) for x in row] for row in iso['Q']];K=len(Q);D=iso['D'];L=iso['order'];M=math.lcm(8,4*L);fld=Field(M);eta=fld.z(iso['eta_exponent']*(M//(4*L)))
 assert mm(dagger(Q),Q)==[[(D*int(i==j),0) for j in range(K)] for i in range(K)]
 exponent=D.bit_length()-1;assert D==1<<exponent
 invroot=fld.const(F(1,2**(exponent//2)))
 if exponent%2:invroot=fld.mul(invroot,fld.scale(fld.add(fld.z(M//8),fld.z(-M//8)),F(1,2)))
 factor=fld.mul(eta,invroot);A=eye(K);traces=[]
 for j in range(L+1):
  tr=(sum(A[i][i][0] for i in range(K)),sum(A[i][i][1] for i in range(K)))
  ztr=fld.add(fld.const(tr[0]),fld.scale(fld.z(M//4),tr[1]));traces.append(fld.mul(fld.pow(factor,j),ztr))
  if j<L:A=mm(A,Q)
 scale=fld.pow(factor,L)
 for i in range(K):
  for j in range(K):
   z=fld.add(fld.const(A[i][j][0]),fld.scale(fld.z(M//4),A[i][j][1]));assert fld.mul(scale,z)==fld.const(int(i==j))
 mult=[]
 for r in range(L):
  v=fld.const(0)
  for j in range(L):v=fld.add(v,fld.mul(traces[j],fld.z(-r*j*(M//L))))
  v=fld.scale(v,F(1,L));assert all(x==0 for x in v[1:]) and v[0].denominator==1 and v[0]>=0;mult.append(int(v[0]))
 assert sum(mult)==K
 return mult

# Logical action of a prime symplectic map, including singular maps when defined.
def prime_logical(c,perm,v):
 D,H,L=prime_data(c);h=L[0];p=c['p'];n=c['N'];j0=next(i for i,x in enumerate(h) if x);t=[0]*n;t[j0]=-pow(h[j0],-1,p)%p
 def action(x,z):
  xx=[0]*n;zz=[0]*n
  for i,j in enumerate(perm):
   a,b,cc,d=v[4*j:4*j+4];xx[j]=(a*x[i]+b*z[i])%p;zz[j]=(cc*x[i]+d*z[i])%p
  delta=[(zz[i]-sum(D[i][j]*xx[j] for j in range(n)))%p for i in range(n)];aa=delta[j0]*pow(h[j0],-1,p)%p
  assert all(delta[i]==aa*h[i]%p for i in range(n));bb=-sum(h[i]*xx[i] for i in range(n))%p;return aa,bb
 a,cc=action([0]*n,h);b,d=action(t,[sum(row[j]*t[j] for j in range(n))%p for row in D]);return [a,b,cc,d]

def prime_diagonal(c,perm,basis):
 p=c['p'];n=c['N'];D,H,L=prime_data(c);h=L[0];j0=next(i for i,x in enumerate(h) if x);t=[0]*n;t[j0]=-pow(h[j0],-1,p)%p;defects=[]
 for x,z in [([0]*n,h),(t,[sum(row[j]*t[j] for j in range(n))%p for row in D])]:
  ds=[]
  for v in basis:
   xx=[0]*n;zz=[0]*n
   for i,j in enumerate(perm):
    a,b,cc,d=v[4*j:4*j+4];xx[j]=(a*x[i]+b*z[i])%p;zz[j]=(cc*x[i]+d*z[i])%p
   delta=[(zz[i]-sum(D[i][j]*xx[j] for j in range(n)))%p for i in range(n)];aa=delta[j0]*pow(h[j0],-1,p)%p;ds.append([(delta[i]-aa*h[i])%p for i in range(n)])
  defects += [list(row) for row in zip(*ds)]
 ns=nullp(defects,len(basis),p);basis=[[sum(co[k]*basis[k][j] for k in range(len(basis)))%p for j in range(4*n)] for co in ns]
 if not basis:return []
 lm=[prime_logical(c,perm,v) for v in basis];ns=nullp([[m[j] for m in lm] for j in (1,2)],len(basis),p);bs=[[sum(co[k]*basis[k][j] for k in range(len(basis)))%p for j in range(4*n)] for co in ns]
 return [(v,prime_logical(c,perm,v)) for v in symplectic_solutions(bs,p)]

def field(p,ext=False):
 q=p*p if ext else p
 add=lambda x,y:((x%p+y%p)%p)+p*((x//p+y//p)%p) if ext else (x+y)%p
 neg=lambda x:(-x%p)+p*((-(x//p))%p) if ext else -x%p
 mul=lambda x,y:((x%p*(y%p)+2*(x//p)*(y//p))%p)+p*((x%p*(y//p)+(x//p)*(y%p))%p) if ext else x*y%p
 M=[[mul(x,y) for y in range(q)] for x in range(q)];A=[[add(x,y) for y in range(q)] for x in range(q)];N=[neg(x) for x in range(q)]
 inv=[0]+[next(y for y in range(1,q) if M[x][y]==1) for x in range(1,q)]
 conj=lambda x:x%p+p*(-(x//p)%p) if ext else x
 return M,A,N,inv,conj

def det(a,F):
 M,A,N,I,_=F;a=[r[:] for r in a];d=1
 for j in range(len(a)):
  i=next((i for i in range(j,len(a)) if a[i][j]),None)
  if i is None:return 0
  if i!=j:a[i],a[j]=a[j],a[i];d=N[d]
  d=M[d][a[j][j]];v=I[a[j][j]]
  for i in range(j+1,len(a)):
   t=M[a[i][j]][v]
   for k in range(j+1,len(a)):a[i][k]=A[a[i][k]][N[M[t][a[j][k]]]]
 return d

def colors_for(c):
 n=c['N']+1;m=n//2;p=c['p'];ext='prime_parent_provenance' in c;F=field(p,ext);M,A,N,I,C=F
 colors={};quad={};start=time.monotonic()
 if ext:
  B=c['prime_parent_provenance']['B'];E=[[int(i==j) for j in range(m)]+B[i] for i in range(m)]
  ds={sum(1<<j for j in J):det([[row[j] for j in J] for row in E],F) for J in itertools.combinations(range(n),m)}
  assert all(ds.values())
 canon={}
 for r in range(1,len(I)):
  if r==1:continue
  r1=A[1][N[r]];vs=[r,r1,I[r],I[r1],M[r][I[r1]],M[r1][I[r]]]
  # correct anharmonic last values: r/(r-1), (r-1)/r
  vs[-2]=N[vs[-2]];vs[-1]=N[vs[-1]]
  canon[r]=min(vs+[C(x) for x in vs])
 for abcd in itertools.combinations(range(n),4):
  a,b,cc,d=abcd;mask=sum(1<<j for j in abcd)
  if not ext:
   r=(a-b)*(cc-d)*pow((a-cc)*(b-d)%p,-1,p)%p;hist=((canon[r],1),)
  else:
   hist0=Counter();remain=[j for j in range(n) if j not in abcd]
   for J in itertools.combinations(remain,m-2):
    z=sum(1<<j for j in J)
    r=M[M[ds[z|(1<<a)|(1<<b)]][ds[z|(1<<cc)|(1<<d)]]][I[M[ds[z|(1<<a)|(1<<cc)]][ds[z|(1<<b)|(1<<d)]]]]
    # signs from inserting indices after the same ordered J cancel.
    # Relative signs of pairs are + for a<b<c<d.
    hist0[canon[r]]+=1
   hist=tuple(sorted(hist0.items()))
  if hist not in colors:colors[hist]=len(colors)+1
  quad[mask]=colors[hist]
 col=[0]*(1<<n)
 for mask,k in quad.items():col[mask]=k
 for size in (3,2,1):
  dic={}
  for J in itertools.combinations(range(n),size):
   mask=sum(1<<j for j in J);v=tuple(sorted(Counter(col[mask|(1<<j)] for j in range(n) if not mask>>j&1).items()))
   if v not in dic:dic[v]=len(dic)+1
   col[mask]=dic[v]
 return col,{'quad_colors':len(colors),'seconds':time.monotonic()-start}


def cycles(g):
 out=[];seen=set()
 for i in range(len(g)):
  if i in seen:continue
  cy=[];j=i
  while j not in seen:seen.add(j);cy.append(j);j=g[j]
  out.append(cy)
 return out

def check_hz_chart(c):
 p=c['p'];prov=c['prime_parent_provenance'];B=prov['B'];m=len(B);n=2*m;M,A,N,I,conj=field(p,True)
 E=[[int(i==j) for j in range(m)]+B[i] for i in range(m)]
 rows=[[M[a][v] for v in row] for row in E for a in (1,p)];mask=prov['local_Fourier_mask']
 XX=[[v%p for v in row] for row in rows];ZZ=[[v//p for v in row] for row in rows]
 T=[[ZZ[i][j] if mask>>j&1 else XX[i][j] for j in range(n)]+[(-XX[i][j])%p if mask>>j&1 else ZZ[i][j] for j in range(n)] for i in range(n)]
 for j in range(n):
  k=next(i for i in range(j,n) if T[i][j]);T[j],T[k]=T[k],T[j];T[j]=[v*pow(T[j][j],-1,p)%p for v in T[j]]
  for i in range(n):
   if i!=j:
    t=T[i][j];T[i]=[(a-t*b)%p for a,b in zip(T[i],T[j])]
 G=[row[n:] for row in T];assert [G[i][i] for i in range(n)]==prov['removed_diagonal']
 for i in range(n):G[i][i]=0
 assert G==c['prime_parent_graph']

def verify_parent(c,cert):
 n=c['N']+1;p=c['p'];G=c['prime_parent_graph'];ext='prime_parent_provenance' in c
 if ext:check_hz_chart(c)
 else:
  m=n//2;C=[row[m:] for row in G[:m]];assert C==[[pow((i-j)%p,-1,p) for j in range(m,n)] for i in range(m)];E=[[int(i==j) for j in range(m)]+C[i] for i in range(m)]
  weights=nullp([[E[i][t]*E[j][t] for t in range(n)] for i in range(m) for j in range(i,m)],n,p)
  assert len(weights)==1 and all(weights[0]) # E^perp = diag(w) E
 col,stats=colors_for(c);candidates=automorphisms(col,n);assert len(candidates)==cert['candidate_permutations']
 hits={tuple(h['perm']):h['maps'] for h in cert['representatives']};assert set(hits)==set(map(tuple,candidates))
 H=[[int(i==j) for j in range(n)] for i in range(n)]
 for perm in candidates:
  basis=local_space(G,H,[],perm,p);v=hits[tuple(perm)];assert len(basis)==len(cert['kernel_basis']) and in_span(v,basis,p)
  assert all((v[i]*v[i+3]-v[i+1]*v[i+2])%p==1 for i in range(0,4*n,4))
 bs=cert['kernel_basis'];real=local_space(G,H,[],list(range(n)),p);assert len(bs)==len(real) and all(in_span(v,real,p) for v in bs)
 def ds(v):return [(v[i]*v[i+3]-v[i+1]*v[i+2])%p for i in range(0,4*n,4)]
 for v in bs+[[a+b for a,b in zip(bs[i],bs[j])] for i in range(len(bs)) for j in range(i)]:assert len(set(ds(v)))==1
 assert not nullp([b[:4] for b in bs],4,p) if len(bs)==4 else True
 kernel=p*(p*p-1) if len(bs)==4 else len(symplectic_solutions(bs,p))
 assert kernel==cert['parent_unsigned_kernel_order'];assert len(hits)*kernel==cert['parent_unsigned_order']
 assert len(hits)*kernel*p**n==cert['parent_projective_clifford_order']
 assert sum(h[0]==0 for h in hits)==cert['fix0_permutation_order']
 return {'complete_permutation_order':len(hits),'unsigned_local_kernel_order':kernel,'conditioned_permutation_order':cert['fix0_permutation_order']}

def verify_redesign(c):
 iso=c['isometry'];K=c['K'];n=c['N'];p=c['p']
 if iso['type']=='coordinate_inclusion':
  assert len(set(iso['columns']))==K and all(0<=x<p for x in iso['columns']);assert not c['symmetry_generators'];return {'certified_group_order':1,'isometry':'coordinate inclusion'}
 mult=spectral_check(iso);L=iso['order'];t=iso['prime_slope'];assert pow(t,L,p)==1 and all(pow(t,j,p)!=1 for j in range(1,L))
 assert all(mult[(-j)%L]<=(p-1)//L+int(j==0) for j in range(L))
 Q=[[tuple(z) for z in row] for row in iso['Q']];D=iso['D'];assert len(Q)==K
 for g in c['symmetry_generators']:
  perm=g['perm'];assert sorted(perm)==list(range(n));assert math.lcm(*(len(cy) for cy in cycles(perm)))==c['certified_permutation_group']['order']
  ims=verify_logical(c,perm,g['binary_maps'],g['binary_pauli_correction'])
  m=K.bit_length()-1
  for j,im in enumerate(ims):
   base=pmat(K,1<<j if j<m else 0,1<<(j-m) if j>=m else 0,0);left=mm(mm(Q,base),dagger(Q));right=pmat(K,*im)
   assert left==[[(D*a,D*b) for a,b in row] for row in right]
  v=g['prime_maps'];assert all((v[i]*v[i+3]-v[i+1]*v[i+2])%p==1 for i in range(0,4*n,4))
  assert in_span(v,local_space(*prime_data(c),perm,p),p);assert prime_logical(c,perm,v)==g['logical_prime_map']==[t,0,0,pow(t,-1,p)]
 return {'certified_group_order':c['certified_permutation_group']['order'],'exact_logical_eigenvalue_multiplicities':mult,'isometry':'exact spectral-projector Gram-Schmidt; rank bounds checked in cyclotomic field'}

def verify_inventory(src,parents):
 inv=read('sym1_symmetry_generators.json')['cells'];checks={}
 for key,c in src.items():
  n=c['N']+1;p=c['p'];bs=parents[key]['kernel_basis'];g=inv[key]
  for x in g['parent_generators']['unsigned_local_kernel_maps']:
   assert in_span(x,bs,p)
   assert all((x[j]*x[j+3]-x[j+1]*x[j+2])%p==1 for j in range(0,4*n,4))
  reps={tuple(h['perm']):h['maps'] for h in parents[key]['representatives']}
  for h in g['parent_generators']['permutation_lifts']+g['reference_fixing_generators']['permutation_lifts']:assert h['maps']==reps[tuple(h['perm'])]
  q=parents[key]['fix0_permutation_order'];K=c['K'];r=c['N']-(K.bit_length()-1)
  assert g['as_built']['projective_local_order']==2**(r+1)*p**(n-2)
  H=prime_data(c)[1];assert H==g['as_built']['prime_stabilizer_x_vectors']
  aff=[(a,d) for a in range(1,p) for d in range(p) if {(a*x+d)%p for x in range(K)}==set(range(K))]
  assert list(map(list,aff))==g['logical_affine_interval_stabilizer']
  if len(bs)==4:
   assert [x[:4] for x in g['parent_generators']['unsigned_local_kernel_maps']]==[[1,1,0,1],[1,0,1,1]]
   assert g['W_preserving_physical_projective_order']==q*p**n*len(aff)
   assert g['computational_conditioning_projective_order']==q*p*(p-1)*p**n
  else:
   total=0;mono=0;wp=set();unit=g['parent_generators']['unsigned_local_kernel_maps'][0][:4]
   power=[1,0,0,1];first=None
   for j in range(1,15):
    a,b,cc,d=power;e,f,hh,k=unit;power=[(a*e+b*hh)%p,(a*f+b*k)%p,(cc*e+d*hh)%p,(cc*f+d*k)%p]
    if power==[1,0,0,1] and first is None:first=j
   assert first==14
   for h in parents[key]['representatives']:
    if h['perm'][0]!=0:continue
    space=local_space(c['prime_parent_graph'],[[int(i==j) for j in range(n)] for i in range(n)],[],h['perm'],p)
    ns=nullp([[b[1] for b in space]],len(space),p);reduced=[[sum(co[k]*space[k][j] for k in range(len(space)))%p for j in range(4*n)] for co in ns]
    maps=symplectic_solutions(reduced,p);mono+=len(maps)
    for m in maps:
     ds=[d for d in range(p) if {(m[0]*x+d)%p for x in range(K)}==set(range(K))];total+=len(ds)*p
     if ds:wp.add(tuple(h['perm']))
   assert mono*p**n==g['computational_conditioning_projective_order'];assert total*p**(n-2)==g['W_preserving_physical_projective_order'];assert len(wp)==g['W_preserving_permutation_order']==7
   checks[key]={'monomial_lifts':mono,'W_logical_lifts':total,'W_permutation_order':len(wp)}
 return checks

def main():
 start=time.monotonic();src=read('o3_external_spec.json')['constructions'];ba=read('sym1_binary_aut.json');pa=read('sym1_parent_results.json');matched=read('sym1_asbuilt.json');new=read('sym1_external_spec.json');out={};cache=set()
 for ns,r in ba.items():
  n=int(ns);c=next(c for c in src.values() if c['N']==n);ps=automorphisms(support_colors(c),n);assert len(ps)==r['support_order']
  found={}
  for perm in ps:
   sols=symplectic_solutions(local_space(*binary_data(c),perm,2),2)
   if sols:found[tuple(perm)]=set(map(tuple,sols))
  assert found=={tuple(h['perm']):set(map(tuple,h['maps'])) for h in r['automorphisms']}
  assert sum(map(len,found.values()))==r['unsigned_order']
  for h in r['automorphisms']:
   for v,act in zip(h['maps'],h['logical_actions']):verify_logical(c,h['perm'],v,act['pauli_correction'],act['logical_XZ_images'])
  print('binary',n,'complete',r['unsigned_order'],flush=True)
 alt=read('sym1_alternates.json')['13_5']
 ap=automorphisms(support_colors(alt),13)
 assert len(ap)==12 and set(map(tuple,ap))=={tuple(h['perm']) for h in alt['automorphisms']}
 for h in alt['automorphisms']:
  sols=symplectic_solutions(local_space(*binary_data(alt),h['perm'],2),2)
  assert set(map(tuple,sols))==set(map(tuple,h['maps']))
  for vm,ac in zip(h['maps'],h['logical_actions']):verify_logical(alt,h['perm'],vm,ac['pauli_correction'],ac['logical_XZ_images'])
 print('alternate binary 13 complete party order12',flush=True)
 for key,c in src.items():
  n=c['N'];p=c['p'];K=c['K'];m=K.bit_length()-1;result=ame(c,cache);result.update(verify_parent(c,pa[key]));hits=[]
  for bh in ba[str(n)]['automorphisms']:
   perm=bh['perm'];bs=local_space(*prime_data(c),perm,p)
   if not bs:continue
   ps=prime_diagonal(c,perm,bs)
   for bi,act in enumerate(bh['logical_actions']):
    ims=act['logical_XZ_images']
    if any(x[1] for x in ims[:m]) or any(x[0] for x in ims[m:]):continue
    linear=span([x[0] for x in ims[:m]])
    for v,lm in ps:
     for d in range(p):
      aff=[(lm[0]*a+d)%p for a in range(K)]
      if set(aff)==set(range(K)) and all(linear[a]^aff[0]==aff[a] for a in range(K)):hits.append((tuple(perm),bi,tuple(aff)))
  assert set(hits)=={(tuple(h['perm']),h['binary_map_index'],tuple(h['branch_permutation'])) for h in matched[key]['matched_cosets']}
  assert len(hits)==2 and all(h[0]==tuple(range(n)) for h in hits)
  assert matched[key]['local_order']==2**(n-m+1)*p**(n-1)
  # Universal extra reflection acts by a -> K-1-a in both factors.
  assert all(c['branch_labels'][a]^c['branch_labels'][K-1]==c['branch_labels'][K-1-a] for a in range(K))
  result['structured_permutation_order']=1;result['structured_local_projective_order']=matched[key]['local_order'];out[key]=result;print('as built',key,'PASS',flush=True)
 redesign={}
 for key,c in list(new['constructions'].items())+([('family_15_62',new['family_witness'])] if 'family_witness' in new else []):
  r=ame(c,cache);r.update(verify_redesign(c));redesign[key]=r;print('redesign',key,'PASS',r['certified_group_order'],flush=True)
 # Nontrivial negative controls: a wrong algebraic phase and singular local map.
 bad=copy.deepcopy(new['constructions']['13_34']['isometry']);bad['eta_exponent']+=1
 try:spectral_check(bad)
 except AssertionError:pass
 else:raise AssertionError('incorrect phase accepted')
 bad=copy.deepcopy(new['constructions']['15_38']);bad['symmetry_generators'][0]['prime_maps'][:4]=[0]*4
 try:verify_redesign(bad)
 except AssertionError:pass
 else:raise AssertionError('singular generator accepted')
 inventory=verify_inventory(src,pa)
 result={'status':'PASS','generator_inventory_checks':inventory,'arithmetic':'exact integers, rational arithmetic and cyclotomic polynomial quotients; standard library only','as_built':out,'redesigned':redesign,'negative_controls':['wrong cyclotomic phase rejected','singular prime local map rejected'],'wall_seconds':time.monotonic()-start,'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'processes':1}
 (P/'sym1_verification.json').write_text(json.dumps(result,indent=2)+'\n');print('ALL PASS',result['wall_seconds'],'seconds',result['max_rss_kib'],'KiB',flush=True)
if __name__=='__main__':main()
