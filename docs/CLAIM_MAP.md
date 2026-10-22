# Claim-to-evidence map

Labels and printed numbers refer to the article of 22 October 2026 (updated R08), which is not
included here. C01–C30 and P01–P09 are stable IDs from the original claim ledger.
The README table is the entry point; this file maps the full computational scope.
Paths below are clone-relative. Dataset basenames beginning O3/SYM1 identify the
research stage, not an external directory or dependency.

## Formal statements and all table rows

| Article / ledger | Evidence and checker | Scope |
|---|---|---|
| Thm.I.1 `thm:main`, C02–C12 | `data/o3_external_spec.json`, `o3_binary_certificates.json`, `o3_construction_certificates.json`, `o3_circle13_certificate.json` (all under `data/`); `coupled_ame/o3_verify.py`, `independent.py`, `reconstruct.py` | Twenty finite instances exact (including small_families_spec.json / small_families.py); all-primes conclusion uses the Cauchy proof and coupling identities. |
| Prop.II.1 `prop:coupling`, C02; Lem.II.2 `lem:parent`, C03 | `docs/o4_algebraic_notes.md`, parent cuts in the preceding row | Written matrix-block/partial-trace argument; permits nonorthogonal binary states and nonnegative weights. |
| Prop.III.1 `prop:weights`, C04 | `data/o3_binary_certificates.json`; `coupled_ame/o3_verify.py` | Pauli expansion of normalized projector, not a uniformity assertion about each supported vector. |
| Prop.III.2 `prop:binary`, C05–C08 | Same binary certificates; `coupled_ame/codes.py`, `reconstruct.py` | Rebuild six polynomial shifts, length18 seed and restrictions; check full enumerators and subgroup ranks. |
| Lem.IV.1 `lem:cauchy`, C09 | `coupled_ame/construction.py`, `reconstruct.py`; analytic argument below | Character-sum/Cauchy proof is not inferred from finite examples. |
| Prop.V.1 `prop:isometry`, C14; matching Eq.(20), C15 | `docs/sym1_notes.md` §1; `coupled_ame/sym1_verify.py` | Written isometry/intertwiner argument; exact finite spectral realizations. |
| Prop.V.2 `prop:redesigns`, C19,C20 | `data/sym1_external_spec.json`, `sym1_alternates.json`; `coupled_ame/sym1_verify.py`, `permutation_cycles.py` | Six finite nontrivial subgroups, not full redesigned groups. |
| Thm.V.3 `thm:c15`, C20 | `data/sym1_external_spec.json/family_witness`; `coupled_ame/rank_and_c15.py`, `sym1_verify.py`; `docs/sym1_notes.md` §6 | Exact p31 witness and signed logical action; orbit/multiplicity proof extends to p≡1 mod15. |
| Prop.VI.1 `prop:rank9`, C28 | `data/o4_lp_certificates.json`; `coupled_ame/rank_and_c15.py`, `farkas_symbolic.py`; `docs/o4_algebraic_notes.md` | Arbitrary-spectrum rank≥9,8,23,19 at N13,15,17,19 (general_rank.py / general_rank_certificates.json). Rational system independently reconstructed; symbolic identity independently derived. |
| Prop.D.1 `prop:groups`, C16–C18 | `data/sym1_asbuilt.json`, `sym1_binary_aut.json`, `sym1_parent_results.json`, `sym1_symmetry_generators.json`, `sym1_groups.json`; `coupled_ame/sym1_verify.py`; `docs/sym1_notes.md` §§2–5 | Exact finite exhaustions plus written completeness reductions; only the factorwise Clifford class, modulo scalar phases. |

All evidence names abbreviated in table cells are under `data/`, all verifier names under `coupled_ame/`.

