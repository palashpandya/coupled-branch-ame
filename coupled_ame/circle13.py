"""Additional p<N construction: Hontarenko--Zyczkowski, S11/S81, q=13.

Build the 16-party prime parent independently and certify all its cuts.
Also instantiate the requested d=38,46 examples with the Cauchy parents.
"""
import copy,json,random
from .construction import HERE,save,cuts,parent_graph
from .codes import modrank

q=13;nu=2 # theta^2=2, a quadratic nonresidue modulo 13
def add(x,y):return ((x%q+y%q)%q)+q*((x//q+y//q)%q)
def neg(x):return (-x%q)+q*((- (x//q))%q)
def sub(x,y):return add(x,neg(y))
def mul(x,y):
    a,b=x%q,x//q;c,d=y%q,y//q
    return ((a*c+nu*b*d)%q)+q*((a*d+b*c)%q)
def conj(x):return x%q+q*((-(x//q))%q)
def norm(x):return mul(x,conj(x))
def inv(x):
    assert x
    return mul(conj(x),pow(norm(x),-1,q))
def div(x,y):return mul(x,inv(y))

def circle():
    # Explicit field checks prevent convention errors from entering the matrix.
    assert pow(nu,(q-1)//2,q)==q-1
    assert all(mul(x,inv(x))==1 for x in range(1,q*q))
    U=[x for x in range(1,q*q) if norm(x)==1]
    H=sorted({mul(x,x) for x in U});assert len(H)==7
    excluded={0,q-1,2,3*pow(2,-1,q)%q}
    u=next(x for x in range(1,q*q) if norm(x)==q-1 and add(x,conj(x)) not in excluded)
    t=add(u,conj(u));b=next(x for x in range(1,q*q) if norm(x)==(-2*(1+t))%q)
    sigma=add(1,u);a=neg(div(mul(b,conj(sigma)),conj(b)));P0=add(1,mul(2,u))
    B=[[a]+[b]*7]+[[b]+[div(mul(2,add(mul(P0,y),x)),add(x,y)) for y in H] for x in H]
    def total(xs):
        s=0
        for x in xs:s=add(s,x)
        return s
    herm=[[total(mul(x,conj(y)) for x,y in zip(r,s)) for s in B] for r in B]
    assert herm==[[q-1 if i==j else 0 for j in range(8)] for i in range(8)]
    G=[[int(i==j) for j in range(8)]+B[i] for i in range(8)]
    rows=[[mul(a,x) for x in row] for row in G for a in (1,q)]
    X=[[x%q for x in row] for row in rows];Z=[[x//q for x in row] for row in rows]
    assert all(sum(X[i][k]*Z[j][k]-Z[i][k]*X[j][k] for k in range(16))%q==0 for i in range(16) for j in range(16))
    rng=random.Random(1316)
    for trial in range(10000):
        mask=rng.getrandbits(16)
        M=[[Z[i][j] if mask>>j&1 else X[i][j] for j in range(16)]+[(-X[i][j])%q if mask>>j&1 else Z[i][j] for j in range(16)] for i in range(16)]
        if modrank([r[:16] for r in M],q)==16:break
    else:raise RuntimeError('graph chart absent')
    for j in range(16):
        i=next(i for i in range(j,16) if M[i][j]);M[j],M[i]=M[i],M[j]
        v=pow(M[j][j],-1,q);M[j]=[x*v%q for x in M[j]]
        for i in range(16):
            if i!=j:
                v=M[i][j];M[i]=[(x-v*y)%q for x,y in zip(M[i],M[j])]
    A=[r[16:] for r in M];assert all(A[i][j]==A[j][i] for i in range(16) for j in range(16))
    diagonal=[A[i][i] for i in range(16)]
    for i in range(16):A[i][i]=0
    return A,dict(source='https://arxiv.org/html/2609.11796v1#S11',equation='S81',field='GF(13)[theta]/(theta^2-2); integer a+13*b encodes a+b*theta',H=H,u=u,t=t,b=b,a=a,P0=P0,B=B,hermitian_product=herm,local_Fourier_mask=mask,removed_diagonal=diagonal)
