"""Exact GF(4), binary symplectic, and prime-field helpers. No network required."""
from collections import Counter
from itertools import product

MUL = [[0,0,0,0],[0,1,2,3],[0,2,3,1],[0,3,1,2]]

def pmul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]^=MUL[x][y]
    return c

def pdiv(a,b):
    a=a[:]
    q=[0]*max(1,len(a)-len(b)+1)
    for i in range(len(a)-len(b),-1,-1):
        v=MUL[a[i+len(b)-1]][[0,1,3,2][b[-1]]]
        q[i]=v
        for j,x in enumerate(b): a[i+j]^=MUL[v][x]
    while len(a)>1 and not a[-1]: a.pop()
    return q,a

def factors(n):
    remaining=[1]+[0]*(n-1)+[1]
    out=[]
    for d in range(1,n+1):
        if len(remaining)==1: break
        # For the small requested lengths factors have degree at most six.
        if d>6: raise ValueError('unfactored polynomial')
        for cs in product(range(4),repeat=d):
            if not cs[0]: continue
            f=list(cs)+[1]; e=0
            while len(remaining)>=len(f):
                q,r=pdiv(remaining,f)
                if r!=[0]: break
                remaining=q; e+=1
            if e: out.append((f,e))
    return out

def cyclic_generators(n,dim):
    fs=factors(n)
    for es in product(*(range(e+1) for _,e in fs)):
        if sum(e*(len(f)-1) for e,(f,_) in zip(es,fs))!=n-dim: continue
        g=[1]
        for e,(f,_) in zip(es,fs):
            for _ in range(e): g=pmul(g,f)
        yield g, [[0]*i+g+[0]*(dim-1-i) for i in range(dim)]

def gf4_words(G):
    w=[[0]*len(G[0])]
    for row in G:
        w=[ [x^MUL[a][y] for x,y in zip(v,row)] for a in range(4) for v in w]
    return w

def hermitian(G):
    return [[xor(MUL[a][MUL[b][b]] for a,b in zip(x,y)) for y in G] for x in G]

def xor(xs):
    a=0
    for x in xs:a^=x
    return a

def pack(row):
    # GF4 1 -> X, omega -> Z, omega+1 -> Y; coordinate i is bit i.
    n=len(row)
    return sum((a&1)<<i for i,a in enumerate(row)) | sum((a>>1)<<(n+i) for i,a in enumerate(row))

def unpack(w,n):return [((w>>i)&1)+2*((w>>(n+i))&1) for i in range(n)]

def gf4_binary(G):
    return [pack([MUL[a][x] for x in row]) for row in G for a in (1,2)]

def basis(words):
    piv={}
    for w in words:
        while w:
            i=w.bit_length()-1
            if i in piv:w^=piv[i]
            else:piv[i]=w;break
    return [piv[i] for i in sorted(piv,reverse=True)]

def span(G):
    out=[0]
    for g in G:out += [v^g for v in out]
    return out

def weight(w,n):return ((w|(w>>n))&((1<<n)-1)).bit_count()

def symp(a,b,n):
    mask=(1<<n)-1
    return (((a&mask)&(b>>n))^((b&mask)&(a>>n))).bit_count()%2

def nullspace(rows,n):
    rows=rows[:];piv=[];r=0
    for j in range(n):
        t=next((i for i in range(r,len(rows)) if rows[i]>>j&1),None)
        if t is None:continue
        rows[r],rows[t]=rows[t],rows[r]
        for i in range(len(rows)):
            if i!=r and rows[i]>>j&1:rows[i]^=rows[r]
        piv.append(j);r+=1
    return [(1<<j)|sum(((rows[i]>>j)&1)<<p for i,p in enumerate(piv)) for j in range(n) if j not in piv]

def certify(G,n):
    assert len(basis(G))==len(G)
    assert all(not symp(x,y,n) for x in G for y in G)
    h=Counter(weight(w,n) for w in span(G))
    return dict(N=n,binary_rank=len(G),K=2**(n-len(G)),minimum_weight=min(w for w in h if w),weight_enumerator=dict(sorted(h.items())),generators=G,pauli_rows=[''.join('IXZY'[a] for a in unpack(g,n)) for g in G])

def modrank(a,p):
    a=[r[:] for r in a];m=len(a);r=0
    for j in range(len(a[0]) if m else 0):
        t=next((i for i in range(r,m) if a[i][j]%p),None)
        if t is None:continue
        a[r],a[t]=a[t],a[r]
        inv=pow(a[r][j]%p,-1,p);a[r]=[(v*inv)%p for v in a[r]]
        for i in range(r+1,m):
            if a[i][j]%p:
                v=a[i][j];a[i]=[(x-v*y)%p for x,y in zip(a[i],a[r])]
        r+=1
        if r==m:break
    return r