**Table I (lineage), P01–P05:** each of its five rows is attributed in
`data/reference/README.md`: Shi et al. (2 branches, Steane/odd graph, cut-dependent);
Atlas (4 branches, nine-cycle/ten-site quinary parent, all-cut); Kitamura
(2 branches, twelve-qubit five-uniform/BB AME(12,5), all-cut); this work
(K16,8,64, binary projectors/conditioned Cauchy or HZ parents, all-cut).
No separate parent attribution is inferred for Atlas. Source-level formalization
claims are cited, not checked by building Lean in this repository.

**Table II (every original cell), C10,C12:** use
`data/o3_external_spec.json/constructions/<key>` and the matching entry of
`data/o3_construction_certificates.json`. Outputs are `results/o3_verification.json`,
`independent_o3.json`, `reconstruction.json`.

| Key | N,d | K | Parent | Oriented / unoriented cuts |
|---|---|---|---|---|
| 7_10 | 7,10 | 2 | F25 Hermitian | 70 / 35 |
| 7_14 | 7,14 | 2 | extended Cauchy p7 | 70 / 35 |
| 7_22 | 7,22 | 2 | Cauchy p11 | 70 / 35 |
| 9_10 | 9,10 | 4 | Atlas p5 | 252 / 126 |
| 9_14 | 9,14 | 4 | GF49 Hermitian p7 | 252 / 126 |
| 9_22 | 9,22 | 4 | Cauchy p11 | 252 / 126 |
| 9_26 | 9,26 | 4 | Cauchy p13 | 252 / 126 |
| 11_10 | 11,10 | 2 | BB/Kitamura p5 | 924 / 462 |
| 11_14 | 11,14 | 2 | GF49 Hermitian p7 | 924 / 462 |
| 11_22 | 11,22 | 2 | extended Cauchy p11 | 924 / 462 |
| 11_26 | 11,26 | 2 | Cauchy p13 | 924 / 462 |
| 13_34 | 13,34 | 16 | Cauchy p17 | 3432 / 1716 |
| 13_38 | 13,38 | 16 | Cauchy p19 | 3432 / 1716 |
| 13_46 | 13,46 | 16 | Cauchy p23 | 3432 / 1716 |
| 15_22 | 15,22 | 8 | GF121 Hermitian | 12870 / 6435 |
| 15_26 | 15,26 | 8 | reconstructed HZ circle p13 | 12870 / 6435 |
| 15_34 | 15,34 | 8 | Cauchy p17 | 12870 / 6435 |
| 15_38 | 15,38 | 8 | Cauchy p19 | 12870 / 6435 |
| 15_46 | 15,46 | 8 | Cauchy p23 | 12870 / 6435 |
| 17_134 | 17,134 | 64 | Cauchy p67 | 48620 / 24310 |

The total is 128180 oriented cuts, or 64090 after identifying transpose cuts. The three N7 rows use data/n7_spec.json and results/n7.json. The eight N9/N11 rows use data/small_families_spec.json and results/small_families.json.

**Table III (notation), C01–C04,C08,C14,C15:** N=2k+1; p prime and d=2p;
K is branch count (projector rank only in the orthonormal case); binary stabilizer
rank r gives K=2^(N−r); B,G are binary/prime graphs; U,T are branch embeddings;
V:C^K→C^p is an isometry. These are definitions, with explicit conventions in
`data/o3_external_spec.json` and `data/sym1_external_spec.json`.

**Table IV (every redesign), C19,C20:** entries in
`data/sym1_external_spec.json/constructions`, except the final `family_witness`.
`coupled_ame/sym1_verify.py` checks physical lifts, phases, logical action and
spectral ranks in exact cyclotomic quotients. `permutation_cycles.py` extracts
spatial cycles independently. Output: `results/sym1_verification.json`.

| Key | Party subgroup | Binary eigenvalue multiplicities |
|---|---|---|
| 13_34 | C4 | 4,4,4,4 |
| 13_38 | C6 | 3,3,2,3,3,2 |
| 13_46 | C2 | 8,8 |
| 15_34 | C2 | 4,4 |
| 15_38 | C3 | 2,4,2 |
| 15_46 | C2 | 4,4 |
| family_witness (15,62) | C15 | 4,2,2 (logical order3) |

