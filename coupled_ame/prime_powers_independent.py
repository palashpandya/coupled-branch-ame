"""Claude's independent check of the N04 certificates.

Field arithmetic is rebuilt here from the defining polynomials; none of the N04 code is used.

1. Graph AME(n,q): every floor(n/2)-subset A has rank |A| for G[A, A^c] over F_q (A is taken to contain site 0 when
   n is even, which is enough by symmetry of the rank of a submatrix and its transpose).
2. Assembled coupled cells: parent graph AME(N+1,q); distinct field labels; K <= q; binary graph-sector average
   k-uniform, i.e. every nonidentity stabilizer element X^x Z^{Bx} of weight <= k has zero label Walsh sum.
3. The product case split for every d in 3..2000.
"""
import itertools, json, sys
from pathlib import Path

from ._paths import DATA, RESULTS
R = DATA / 'prime_powers'


class Field:
    def __init__(self, p, poly):  # poly: monic, coefficients low -> high, degree m
        self.p, self.m = p, len(poly) - 1
        self.q = p ** self.m
        vec = lambda a: [(a // p ** i) % p for i in range(self.m)]
        num = lambda v: sum(c * p ** i for i, c in enumerate(v))
        self.add = [[num([(x + y) % p for x, y in zip(vec(a), vec(b))]) for b in range(self.q)] for a in range(self.q)]
        self.mul = [[0] * self.q for _ in range(self.q)]
        for a in range(self.q):
            for b in range(self.q):
                prod = [0] * (2 * self.m)
                for i, x in enumerate(vec(a)):
                    for j, y in enumerate(vec(b)):
                        prod[i + j] = (prod[i + j] + x * y) % p
                for d in range(2 * self.m - 1, self.m - 1, -1):  # reduce by t^m = -sum poly[i] t^i
                    c = prod[d]
                    if c:
                        prod[d] = 0
                        for i in range(self.m):
                            prod[d - self.m + i] = (prod[d - self.m + i] - c * poly[i]) % p
                self.mul[a][b] = num(prod[:self.m])
        self.neg = [next(b for b in range(self.q) if self.add[a][b] == 0) for a in range(self.q)]
        self.inv = [None] + [next(b for b in range(self.q) if self.mul[a][b] == 1) for a in range(1, self.q)]
        assert all(self.inv[a] is not None for a in range(1, self.q)), 'polynomial not irreducible'

    def rank(self, M):
        M = [list(r) for r in M]; rk = 0
        for c in range(len(M[0])):
            piv = next((i for i in range(rk, len(M)) if M[i][c]), None)
            if piv is None:
                continue
            M[rk], M[piv] = M[piv], M[rk]
            s = self.inv[M[rk][c]]; M[rk] = [self.mul[s][v] for v in M[rk]]
            for i in range(len(M)):
                if i != rk and M[i][c]:
                    f = self.neg[M[i][c]]
                    M[i] = [self.add[a][self.mul[f][b]] for a, b in zip(M[i], M[rk])]
            rk += 1
        return rk


POLYS = {2: [0, 1], 3: [0, 1], 4: [1, 1, 1], 5: [0, 1], 7: [0, 1], 8: [1, 1, 0, 1], 9: [1, 0, 1]}
PRIME = {2: 2, 3: 3, 4: 2, 5: 5, 7: 7, 8: 2, 9: 3}


def field(q):
    return Field(PRIME[q], POLYS[q])


def graph_ame(G, F):
    n = len(G); k = n // 2
    assert all(G[i][j] == G[j][i] for i in range(n) for j in range(n)) and all(G[i][i] == 0 for i in range(n))
    bad = 0; cuts = 0
    for A in itertools.combinations(range(n), k):
        if n % 2 == 0 and 0 not in A:
            continue
        cuts += 1
        rest = [j for j in range(n) if j not in A]
        if F.rank([[G[i][j] for j in rest] for i in A]) != k:
            bad += 1
    return cuts, bad


def binary_walsh(B, labels, k):
    N = len(B); bad = 0; low = 0
    for x in range(1, 2 ** N):
        xs = [(x >> i) & 1 for i in range(N)]
        z = [sum(B[i][j] * xs[j] for j in range(N)) % 2 for i in range(N)]
        w = sum(1 for i in range(N) if xs[i] or z[i])
        if w <= k:
            low += 1
            # label l flips the sign of X^x Z^{Bx} by (-1)^{l.x}
            if sum((-1) ** bin(l & x).count('1') for l in labels) != 0:
                bad += 1
    return low, bad


def main():
    out = {}
    for q in (3, 4, 5, 7, 8, 9):
        d = json.load(open(R / f'graph_9_{q}.json'))
        G = d.get('matrix') or d['graph']
        out[f'AME(9,{q})'] = graph_ame(G, field(q))
    F9 = field(9)
    for n in (10, 12, 16):
        out[f'parent AME({n},9)'] = graph_ame(json.load(open(R / f'parent_{n}_9.json'))['graph'], F9)
    for N in (9, 11, 15):
        s = json.load(open(R / f'ame_{N}_18.json'))
        assert s['field_polynomial'] == POLYS[9] and s['q'] == 9
        K, labels, fl = s['K'], s['binary_labels'], s['field_labels']
        par = graph_ame(s['prime_power_parent_graph'], F9)
        assert len(set(fl)) == K == len(set(labels)) and K <= 9 and all(0 <= a < 9 for a in fl)
        out[f'AME({N},18) parent'] = par
        out[f'AME({N},18) binary low words, bad'] = binary_walsh(s['binary_graph'], labels, N // 2)
    # corruption controls
    G = [r[:] for r in json.load(open(R / 'graph_9_4.json'))['matrix']]; G[0][1] = G[1][0] = (G[0][1] + 1) % 4
    out['control: perturbed AME(9,4)'] = graph_ame(G, field(4))
    s = json.load(open(R / 'ame_9_18.json'))
    out['control: AME(9,18) duplicate label'] = binary_walsh(s['binary_graph'], s['binary_labels'][:3] + [s['binary_labels'][0]], 4)
    # product split
    def factor(n):
        f, p = {}, 2
        while p * p <= n:
            while n % p == 0:
                f[p] = f.get(p, 0) + 1; n //= p
            p += 1
        if n > 1: f[n] = f.get(n, 0) + 1
        return f
    def covered_odd(m):  # products of AME(9,p^a): p^a in {3,5,7} explicit, >= 8 RS
        return all(p ** a in (3, 5, 7) or p ** a >= 8 for p, a in factor(m).items())
    fails = []
    for d in range(3, 2001):
        e = 0; m = d
        while m % 2 == 0: m //= 2; e += 1
        if e == 0: ok = covered_odd(m)
        elif e == 1:
            if m % 3 == 0: ok = covered_odd(m // 3) or m == 3        # AME(9,6) x odd
            else: ok = any(p >= 5 and covered_odd(m // p) for p in factor(m)) if m > 1 else False
        else: ok = covered_odd(m)  # 2^e in {4, 8} explicit or >= 16 RS
        if not ok: fails.append(d)
    out['product split fails in 3..2000'] = fails
    print(json.dumps(out, indent=1))
    ok = all(v[1] == 0 for k, v in out.items() if not k.startswith('control') and isinstance(v, tuple))
    ok &= out['control: perturbed AME(9,4)'][1] > 0 and out['control: AME(9,18) duplicate label'][1] > 0 and not fails
    assert ok, out
    (RESULTS/'prime_powers_independent.json').write_text(json.dumps(out,indent=2)+'\n')
    print('ALL PASS')


if __name__ == '__main__':
    main()
