# Reference sources and attribution

This directory contains reference metadata only. No third-party PDFs, source code,
README text or datasets are vendored. Linked material retains its original licence.
The exact generated data elsewhere in this repository have the licence described
in `LICENSE-DATA.md`.

## Coupling and parent constructions (article Table I)

- Shi, Zhang, Zhao and Li, [arXiv:2608.01011v1](https://arxiv.org/abs/2608.01011v1),
  Eqs.31–38: two Steane logical branches and odd-dimensional graph branches;
  binary/odd cancellation depends on the triple (non-Fano/Fano).
- Atlas, [Oqp35.lean at 15e4b3a7584e](https://github.com/niketp03/atlas-fc-verified/blob/15e4b3a7584e218cec531aeaf71cce72a8a9ecb1/AtlasFCSolutions/Oqp35.lean):
  four-branch AME(9,10), nine-cycle binary states and ten-site quinary parent;
  all-cut quinary cancellation. Separate parent attribution not supplied in the inspected file.
- Kitamura, [ame-11-10-lean at 6b7d009a4397](https://github.com/KitaKen1/ame-11-10-lean/tree/6b7d009a43970587a3386b690221bec4339ce271):
  two-branch AME(11,10), five-uniform twelve-qubit parent and BB AME(12,5).
  The README reports a completed Lean proof and marks its explanatory prose as
  AI-generated, with Lean authoritative. Neither Lean project is rebuilt here.
- Bevins and Bidav, [arXiv:2608.05781v2](https://arxiv.org/abs/2608.05781v2): parent/code source.
- Hontarenko and Życzkowski, [arXiv:2609.11796v1](https://arxiv.org/abs/2609.11796v1),
  supplement S11, TheoremS7, Eq.S81: the circle parent used at(15,26).
  AME(2q,q) in their title means 2q parties, not composite local dimension.

## Code seeds

- Grassl's [GF(4), length15, dimension6 entry](https://www.codetables.de/BKLC/BKLC.php?q=4&n=15&k=6).
- Grassl's [GF(4), length17, dimension6 entry](https://www.codetables.de/BKLC/BKLC.php?q=4&n=17&k=6),
  including the length18 quasicyclic [18,6,10] seed.

Parameters precede this work. No equivalence to an unread classical original is claimed.

## Background, bounds and asymptotic context

- Scott, [quant-ph/0310137](https://arxiv.org/abs/quant-ph/0310137), Sec.III: binary AME bounds.
- Huber, Gühne and Siewert, [1608.06228v3](https://arxiv.org/abs/1608.06228v3), Observation2: no AME(7,2).
- Helwig et al., [1204.2289](https://arxiv.org/abs/1204.2289), Theorem2: secret sharing.
- Helwig and Cui, [1306.2536v1](https://arxiv.org/abs/1306.2536v1), Theorem2: arrays/codes to AME.
- Huber and Grassl, [1907.07733v2](https://arxiv.org/abs/1907.07733v2): uniform subspaces and codes.
- Antipin, [2301.03120v1](https://arxiv.org/abs/2301.03120v1), Lemma1: isometric encoding.
- Rains, [quant-ph/9611001v2](https://arxiv.org/abs/quant-ph/9611001v2): quantum shadow enumerators.
- Huber et al., [1708.06298](https://arxiv.org/abs/1708.06298): shadow/MacWilliams bounds.
- Keevash, [1802.05900v1](https://arxiv.org/abs/1802.05900v1), Definition1.6/Theorem1.7:
  partite designs; combined with the array construction, this implies eventual
  AME existence for fixed N and sufficiently large integer dimension. It supplies
  no numerical threshold for the finite cells here.

The AME(16,11) parent parameters are recorded by the [Huber–Wyderka table](https://huberfe.github.io/table.html),
citing [Grassl–Rötteler, Quantum MDS Codes over Small Fields](https://arxiv.org/abs/1502.05267).
The explicit bordered-circulant matrix in `parent11_certificate.json` was found by our
deterministic local search and is reconstructed and checked by `parent11.py`;
its inclusion does not assert new existence of the prime parent.


Kitamura AME(9,6): pinned source metadata in `data/kitamura96-source.json`;
no external matrices or Lean files redistributed because licence permission
was not established offline. See `docs/R10-prime-powers.md` for user retrieval
and the hash-checked structured verifier. No Lean build.