The original(15,26) and(17,134) entries are retained without a nontrivial redesign claim.

## Remaining numerical and algebraic claims

- **C05–C08:** every coefficient and exponent of W13,W15,W17, the polynomial and
  length18 seed, ranks9,12,11, minima7,8,9, and nonidentity sizes511,4095,2047:
  `data/o3_binary_certificates.json`, `o3_verify.py`, `reconstruct.py`.
  Graph branch signs and ordered labels use `data/o3_external_spec.json`.
- **C09,C11:** Cauchy thresholds17,17,67 follow from p≥N+1 and K≤p;
  the complete N15 threshold is11 using the GF121 and circle parents. The p13 member uses `data/o3_circle13_certificate.json`. Its GF169 formula,
  Hermitian matrix, graph conversion, and all cuts are reconstructed by `circle13.py`
  and checked against the certificate by `reconstruct.py`.
- **C14,C15,C19,C20:** phases, isometry recipe, eigenvalue multiplicities and fixed
  point/cycle counts: `data/sym1_external_spec.json`, `sym1_verify.py`;
  N13 spatial patterns1·4³,1·6²,1·2⁶ and N15 patterns1·2⁷,3⁵ additionally checked
  by `permutation_cycles.py`. The C15 logical signed images, trace2, order3 and
  multiplicities4,2,2 are checked in `rank_and_c15.py`. The prime logical permutation
  has multiplicities((p+2)/3,(p−1)/3,(p−1)/3); at p31 these are(11,10,10).
- **C16–C18:** full structured original group orders, ingredient automorphisms,
  endomorphism-algebra dimensions and logical matching: data and proof notes in
  the Prop.D.1 row. Counts are not unrestricted LU classifications.
- **C22–C25:** branch capacity K≤p is the written entropy/Singleton argument;
  `data/o3_lp_certificates.json` and `o3_verify.py` give projector exclusions at
  N13/K1..8 and N15/K1..7, feasible enumerators K9 and K8, N17 tests K22/23/32,
  and even-weight contradictions−1/7 at(13,16) and−1/2 at(17,32). No state
  existence follows from LP feasibility and the R07 arbitrary-spectrum certificate separately proves rank≥23.
- **C26:** all4095 nonzero extension cosets of the specified N17 subgroup:
  `data/o3_n17_extensions.json`, exhaustively replayed by `o3_verify.py`.
- **C27:** masks6403,6402,6161,4401, fifteen low-weight nonzero words, sixteen
  syndromes, mass1/16 and support/divisibility: `data/o3_nonstabilizer_search.json`,
  `o3_verify.py`, Fourier argument in `docs/o4_algebraic_notes.md`.
- **C28:** all57 rational rank-inequality rows, seven variable columns,
  multipliers292864,8192,133120,3584,39936,1536,13312,1 and contradiction−3328
  (normalized−3328/492545): `data/o4_lp_certificates.json`, independently checked
  by `rank_and_c15.py`; `farkas_symbolic.py` derives the transforms independently
  in SymPy and asserts the constant identity. The extra rank5 certificate is also
  replayed but is not a separate manuscript theorem.
- **C29:** certified AME(14,13) parent: `data/o4_external_spec.json/target_parent`,
  `parent13.py` and `rank_parent.py`. Rank9..13 binary ingredients would suffice;
  none is supplied. The rank≥9/capacity argument excludes only strict all-cut
  coupling at(13,10), including weighted/nonorthogonal binary branches.
- **C30:** unresolved statements are scope boundaries, not results inferred from
  failed searches. Search histories and large unsuccessful searches are omitted.
