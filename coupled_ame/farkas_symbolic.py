from ._paths import ROOT
# Independent check of manuscript Eq. (farkas): own derivation of enumerator transforms.
import sympy as sp
N,R=13,8
a=[sp.Integer(1)]+[0]*6+list(sp.symbols('a7:14'))
x,y=sp.symbols('x y')
A=lambda X,Y: sum(a[j]*X**(N-j)*Y**j for j in range(N+1))
bp=sp.Poly(sp.expand(A(x+3*y,x-y)/2**N),x,y); sp_=sp.Poly(sp.expand(A(x+3*y,y-x)/2**N),x,y)
b=[bp.coeff_monomial(x**(N-j)*y**j) for j in range(N+1)]
s=[sp_.coeff_monomial(x**(N-j)*y**j) for j in range(N+1)]
D=lambda j: R*b[j]-a[j]
D10c=sum(sp.binomial(N-j,10-j)*(R*a[j]-b[j]) for j in range(11))
lhs=292864*s[0]+8192*D(1)+133120*s[1]+3584*D(2)+39936*s[2]+1536*D(3)+13312*s[3]+D10c
assert sp.simplify(lhs) == -3328
print('[PASS] independent symbolic identity =', sp.simplify(lhs))
