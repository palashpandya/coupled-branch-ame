# Coupled-branch AME states in dimensions twice a prime power

[![code: MIT](https://img.shields.io/badge/code-MIT-blue)](LICENSE)
[![data: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey)](LICENSE-DATA.md)

Companion code and data for the article

> **Explicit absolutely maximally entangled states in dimensions twice a prime power**
> In preparation, 2026; the publication reference and final article author list will be added when confirmed.

**Author / repository maintainer.** Palash Pandya<br>
Center for Theoretical Physics, Polish Academy of Sciences, Aleja Lotników 32/46, 02-668 Warsaw, Poland<br>
Center for Quantum-Enabled Computing, Center for Theoretical Physics, Polish Academy of Sciences, Warsaw, Poland<br>
Contact: ppandya@cft.edu.pl · GitHub [@palashpandya](https://github.com/palashpandya)

This repository contains data and verification code, **not the manuscript**. Version **0.1 is a pre-release**;
no public release, tag, permanent identifier or archive is asserted.

An AME(N,d) state is a pure state whose reductions to any floor(N/2) parties are maximally mixed.
Here a coherent sum pairs binary branches with conditioned finite-field AME branches. The binary
average supplies local uniformity and the odd factor removes interference between branch labels.

The constructions give AME(N,2q) for N=9,11,13,15,17 and every odd prime power q≥5,5,17,9,67, respectively.
N9 and N11 retain Atlas’s K4 and Kitamura’s K2 binary branches; p5 uses Atlas’s parent and the
Bevins–Bidav parent used by Kitamura. At p7 we supply explicit GF49 parents; p≥11 uses Cauchy,
including the extended N11,p11 case.
The fifteen-party family uses one rank8 binary ingredient with a GF121 Hermitian parent at p11,
the HZ circle parent at p13, and Cauchy parents for p≥17. For N13 and N17, the thresholds
are set by branch capacity K≤p (K16 and K64), not by the availability of prime parents.
The eight N9/N11 cells at p5,7,11,13 are in `data/small_families_spec.json`.
The nine stored N≥13 cells are (13,34), (13,38), (13,46), (15,22), (15,26), (15,34), (15,38), (15,46), (17,134).
Branch isometries also give the cyclic subgroups in Table IV, including AME(15,62) and a C15 family
for every prime p≡1 (mod 15).

The contribution is the explicit small binary ingredients, effective prime-power thresholds, exact certificates,
and symmetric realizations. Coupling has precedents in Shi–Zhang–Zhao–Li, Atlas and Kitamura; Bevins–Bidav
and Hontarenko–Życzkowski supply parent/code constructions. Publication priority remains unestablished; no new priority audit is asserted for the enlarged family. Neither a new coupling principle nor first eventual existence is claimed.

## Results and how they are established

Numbers and labels refer to the article draft of 22 October 2026. Full paths and evidence boundaries
are in [docs/CLAIM_MAP.md](docs/CLAIM_MAP.md). Verifier filenames below refer to `coupled_ame/`.
**Exact** means finite integer/rational/finite-field/cyclotomic verification; analytic family statements
also require the indicated written proof. **Numerical** means corroboration, not proof. **Cited** means
a written argument or external source: `inventory.py` only checks its catalogue/provenance, not the theorem.

| # | Statement | Paper | Script | Status |
|---|---|---|---|---|
| 1 | Twenty-three coupled cells are AME; 142,226 oriented parent cuts | Thm. I.1; Table II | `o3_verify.py`, `independent.py`, `reconstruct.py`, `small_families.py`, `n7.py`, `prime_powers.py` | exact |
| 2 | Every odd prime power q≥5,5,17,9,67 for N9,11,13,15,17; four parent constructions at N15 | Thm. I.1; Lem. IV.1 (`lem:cauchy`) | `reconstruct.py`, `inventory.py` | exact finite inputs; cited analytic Cauchy proof |
| 3 | Weighted coupling, conditioned-parent identity and stabilizer-projector criterion | Prop. II.1, Lem. II.2, Prop. III.1 | `o3_verify.py`, `inventory.py` | exact finite inputs; cited partial-trace/Pauli arguments |
| 4 | Binary ranks16,8,64 and minimum stabilizer weights7,8,9; full enumerators and seeds | Prop. III.2; Eqs.(10)–(12),(A1)–(A3) | `o3_verify.py`, `reconstruct.py` | exact |
| 5 | Cauchy and HZ circle parent graphs, all stored cut certificates | Sec. IV; Eq.(17) | `reconstruct.py` | exact; HZ formula independently implemented |
| 6 | Arbitrary branch isometries preserve AME; matching condition βV=e^(iθ)V conjugate(α) | Prop. V.1; Eq.(20) | `sym1_verify.py`, `inventory.py` | exact finite realizations; cited algebraic argument |
| 7 | Six nontrivial finite redesigns with C4,C6,C2,C2,C3,C2 | Prop. V.2; Table IV rows1–6 | `sym1_verify.py`, `permutation_cycles.py` | exact subgroup certificates |
| 8 | C15 at(15,62); logical order3 and multiplicities(4,2,2); all primes p≡1 mod15 | Thm. V.3; Table IV row7; Eq.(C3) | `sym1_verify.py`, `rank_and_c15.py`, `inventory.py` | exact witness/action; cited all-primes orbit proof |
| 9 | Full projective structured groups of the eight previously classified states (excluding15_22 and the N9/N11 additions) | Prop. D.1; Eqs.(D1)–(D3) | `sym1_verify.py` | exact, with completeness reductions in `docs/sym1_notes.md`; restricted Clifford class only |
| 10 | Projector rank exclusions at N13,N15; optimal stabilizer ranks16,8 | Sec. VI; App. B | `o3_verify.py` | exact rational certificates |
| 11 | N17: K22 excluded, K23 and K32 feasible enumerators; even-weight K32 excluded | Sec. VI; App. B | `o3_verify.py` | exact projector tests; general rank≥23 separately certified; no state from feasibility |
| 12 | No weight9 one-generator extension of the specified N17 subgroup; 4,095 cosets | Sec. VI; App. B | `o3_verify.py` | exact, scoped to that subgroup |
| 13 | Arbitrary-spectrum half-uniform qubit rank≥9,8,23,19 at N13,15,17,19 | Prop. VI.1; Eqs.(B1)–(B7) | `general_rank.py`, `rank_and_c15.py`, `farkas_symbolic.py` | exact, with written inequality derivation |
| 14 | Original N13 graph basis requires support≥16 and 16 divides equal-weight branch count | Sec. VI; Eq.(B8) | `o3_verify.py` | exact masks plus Fourier argument |
| 15 | AME(14,13) parent available for a hypothetical binary rank9..13 ingredient | Sec. VI | `parent13.py` | exact parent; no AME(13,26) state supplied |
| 16 | Strict all-cut branch capacity K≤p and exclusion of that mechanism at(13,10) | Sec. VI | `rank_and_c15.py`, `inventory.py` | exact rank certificate; cited entropy argument; no unrestricted nonexistence |
| 17 | Binary marginal residuals on three deterministic cuts per stored N≥13,N≤15 cell | App. A, corroboration only | `independent.py` | numerical; `--all-marginals` enables the slower exhaustive numerical mode |
| 18 | Coupling lineage and binary AME background | Sec. I; Table I | `inventory.py` | cited; source links in `data/reference/README.md`, no Lean build |
| 19 | Eventual existence for sufficiently large integer d at fixed N | App. E | `inventory.py` | cited Keevash/Helwig–Cui implication, no effective threshold |
| 20 | Catalogue, data provenance and packaged-file integrity | App. A (availability) | `inventory.py` | exact file/catalogue checks; not a mathematical proof of cited results |
| 21 | Computational-basis support fraction 1−(K−1)/(Kp), exact zeros and intensity classes | Lem. A.1 (`lem:support`); Fig. 2 | `support.py`, `o3_verify.py` | exact nine-state checks; analytic cyclotomic proof for the stated graph-branch form |

| 22 | Six AME(9,q) graphs, q3,4,5,7,8,9 | Sec. VIII | `prime_powers.py`, `prime_powers_independent.py` | exact field arithmetic from defining polynomials |
| 23 | q9 parents10,12,16; cells9_18,11_18,15_18 | Sec. IV; Table II | `prime_powers.py`, `prime_powers_independent.py` | exact Hermitian/minor/cut and binary Walsh checks |
| 24 | Kitamura9,6:126 cuts and16-branch decomposition | Table I; Sec. VIII | `kitamura96.py` | exact when pinned external data supplied; explicit NOT_RUN otherwise; no Lean build |
| 25 | Nine-party product classification; binary9 shadow | Cor. VIII.1 | `product_classification.py` | finite factor certificates3..2000 plus written infinite proof and cited inputs |

The q9 parents are extended RS at length10, N04's explicit F81 search matrix at
length12 (a second realization of parameters supplied by HZ TheoremS7), and HZ's
finite M16,9 at length16. The six graph inputs and three coupled cells are in
`data/prime_powers/`. AME(9,18) also follows from products; (11,18) and (15,18)
do not follow from the available product inputs. This is not a priority claim.
For extension fields, integer labels encode polynomial-basis coefficients and
phases use the field trace, not arithmetic modulo q. See
[the field conventions and external-data procedure](docs/R10-prime-powers.md).

The original structured local group is
`C2^(N-log2(K)) × (Cp^(N-1) ⋊ C2)`, with inversion by the last C2, modulo scalar phases.
Its party group is trivial only within products of qubit Clifford and prime-qudit Clifford operations.
Redesign subgroups are lower bounds, not full group classifications. Isometry freedom does not establish
LU inequivalence. Unrestricted AME(13,10), AME(13,26), general additive N17/rank32 constructions and full
local-unitary symmetry are not settled here.

## Closed forms and data conventions

For N=2k+1, use the local identification `|b>_2 |y>_p = |pb+y>_(2p)` and

```
u_a(b) = 2^(-N/2) (-1)^(sum_(i<j) B_ij b_i b_j + branch_labels[a] . b)
v_a(y) = p^(-N/2) exp((2πi/p) [sum_(i<j) G_(i+1,j+1) y_i y_j + a sum_i G_(0,i+1) y_i])
|Psi> = K^(-1/2) sum_(a=0)^(K-1) |u_a> |v_a>.
```

`data/o3_external_spec.json` gives B, G and the **ordered** branch labels for each cell. Bit i is party i;
prime vertex0 is conditioned; GF(4) symbols 0,1,ω,ω² are encoded 0,1,2,3. Binary rank r gives K=2^(N−r).
The checker enumerates small stabilizer groups, never the full `(2p)^N` composite tensor.

For redesigned states replace `v_a` by `TV|a>`, where V is an isometry from C^K to C^p.
`data/sym1_external_spec.json` records a deterministic spectral-projector/Gram–Schmidt recipe and exact
logical matrices, including phases, for V. `sym1_verify.py` verifies projector ranks in cyclotomic polynomial
quotients and the physical Clifford lifts. [docs/sym1_notes.md](docs/sym1_notes.md) explains why this
certifies the state and symmetry without floating-point diagonalization.

## Running

Python **3.10 or newer** on Linux/macOS, numpy and sympy (the symmetry verifier uses Unix resource accounting). No Sage, scipy, solver, Lean, GPU or network is needed after
installing dependencies. On Linux the reference run takes about **20 seconds**; exact timings and versions
are in [results/timings.txt](results/timings.txt) and [results/environment.txt](results/environment.txt).

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
./run_all.sh .venv/bin/python
# Equivalent package entry point:
.venv/bin/python -m coupled_ame
# Optional, potentially much slower; does not replace the committed default logs:
.venv/bin/python -m coupled_ame.independent --all-marginals
```

If the system Python lacks ensurepip/venv support, `uv venv .venv` followed by
`uv pip install --python .venv/bin/python -r requirements.txt` is an alternative.
From the clone root, run any verifier with the virtual-environment Python, for example
`.venv/bin/python -m coupled_ame.rank_and_c15`. The shell runner can be invoked by absolute path
from any working directory. Do not use Python `-O`: assertions are part of the certificate checks. The runner disables
optimization and limits numerical library threads to one. Scripts return nonzero on failed checks.

`run_all.sh` rewrites every committed result log, the environment record, timings, and generated JSON
summaries. Elapsed times and small floating-point residuals may vary; exact conclusions must agree.
For the nine N≥13 cells, the independent implementation checks 61,633 unoriented parent cuts and binary support constraints;
small_families.py checks the additional 4,704 oriented cuts twice.
its default numerical component checks first/middle/last cuts in lexicographic order for each original N13/N15 cell.
No historical exhaustive numerical residual is presented as newly reproduced.

## Layout and provenance

- `coupled_ame/`: portable verifier modules and finite-field reconstruction helpers.
- `coupled_ame/__main__.py`: suite runner; `_paths.py` resolves clone-relative input/output paths.
- `data/`: frozen amplitude specifications, certificates, symmetry inventories and the catalogue.
- `data/reference/`: attribution metadata and primary-source links; no third-party PDFs or Lean code vendored.
- `docs/`: mathematical certificate notes, claim mapping and an import manifest with original and packaged SHA256 hashes.
- `results/`: logs and machine-readable outputs of the reference run.

O3/SYM1 are retained dataset identifiers, not software dependencies. Original verifier bodies were ported
with input/output paths separated. The independent O3 implementation retains its own arithmetic;
its runner adds explicit failure assertions and a declared numerical sample. The independent SymPy
Farkas check now asserts its result, rather than merely printing it. R01b and R02 checks are packaged
as `rank_and_c15.py` and `permutation_cycles.py`. Search histories, cluster scripts, paper sources and literature PDFs are excluded.
The earlier announcement remains in Git history; its unverified catalogue and priority language are
superseded by this evidence-backed version. [docs/CLAIM_MAP.md](docs/CLAIM_MAP.md) states what is checked
and what still rests on a written or cited argument.

## Citation, licence and AI assistance

Please cite the article when published and this repository:

```bibtex
@misc{pandya2026coupledbranchame,
  author = {Palash Pandya},
  title = {Companion code and data: coupled-branch AME states, version 0.1 (pre-release)},
  year = {2026},
  howpublished = {\url{https://github.com/palashpandya/coupled-branch-ame}}
}
```

See [CITATION.cff](CITATION.cff). Code is MIT; data and results are CC BY 4.0. See
[LICENSE](LICENSE) and [LICENSE-DATA.md](LICENSE-DATA.md). Published parent formulas and code parameters
are credited separately; no ownership over those results is claimed.

Codex and Claude assisted in development, mathematical checking and documentation. Computational
certificates have explicit scopes; neither AI assistance nor successful execution replaces review of
the analytic arguments. This pre-release does not claim a completed human publication review.

## Reproduce the article graphics

The verifier suite includes `support.py`, which exports exact squared-modulus
polynomials and checks the computational-basis support of the nine original
graph-branch states. Equal compressed-cell sizes are not equal probabilities;
the support formula is basis-dependent and does not cover arbitrary isometries.

Figure generation has separate dependencies in `requirements-figures.txt`. After
running the verifier suite, run `.venv/bin/python figures/build.py` to reproduce
the vector PDFs and the exact-data validation record. See [figures/README.md](figures/README.md).
No plotting package is needed to run the verifiers.

The p11 parent is reconstructed by `parent11.py`, invoked by `reconstruct.py`.
It checks the GF121 Hermitian identity, all12,869 nonempty minors, all12,870 balanced-cut
orientations of the graph and a failing one-edge mutation. The parent parameters were
previously recorded in the Huber–Wyderka table citing Grassl–Rötteler; this package supplies
an explicit searched matrix and graph certificate, not a new parent existence claim.
`data/parent11_certificate.json` contains the matrix, graph conversion and negative control.
The existing symmetry inventory covers the previous eight states only; 15_22 is unclassified.

## R07 evidence and scope

`small_families.py` ports the independent N01 acceptance code (`small_exact.py`), reconstructs the
unchanged Atlas/Kitamura binary ingredients from `data/o1_external_spec.json`, replays every nonempty
minor of the two GF49 matrices and their graph conversions, and checks all eight cells. A second
determinant implementation checks all 4,704 new oriented cuts. Duplicate branch labels and zero
parents are rejected. The finite certificates do not replace the analytic extended-Cauchy proof.

`general_rank.py` rebuilds arbitrary-spectrum inequalities using Fraction arithmetic and replays
`data/general_rank_certificates.json`. The four contradictions are −3328/492545,
−2031120/18916487, −6528/6182327 and −16093152/697142701. Exact feasible enumerators at the
next ranks are checked too; they are not quantum states. No scipy or solver is needed for replay.
At N15 this makes p≥11 complete within the all-cut route. At N17 primes≤19 are excluded and
primes23..61 remain unresolved here. These are not unrestricted AME nonexistence claims.

R08 resolves the N7 all-cut question: Steane K2 plus AME(8,p) works for primes≥5,
and the exact all-party shadow row excludes every pure ((7,K,4))_3 code with K>1.
K1 would require a nonexistent three-uniform seven-qubit state. No search is needed for replay. Literature-search scope and attribution are recorded in
`docs/R07-literature.md`; no priority claim is made. Support exports still cover the nine N≥13
states, and symmetry classification still covers the previous eight states only.

## N7 reconstruction and shadow condition (R08)

The known N7 existence cells (7,10), (7,14), (7,22) are certified by `n7.py`, using
`data/n7_spec.json` and `data/n7_certificates.json`. The whole all-cut family p≥5 uses an explicit
F25 Hermitian parent at p5, extended Cauchy at p7 and ordinary Cauchy at p≥11. These cells are
already covered by Shi et al.; no equality or local-unitary equivalence to their states is asserted.
The Steane enumerator is **1+21z^4+42z^6**, so the minimum weight is four.

| Statement | Article anchor | Exact replay |
|---|---|---|
| Three N7 cells, 70 oriented parent cuts each | Table II; discussion | `n7.py`: Hermitian product, 69 nonempty minors, graph chart, binary Walsh average, independent 35-cut Leibniz determinants |
| Any K>1 all-cut branches require S(N,p)=sum(s=0..k)(−1)^s binom(N,s)/p^s≥0 | `lem:branch-shadow` | Purity/complement derivation; `n7.py` replays all256 shadow rows at N7 |
| S(7,3)=−8/27 excludes all pure ((7,K,4))_3, K>1 | Same lemma | E=−(16/27)(1−1/K); no additive, stabilizer or parent-extension assumption |
| At N7,11,15,19 exactly primes2,3 are excluded by this row; N9,13,17 none | Following lemma | p2,p3 evaluated exactly; positive coefficients in p−5 certify every p≥5 |

The general inequality is valid at every odd N. The finite sign table is not a universal
classification for N≡3 (mod4): S(27,5)<0. For N≡1 (mod4), the even Taylor truncation of
(1−x)^N at x=1/p is positive, so this row cannot exclude a prime. The shadow row gives a
parent-independent floor p≥5 at N7,11,15; the N15 binary rank bound gives the stronger floor11.
The no-go concerns the stated all-cut route. AME(7,6) exists by Shi's cut-dependent coupling;
no unrestricted AME nonexistence or particular mandatory cancellation pattern is inferred.


## Optional independent Kitamura all-cut check (R11)

`kitamura96_exact.py` checks every physical marginal using exact integer
coefficients of sixth roots of unity, independently of the fast difference-type
checker. It is intentionally outside the default runner. See
[arithmetic guarantees and usage](docs/R11-audit.md). It uses the same pinned,
caller-supplied external data and writes no dense tensor files. A low floating
residual alone is not treated as proof. The classification's primary small-field
inputs are the six explicitly certified graphs, with RS for all prime powers>=8.