- **C13,C21:** historical dense numerical residuals are not manuscript claims and
  are not imported as current results. `independent.py` supplies fresh declared
  numerical corroboration on three deterministic cuts per cell by default;
  `--all-marginals` is optional. No independent dense symmetry run is claimed.

## Written versus computational arguments

For a balanced cut of the Cauchy graph, partition the row and column vertex sets
into I,J on one side. The cut matrix, after rearrangement, has blocks C[I,Jc] and
C[Ic,J]^T. Each is a square Cauchy minor, with determinant a product of distinct
point differences divided by nonzero cross differences. Both are invertible.
Character orthogonality then gives the maximally mixed reduction. This proves
all eligible fields, not just the stored examples.

Condition an even-party parent at its reference site. Its reference-plus-k-site
reduction is I/p^(k+1); comparison of reference matrix blocks gives
Tr(v_a v_b*)=δ_ab I/p^k on every k-site cut. Coupling to a k-uniform binary average
therefore gives I/(2p)^k. The isometry generalization follows by linearity.
The entropy proof of capacity K≤p purifies the code and partitions physical sites
into k,k,1; the two decoupling relations and subadditivity bound the reference
entropy by that of the remaining one site.

The C15 family uses one fifteen-point multiplicative orbit and a reference at
infinity in an extended RS[16,8,9] code. Common coordinate scaling adjusts the
reference multiplier to order3. Its eigenvalue multiplicities contain(4,2,2)
for every prime p≡1 mod15 (smallest31). The finite p31 witness is exact;
this orbit argument supplies the infinite family. See `docs/sym1_notes.md` §6.

P01–P06 (lineage/parents/codes), P08 (Keevash plus array implication), P09
(uniform-subspace/encoding ancestry) and the added qubit/secret-sharing citations
are linked in `data/reference/README.md`. The inventory verifier checks metadata
and file integrity only. P07 is a qualified historical audit, not a new novelty
search. No third-party source code is copied or proof-assistant execution claimed.

## Reproduction and provenance

`docs/import-manifest.json` records the original basename and SHA256, packaged
path/hash, and adaptation status for imported evidence and checker sources.
`data/SHA256SUMS.json` additionally covers all frozen data and reference metadata.
Paths have no dependency on the original working repository. Generated summaries
are written only to `results/`; the suite does not overwrite data.
The independent implementations do not import each other's mathematical routines.

R01b's rank/C15 checks are `rank_and_c15.py`; R02's cycle check is
`permutation_cycles.py`; Claude's symbolic Farkas derivation is
`farkas_symbolic.py`. The independent O3 arithmetic is in `independent_core.py`;
`independent.py` adds failure assertions and declares the numerical scope.
The original construction helpers are retained as library functions; discovery
entry points and solver searches are omitted. The manuscript and local workflow
notes are not part of this repository.

## Computational support and graphics (R04 stage 2)

| Article anchor | Data / checked export | Scope and validation |
|---|---|---|
| Lemma A.1 `lem:support`; `eq:compressed-intensity`, `eq:support-fraction` | `data/o3_external_spec.json`; `coupled_ame/support.py`; `results/support.json` | Exact checks for nine originals. General proof uses full independent binary label span, distinct prime labels, prime p, K<p, nonzero reference row and equal-weight graph-branch form. No extension to arbitrary isometries or bases. |
| Fig.2 `fig:support`, worked AME(15,26) paragraph | Same export, `15_26` full canonical array; `figures/build.py` | 104 cells, seven exact zeros, support97/104, 50 distinct squared moduli including zero; each cell has 2^12·13^14 strings. R=|S|²/8; Born cell mass R/104. Exact normalization/mask/classes asserted before floating color evaluation. |
| Fig.3 `fig:c15` | `data/sym1_external_spec.json/family_witness`; `results/rank_and_c15.json`; figure script | Checked signed images, physical cycle, prime multiplier5 modulo31, dimensions(4,2,2) and(11,10,10). Physical arrows are permutation arrows; local Clifford compensation required. |
| Fig.4 `fig:capacity` | `data/o4_lp_certificates.json`, `results/rank_and_c15.json`, binary rank16 certificate and original p17 specification | Rank≥9 without spectrum assumptions; capacity K≤p uses written entropy argument. Rank9..13 at p13 remains unresolved. No unrestricted AME nonexistence claim. |
| Fig.5 `fig:weights` | `data/o3_binary_certificates.json`; `results/o3_verification.json`; figure script independently re-enumerates generator spans | First occupied weights7,8,9; totals511,4095,2047 excluding identity, common vertical scale. Uniformity is of normalized projector, not every supported pure vector. |

