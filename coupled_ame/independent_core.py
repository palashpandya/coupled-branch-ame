"""Claude's independent verification of the O3 coupled-branch AME(N,2p) constructions, from o3_external_spec.json
only (no O3 code imported).

For each construction:
 (1) exact binary check: the branch labels form a linear space L of size K (closure under XOR, K distinct).
     Average_a Z^l_a |B><B| Z^l_a = 2^-N sum_{h in L-perp} g^h with g^h ~ X^h Z^(Bh), so the average is
     floor(N/2)-uniform iff every nonzero h in L-perp has |supp h  U  supp Bh| > floor(N/2). Enumerate L-perp exactly.
 (2) numerical binary check (N <= 15): build u_a(b) = 2^-N/2 (-1)^(q_B(b) + l_a.b) and test every floor(N/2)-party
     marginal of the average against I/2^k; the runner selects a declared sample or all cuts.
 (3) exact prime parent: every balanced cut block G[A, A^c] of the (N+1)-vertex graph has full rank (N+1)/2 over
     GF(p), own modular elimination; and K <= p (distinct conditioning values).
Together with the coupling lemma (Tr_{A^c}|v_a><v_b| = delta_ab I/p^k from (3)) these give AME(N,2p).
"""
import itertools as it
import json
import sys
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parents[1] / "data"


def rank_mod(rows, p):
    rows = [[x % p for x in r] for r in rows]
    rank, ncol = 0, len(rows[0])
    for c in range(ncol):
        piv = next((i for i in range(rank, len(rows)) if rows[i][c]), None)
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        inv = pow(rows[rank][c], p - 2, p)
        rows[rank] = [x * inv % p for x in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][c]:
                f = rows[i][c]
                rows[i] = [(x - f * y) % p for x, y in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def binary_exact(c):
    N, K = c["N"], c["K"]
    k = N // 2
    B = c["binary_graph"]
    L = set(c["branch_labels"])
    closed = len(L) == K and all((a ^ b) in L for a in L for b in L)
    Bmask = [sum(B[i][j] << j for j in range(N)) for i in range(N)]  # row i as a bit mask over parties j
    minw, count = N + 1, 0
    for h in range(1, 2 ** N):
        if any(bin(h & l).count("1") % 2 for l in c["binary_label_generators"]):
            continue  # h not in L-perp
        bh = 0
        for i in range(N):
            if bin(Bmask[i] & h).count("1") % 2:
                bh |= 1 << i
        count += 1
        minw = min(minw, bin(h | bh).count("1"))
    return dict(labels_linear_space=closed, Lperp_nonzero=count, expected_Lperp_nonzero=2 ** N // K - 1,
                min_weight=minw, k=k, binary_k_uniform=closed and count == 2 ** N // K - 1 and minw > k)


def _u(c):
    N = c["N"]
    idx = np.arange(2 ** N)
    bits = (idx[:, None] >> np.arange(N)) & 1  # bits[:, i] = party i
    B = np.array(c["binary_graph"])
    q = (np.einsum("xi,ij,xj->x", bits, np.triu(B, 1), bits)) % 2
    us = []
    for l in c["branch_labels"]:
        lb = (l >> np.arange(N)) & 1
        us.append(((-1.0) ** ((q + bits @ lb) % 2)) / 2 ** (N / 2))
    # tensor axis j (C order, most significant first) is party N-1-j; all k-subsets are tested, so labels are moot
    return np.array(us).reshape((len(us),) + (2,) * N)


_U = {}


def _marg(args):
    key, A = args
    U = _U[key]
    N = U.ndim - 1
    Bc = [i for i in range(N) if i not in A]
    M = U.transpose([0] + [1 + i for i in A] + [1 + i for i in Bc]).reshape(U.shape[0], 2 ** len(A), -1)
    rho = np.einsum("aij,akj->ik", M, M) / U.shape[0]
    return float(np.linalg.norm(rho - np.eye(2 ** len(A)) / 2 ** len(A)))


def _cut(args):
    G, A, p = args
    Bc = [j for j in range(len(G)) if j not in A]
    return rank_mod([[G[i][j] for j in Bc] for i in A], p) == len(A)
