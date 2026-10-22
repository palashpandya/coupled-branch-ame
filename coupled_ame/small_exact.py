"""Independent exact checker. No imports from search or orchestration modules."""
import argparse,json,itertools,collections
from pathlib import Path

def rank(a,p):
    a=[list(row) for row in a];r=0
    for j in range(len(a[0]) if a else 0):
        z=next((i for i in range(r,len(a)) if a[i][j]%p),None)
        if z is None:continue
        a[r],a[z]=a[z],a[r];inv=pow(a[r][j]%p,-1,p)
        a[r]=[x*inv%p for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                f=a[i][j]%p;a[i]=[(x-f*y)%p for x,y in zip(a[i],a[r])]
        r+=1
    return r

def graph_check(g,p,k=None):
    n=len(g);k=n//2 if k is None else k
    assert all(len(row)==n for row in g)
    assert all(g[i][i]==0 and all(g[i][j]==g[j][i] and 0<=g[i][j]<p for j in range(n)) for i in range(n))
    cuts=0
    for a in itertools.combinations(range(n),k):
        b=[i for i in range(n) if i not in a]
        assert rank([[g[i][j] for j in b] for i in a],p)==k,('bad cut',a)
        cuts+=1
    return cuts

class Extension:
    # Polynomial pairs, independent of C++ lookup tables.
    def __init__(self,p,nu):
        self.p,self.nu=p,nu
        assert pow(nu,(p-1)//2,p)==p-1
    def dec(self,x):return x%self.p,x//self.p
    def add(self,x,y):
        a,b=self.dec(x);c,d=self.dec(y);return (a+c)%self.p+self.p*((b+d)%self.p)
    def neg(self,x):
        a,b=self.dec(x);return (-a)%self.p+self.p*((-b)%self.p)
    def conj(self,x):
        a,b=self.dec(x);return a+self.p*((-b)%self.p)
    def mul(self,x,y):
        a,b=self.dec(x);c,d=self.dec(y);return (a*c+self.nu*b*d)%self.p+self.p*((a*d+b*c)%self.p)
    def inv(self,x):
        assert x
        n=self.mul(x,self.conj(x));assert 0<n<self.p
        return self.mul(self.conj(x),pow(n,-1,self.p))
    def det(self,a):
        # Recursive Laplace expansion: independent of search's Gaussian elimination.
        n=len(a)
        if n==0:return 1
        if n==1:return a[0][0]
        value=0
        for j,x in enumerate(a[0]):
            if not x:continue
            term=self.mul(x,self.det([r[:j]+r[j+1:] for r in a[1:]]))
            value=self.add(value,self.neg(term) if j%2 else term)
        return value

def parent(rec):
    p,nu=rec['p'],rec['nu'];f=Extension(p,nu);b=rec['B'];m=len(b);n=2*m
    assert all(f.mul(x,f.inv(x))==1 and f.conj(f.conj(x))==x for x in range(1,p*p))
    assert 1<=m<=8 and all(len(r)==m and all(type(x)==int and 0<=x<p*p for x in r) for r in b)
    for i in range(m):
        for j in range(m):
            s=0
            for x,y in zip(b[i],b[j]):s=f.add(s,f.mul(x,f.conj(y)))
            assert s==((p-1) if i==j else 0),'Hermitian product'
    # For m<=6 check all orders by a separately implemented elimination below,
    # and cross-check low orders using Laplace. V01 m8 also stays inexpensive.
    def det2(mat):
        mat=[row[:] for row in mat];out=1
        for c in range(len(mat)):
            row=next((r for r in range(c,len(mat)) if mat[r][c]),None)
            if row is None:return 0
            if row!=c:mat[c],mat[row]=mat[row],mat[c];out=f.neg(out)
            out=f.mul(out,mat[c][c]);q=f.inv(mat[c][c])
            for r in range(c+1,len(mat)):
                a=f.mul(mat[r][c],q)
                mat[r]=[f.add(x,f.neg(f.mul(a,y))) for x,y in zip(mat[r],mat[c])]
        return out
    counts={}
    for size in range(1,m+1):
        cnt=0
        for rr in itertools.combinations(range(m),size):
            for cc in itertools.combinations(range(m),size):
                mat=[[b[i][j] for j in cc] for i in rr];v=det2(mat);assert v,'zero minor'
                if size<=3:assert v==f.det(mat)
                cnt+=1
        counts[size]=cnt
    rows=[[int(i==j) for j in range(m)]+b[i] for i in range(m)]
    expanded=[[f.mul(s,x) for x in row] for row in rows for s in (1,p)]
    x=[[v%p for v in row] for row in expanded];z=[[v//p for v in row] for row in expanded]
    assert all(sum(x[i][l]*z[j][l]-z[i][l]*x[j][l] for l in range(n))%p==0 for i in range(n) for j in range(n))
    for mask in range(1<<n):
        t=[[z[i][j] if mask>>j&1 else x[i][j] for j in range(n)]+[(-x[i][j])%p if mask>>j&1 else z[i][j] for j in range(n)] for i in range(n)]
        if rank([r[:n] for r in t],p)==n:break
    else:raise AssertionError('no graph chart')
    for j in range(n):
        r=next(i for i in range(j,n) if t[i][j]);t[j],t[r]=t[r],t[j]
        inv=pow(t[j][j],-1,p);t[j]=[v*inv%p for v in t[j]]
        for i in range(n):
            if i!=j:
                a=t[i][j];t[i]=[(v-a*w)%p for v,w in zip(t[i],t[j])]
    g=[r[n:] for r in t];diag=[g[i][i] for i in range(n)]
    for i in range(n):g[i][i]=0
    cuts=graph_check(g,p)
    return dict(PASS=True,p=p,nu=nu,B=b,graph=g,minor_counts=counts,cut_count=cuts,Fourier_mask=mask,removed_diagonal=diag)

def code(rec,require=True):
    n,r,d=rec['N'],rec['rank'],rec['distance'];g=rec['generators'];assert len(g)==r and all(type(v)==int and 0<v<1<<(2*n) for v in g)
    mask=(1<<n)-1
    def pair(a,b):return (((a&mask)&(b>>n)).bit_count()+((a>>n)&(b&mask)).bit_count())%2
    assert all(pair(a,b)==0 for a in g for b in g),'noncommuting'
    assert rank([[(v>>i)&1 for i in range(2*n)] for v in g],2)==r,'dependent'
    hist=collections.Counter()
    # Compute each word from its coefficient bits, not the search's incremental span.
    for c in range(1<<r):
        w=0
        for i in range(r):
            if c>>i&1:w^=g[i]
        hist[((w|(w>>n))&mask).bit_count()]+=1
    minimum=min(w for w in hist if w)
    if require:assert minimum>=d,('low weight',minimum,d)
    return dict(PASS=True,N=n,rank=r,minimum_weight=minimum,weight_enumerator=dict(hist),K=2**(n-r),signed_generators='independent Hermitian i^popcount(x&z) X^x Z^z, each +1')

def assembled(rec):
    n,p=rec['N'],rec['p'];k=n//2;g=rec['binary_graph'];labels=rec['binary_labels'];prime=rec['prime_labels'];K=len(labels)
    assert len(g)==n and K==len(prime) and K<=p and len(set(prime))==K and all(0<=a<p for a in prime)
    assert all(len(r)==n and g[i][i]==0 for i,r in enumerate(g))
    assert all(g[i][j]==g[j][i] and g[i][j] in (0,1) for i in range(n) for j in range(n))
    assert all(type(l)==int and 0<=l<1<<n for l in labels)
    count=0
    for x in range(1,1<<n):
        z=0
        for j in range(n):
            if sum(g[i][j] for i in range(n) if x>>i&1)%2:z|=1<<j
        if (x|z).bit_count()<=k:
            assert sum((-1)**((x&lab).bit_count()%2) for lab in labels)==0,'nonuniform binary average'
            count+=1
    assert len(rec['prime_parent_graph'])==n+1
    cuts=graph_check(rec['prime_parent_graph'],p)
    return dict(PASS=True,N=n,p=p,K=K,binary_low_words_checked=count,parent_cuts=cuts,normalization='equal normalized orthogonal prime branches; 1/sqrt(K)',proof='condition reference vertex 0; compare all reference+k-site blocks; binary Walsh cancellation; local digit p*b+y')

def extensions(rec):
    n=rec['N'];g=rec['base_generators'];q=rec['quotient_basis'];mask=(1<<n)-1
    base=[0]
    for v in g:base += [w^v for w in base]
    quotient=[0]
    for v in q:quotient += [w^v for w in quotient]
    assert len(set(base))==2048 and len(set(quotient))==4096
    hist=collections.Counter()
    for v in quotient[1:]:
        w=min((((v^b)|((v^b)>>n))&mask).bit_count() for b in base)
        hist[w]+=1
    assert dict(hist)=={int(k):v for k,v in rec['coset_minimum_histogram'].items()}
    assert max(hist)<9
    # Whole centralizer quotient: check independence jointly, symplectic centrality.
    assert rank([[(v>>i)&1 for i in range(2*n)] for v in g+q],2)==23
    assert all(((((a&mask)&(b>>n)).bit_count()+((a>>n)&(b&mask)).bit_count())%2)==0 for a in g for b in g+q)
    return dict(PASS=True,cosets=len(quotient)-1,histogram=dict(hist))

def main():
    a=argparse.ArgumentParser();a.add_argument('kind',choices=['parent','code','assembled','extensions']);a.add_argument('input');a.add_argument('--output');ns=a.parse_args()
    try:
        out=globals()[ns.kind](json.loads(Path(ns.input).read_text()))
    except Exception as e:
        print(json.dumps(dict(PASS=False,error=str(e))));return 1
    if ns.output:Path(ns.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out if not ns.output else {'PASS':True,'output':ns.output}));return 0
if __name__=='__main__':raise SystemExit(main())