`figures/validation.json` records exact figure assertions and PDF hashes. The
matplotlib PDFs are reproducible from `figures/build.py` with the separate
`requirements-figures.txt`; the two TikZ diagrams reside only in the article.
The optional (N,d) lineage map and candidates B,F,G were not built.

## R06: the unified N15 family and the p11 certificate

- `thm:main` now gives prime thresholds17,11,67 for N13,15,17. N15 uses one binary ingredient and three parents: GF121 at p11, HZ circle at p13, Cauchy for primes≥17. At N13 and N17 the limiting inequality is K≤p, with K16 and K64. No unread Ball theorem or general classical-MDS exclusion is used.
- Table II adds15_22: N15,d22,K8, Hermitian parent,12870 oriented/6435 unoriented cuts. Total across nine cells:123266/61633. `data/o3_external_spec.json`, `data/o3_construction_certificates.json` and `data/catalogue.json` include the new cell.
- `eq:parent11`: `data/parent11_certificate.json`; `coupled_ame/parent11.py` invoked by `reconstruct.py` checks the Hermitian identity, all12869 minors, symplectic/graph conversion, all12870 cuts and one-edge negative control. `o3_verify.py` and `independent.py` independently accept the assembled specification. Results: `results/parent11.json`, `o3_verification.json`, `independent_o3.json`, `reconstruction.json`.
- `tab:support` (Table VI), `lem:support`: `results/support.json` supplies every row, exact zeros, support fractions and intensity counts for nine cells. New15_22 row:88 cells,7 zeros,81/88 support,42 distinct squared moduli including zero. Fig.2 remains the15_26 example.
- Symmetry classification and its group formulas still cover only the previous eight states, explicitly excluding15_22. `sym1_verify.py` selects the keys present in the existing symmetry certificates; no new group claim is inferred.
- Parent existence attribution: locally read Grassl–Rötteler arXiv1502.05267v1, Proposition2, Theorem8 and SectionVI; local Huber–Wyderka table snapshot records AME(16,11) with this reference. The explicit bordered-circulant matrix was found in V01. No novelty claim for parent existence or exhaustive search is made.

## R07: five families and arbitrary-spectrum rank bounds

Current evidence is in the companion repository, independently of historical R01/R06 replay files.

