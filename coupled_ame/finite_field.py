"""Polynomial-basis finite fields; exact checker arithmetic, no search imports."""
from itertools import combinations
class Field:
 def __init__(self,p,poly):
  self.p=p;self.poly=poly;self.e=len(poly)-1;self.q=p**self.e
  self.digits=[[x//p**i%p for i in range(self.e)] for x in range(self.q)]
  self.add=[[sum(((a+b)%p)*p**i for i,(a,b) in enumerate(zip(x,y))) for y in self.digits] for x in self.digits]
  self.neg=[sum((-a%p)*p**i for i,a in enumerate(x)) for x in self.digits]
  self.mul=[[self.product(x,y) for y in self.digits] for x in self.digits]
  self.inv=[0]+[next(y for y in range(1,self.q) if self.mul[x][y]==1) for x in range(1,self.q)]
 def product(self,x,y):
  p=self.p;e=self.e;t=[0]*(2*e-1)
  for i,a in enumerate(x):
   for j,b in enumerate(y):t[i+j]=(t[i+j]+a*b)%p
  for j in range(2*e-2,e-1,-1):
   for i in range(e):t[j-e+i]=(t[j-e+i]-t[j]*self.poly[i])%p
  return sum(t[i]*p**i for i in range(e))
 def pow(self,x,n):
  y=1
  while n:
   if n&1:y=self.mul[y][x]
   x=self.mul[x][x];n//=2
  return y
 def sum(self,xs):
  z=0
  for x in xs:z=self.add[z][x]
  return z
 def rank(self,a):
  a=[r[:] for r in a];r=0
  for j in range(len(a[0]) if a else 0):
   i=next((i for i in range(r,len(a)) if a[i][j]),None)
   if i is None:continue
   a[r],a[i]=a[i],a[r];a[r]=[self.mul[x][self.inv[a[r][j]]] for x in a[r]]
   for i in range(len(a)):
    if i!=r:
     z=a[i][j];a[i]=[self.add[x][self.neg[self.mul[z][y]]] for x,y in zip(a[i],a[r])]
   r+=1
  return r
 def cuts(self,g,k=None):
  n=len(g);k=n//2 if k is None else k
  assert all(len(row)==n for row in g)
  assert all(g[i][i]==0 and all(g[i][j]==g[j][i] and 0<=g[i][j]<self.q for j in range(n)) for i in range(n))
  out=[]
  for a in combinations(range(n),k):
   b=[i for i in range(n) if i not in a];rank=self.rank([[g[i][j] for j in b] for i in a]);assert rank==k,('bad cut',a,rank)
   out.append(list(a))
  return dict(PASS=True,N=n,q=self.q,k=k,cuts=len(out))
FIELDS={2:(2,[0,1]),3:(3,[0,1]),4:(2,[1,1,1]),5:(5,[0,1]),7:(7,[0,1]),8:(2,[1,1,0,1]),9:(3,[1,0,1]),81:(3,[2,1,0,0,1])}
def field(q):return Field(*FIELDS[q])
