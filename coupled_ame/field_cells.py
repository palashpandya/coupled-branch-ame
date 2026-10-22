"""Exact assembled-cell check, including field and binary label constraints."""
from .finite_field import field
def check(a):
 n=a['N'];k=n//2;g=a['binary_graph'];labs=a['binary_labels'];pl=a['field_labels'];K=a['K']
 assert K==len(labs)==len(pl) and len(set(labs))==K and len(set(pl))==K
 assert K<=9 and all(0<=l<9 for l in pl) and all(0<=l<1<<n for l in labs)
 assert all(len(row)==n for row in g) and all(g[i][i]==0 and all(g[i][j]==g[j][i] and g[i][j] in [0,1] for j in range(n)) for i in range(n))
 words=[0]
 for i,row in enumerate(g):
  w=(1<<i)|sum(v<<(n+j) for j,v in enumerate(row));words += [u^w for u in words]
 low=0
 for w in words[1:]:
  x=w&((1<<n)-1);support=x|(w>>n)
  if support.bit_count()<=k:
   assert sum((-1)**((x&l).bit_count()%2) for l in labs)==0;low+=1
 assert len(a['prime_power_parent_graph'])==n+1
 p=field(9).cuts(a['prime_power_parent_graph'])
 return dict(PASS=True,N=n,K=K,low_binary_words=low,parent_cuts=p['cuts'])