| Article anchor | Evidence | Scope |
|---|---|---|
| Theorem I.1; Table I; Table II, N9/N11 | data/small_families_spec.json; data/small_families_certificates.json; data/o1_external_spec.json; coupled_ame/small_families.py and small_exact.py; results/small_families.json | Eight cells: N9/N11 at p5,7,11,13. Atlas K4 and Kitamura K2 branches unchanged. Known p5 parents attributed to Atlas and BB/Kitamura. |
| Sec. IV, GF49 parents | data/parent10_7.json; data/parent12_7.json; results/small_families.json/parents | Hermitian products, 251/923 nonempty minors, graph conversion and 252/924 oriented cuts. |
| Sec. IV, small-family range | small_families.cauchy; manuscript determinant argument | N9 p≥11 ordinary; N11 p11 infinity column, p≥13 ordinary. p5/p7 finite parents close the range p≥5. |
| Table II total | results/small_families.json + results/reconstruction.json | 17 cells, 127970 oriented / 63985 unoriented cuts. New rows: (9,10),(9,14),(9,22),(9,26), each252; (11,10),(11,14),(11,22),(11,26), each924. |
| Proposition VI.1 (`prop:rank9`); rank-capacity table (`tab:rank-capacity`); Appendix B | data/general_rank_certificates.json; coupled_ame/general_rank.py; results/general_rank.json | Arbitrary spectrum: rank≥9,8,23,19 at N13,15,17,19. Exact contradictions −3328/492545, −2031120/18916487, −6528/6182327, −16093152/697142701. Exact next-rank LP points; no state inferred. |
| N15 completeness / N17 gap | Same bounds and Sec. VI entropy proof | All-cut route: N15 primes≤7 excluded, p≥11 attained; N17 primes≤19 excluded, primes23..61 unresolved here. |
| N7 analytic discussion | Steane stabilizer weights; Huber–Wyderka table AME(8,5); extended/ordinary Cauchy for primes≥7; shadowbounds Sec. IX p8 explicitly excludes n8,D3 | Does not exclude pure ((7,2,4))_3 or the all-cut route at p3; no search here. |
| Literature and attribution | docs/R07-literature.md; pinned Atlas/Kitamura sources and BB; supplied Claude search note | Targeted search only, no priority claim. |

The support table (`tab:support`) remains nine N≥13 cells. The complete symmetry classification
remains the earlier eight cells; none of the N9/N11 states or15_22 is added to that claim.
The earlier rank-grid caution is superseded by exact arbitrary-spectrum certificates, not by
extrapolation from projector tests. Stable LaTeX labels identify the current tables.

## R08: N7 and the general all-party shadow row

All companion paths below are clone-relative; imported research sources are identified by workspace-relative provenance.

| Article anchor | Evidence | Scope |
|---|---|---|
| Discussion; Table II N7 rows | data/n7_spec.json; data/n7_certificates.json; results/n7.json; coupled_ame/n7.py | (7,10),(7,14),(7,22); each70 oriented /35 unoriented cuts. Family primes≥5, known existence covered by Shi et al.; no LU comparison. |
| Steane correction | data/steane_graph.json; n7.py | 1+21z^4+42z^6, rank6, K2, minimum weight4. Graph subgroup reconstructed under Fourier mask15; actual graph sector checked. |
| F25 parent | data/parent8_5.json; parent8_5_certificate.json | theta²2; B Hermitian-unitary;69 nonempty square minors; graph chart and70 cuts. |
| Lemma `lem:branch-shadow` | Text purity/complement/swap proof; data/n7_shadow_certificate.json; results/n7.json | E=2(1−1/K)S(N,p)≥0. For N7,p3: S=−8/27; every K>1 excluded. K1 separately excluded by binary AME7 nonexistence. |
| Finite-N all-prime sign list | results/n7.json/sign_table | N7,11,15,19 exclude exactly2,3; N9,13,17 exclude none. Positive integer coefficients of p^k S in p−5 prove all p≥5. |
| General-N qualification | Taylor-remainder proof in text; results/n7.json/counterexample_to_all_N_extrapolation | N≡1 mod4: S positive. Do not extrapolate the finite odd-k table: S(27,5)<0. |
| Current totals | n7.json + small_families.json + reconstruction.json |20 cells;128180 oriented /64090 unoriented cuts. |

The old R07 N7 “undecided” remark is superseded by the exact shadow proof. The main theorem
retains its five N9..17 families; N7 is presented as a known-existence reconstruction in the
discussion. Support and full-symmetry inventories retain their previous nine/eight-state scope.


## R10 current field and classification evidence

# R10: fields, classification and external input

The main families use odd prime powers q with thresholds5,5,17,9,67 for
N9,11,13,15,17. Graph amplitudes are q^(-n/2) chi(sum_{i<j}Gij xi xj),
where chi(z)=exp(2pi i Tr_Fq/Fp(z)/p). Labels encode base-p polynomial
coefficients; local physical digit is q*b+iota(y). F4:t²+t+1, F8:t³+t+1,
F9:t²+1, F81:t⁴+t+2. The i<j formula also works in characteristic2.

`prime_powers` checks six nine-party graphs, the three q9 parents and the
assembled cells. Hermitian checks reconstruct the F9 embedding in F81,
all923/12869 nonempty minors, symplectic and graph conversions, and all
balanced cuts. `prime_powers_independent` adapts Claude's independently
written arithmetic and checks one orientation per balanced cut. Both reject
corruptions. No search executable is packaged or run.

The product rule tensors local factors partywise. Odd dimensions factor into
odd prime powers. If4 dividesd, use its2^e factor (e>=2) and its odd part.
Ifd=2m for oddm>=3, use6 timesm/3 when3 dividesm; otherwise choose a prime
p>=5 dividingm and use2p timesm/p. Residual1 is omitted. Pure-code/RS
inputs supply all prime powers>=3, and Scott excludesd2. The factor check
through2000 is corroboration, not an infinite proof. An exact swap row also
excludes binary AME9 with expectation-1/4.

## Kitamura data: caller-supplied, not redistributed

No redistribution licence was established from the local offline evidence.
We therefore do not include Data.lean or its four matrices in this repository.
The pinned URL and SHA-256 are in `data/kitamura96-source.json`. On a network-enabled
machine, the documented retrieval step is:

```bash
mkdir -p .external
curl --fail --location 'https://raw.githubusercontent.com/KitaKen1/ame-9-6-lean/500ee827dffbeed9bb2ed502adcd6690943a7463/lean/AME96/Data.lean' -o .external/kitamura96-Data.lean
KITAMURA96_DATA="$PWD/.external/kitamura96-Data.lean" ./run_all.sh .venv/bin/python
```

No network request was made during R10. Alternatively supply an existing copy
through KITAMURA96_DATA. The verifier checks the hash before parsing; it never
executes Lean. Without that variable it records NOT_RUN, explicitly separate
from the bundled checks. With data, it checks826560 nonzero difference types
on126 cuts, zero off-diagonal Frobenius numerators, and the160-violation
mixed-phase deletion control. It then verifies B has independent nonzero rows
exactly0..3, H is supported there, all16 labels b^T B are distinct and C has
all126 rank4 cuts. Fixing four binary bits gives disjoint-support normalized
binary branches; H's phase is absorbed in them. The ternary branches are
orthonormal graph-basis shifts of the AME(9,3) graph C. K16>3 forbids all-cut
erasure, so cancellation depends on both cut and branch pair. This is neither
a two-branch Shi state nor an LU-equivalence claim.

The local R10 full run used the already available hash-matching source. The
saved PASS result contains check counts, not the external matrices. A fresh
clone needs the documented external-data step to reproduce that part.

## Provenance and evidence scope

Imports come from `workspace:research/lambda13_20261021/`, pinned in
`docs/import-manifest.json`; all provenance identifiers are workspace-relative.
The final N04 report and artifact hashes were reconciled. Source search logs
are historical, not newly rerun searches. HZ M16,9 is credited to supplement
S9 Eq.S66/S75/TableS2; the length12 F81 matrix is N04's distinct searched
witness, not asserted to be HZ's circle matrix. The article's N9 q9 Cauchy
proof and packaged extended-RS witness establish the same parameters, not
an asserted identical state.

The certificate inventory now has23 coupled cells and142226 oriented /
71113 unoriented parent cuts. Six prime-power nine-party graph inputs add756
four-party cuts separately; Kitamura's126 physical cuts are also separate.
Support formulas remain prime-only and cover nine originals; the full
factorwise-Clifford symmetry inventory remains eight originals. The (11,6)
design stays proposal-only and is not packaged as a construction.
