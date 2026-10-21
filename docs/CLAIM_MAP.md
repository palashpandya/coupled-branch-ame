# Claim-to-evidence map

Labels and printed numbers refer to the article of 21 October 2026 (updated R04), which is not
included here. C01–C30 and P01–P09 are stable IDs from the original claim ledger.
The README table is the entry point; this file maps the full computational scope.
Paths below are clone-relative. Dataset basenames beginning O3/SYM1 identify the
research stage, not an external directory or dependency.

## Formal statements and all table rows

| Article / ledger | Evidence and checker | Scope |
|---|---|---|
| Thm.I.1 `thm:main`, C02–C12 | `data/o3_external_spec.json`, `o3_binary_certificates.json`, `o3_construction_certificates.json`, `o3_circle13_certificate.json` (all under `data/`); `coupled_ame/o3_verify.py`, `independent.py`, `reconstruct.py` | Eight finite instances exact; all-primes conclusion uses the Cauchy proof and coupling identities. |
| Prop.II.1 `prop:coupling`, C02; Lem.II.2 `lem:parent`, C03 | `docs/o4_algebraic_notes.md`, parent cuts in the preceding row | Written matrix-block/partial-trace argument; permits nonorthogonal binary states and nonnegative weights. |
| Prop.III.1 `prop:weights`, C04 | `data/o3_binary_certificates.json`; `coupled_ame/o3_verify.py` | Pauli expansion of normalized projector, not a uniformity assertion about each supported vector. |
| Prop.III.2 `prop:binary`, C05–C08 | Same binary certificates; `coupled_ame/codes.py`, `reconstruct.py` | Rebuild six polynomial shifts, length18 seed and restrictions; check full enumerators and subgroup ranks. |
| Lem.IV.1 `lem:cauchy`, C09 | `coupled_ame/construction.py`, `reconstruct.py`; analytic argument below | Character-sum/Cauchy proof is not inferred from finite examples. |
| Prop.V.1 `prop:isometry`, C14; matching Eq.(19), C15 | `docs/sym1_notes.md` §1; `coupled_ame/sym1_verify.py` | Written isometry/intertwiner argument; exact finite spectral realizations. |
| Prop.V.2 `prop:redesigns`, C19,C20 | `data/sym1_external_spec.json`, `sym1_alternates.json`; `coupled_ame/sym1_verify.py`, `permutation_cycles.py` | Six finite nontrivial subgroups, not full redesigned groups. |
| Thm.V.3 `thm:c15`, C20 | `data/sym1_external_spec.json/family_witness`; `coupled_ame/rank_and_c15.py`, `sym1_verify.py`; `docs/sym1_notes.md` §6 | Exact p31 witness and signed logical action; orbit/multiplicity proof extends to p≡1 mod15. |
| Prop.VI.1 `prop:rank9`, C28 | `data/o4_lp_certificates.json`; `coupled_ame/rank_and_c15.py`, `farkas_symbolic.py`; `docs/o4_algebraic_notes.md` | Arbitrary-spectrum rank≥9. Rational system independently reconstructed; symbolic identity independently derived. |
| Prop.D.1 `prop:groups`, C16–C18 | `data/sym1_asbuilt.json`, `sym1_binary_aut.json`, `sym1_parent_results.json`, `sym1_symmetry_generators.json`, `sym1_groups.json`; `coupled_ame/sym1_verify.py`; `docs/sym1_notes.md` §§2–5 | Exact finite exhaustions plus written completeness reductions; only the factorwise Clifford class, modulo scalar phases. |

All evidence names abbreviated in table cells are under `data/`, all verifier names under `coupled_ame/`.

**Table I (lineage), P01–P05:** each of its four rows is attributed in
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
| 13_34 | 13,34 | 16 | Cauchy p17 | 3432 / 1716 |
| 13_38 | 13,38 | 16 | Cauchy p19 | 3432 / 1716 |
| 13_46 | 13,46 | 16 | Cauchy p23 | 3432 / 1716 |
| 15_26 | 15,26 | 8 | reconstructed HZ circle p13 | 12870 / 6435 |
| 15_34 | 15,34 | 8 | Cauchy p17 | 12870 / 6435 |
| 15_38 | 15,38 | 8 | Cauchy p19 | 12870 / 6435 |
| 15_46 | 15,46 | 8 | Cauchy p23 | 12870 / 6435 |
| 17_134 | 17,134 | 64 | Cauchy p67 | 48620 / 24310 |

The total is 110396 oriented cuts, or 55198 after identifying transpose cuts.

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
- **C09,C11:** sufficient prime thresholds17,17,67 follow from p≥N+1 and K≤p;
  the p13 exception uses `data/o3_circle13_certificate.json`. Its GF169 formula,
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
  existence follows from LP feasibility and no N17 global threshold is inferred.
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
| Lemma A.1 `lem:support`; `eq:compressed-intensity`, `eq:support-fraction` | `data/o3_external_spec.json`; `coupled_ame/support.py`; `results/support.json` | Exact checks for eight originals. General proof uses full independent binary label span, distinct prime labels, prime p, K<p, nonzero reference row and equal-weight graph-branch form. No extension to arbitrary isometries or bases. |
| Fig.2 `fig:support`, worked AME(15,26) paragraph | Same export, `15_26` full canonical array; `figures/build.py` | 104 cells, seven exact zeros, support97/104, 50 distinct squared moduli including zero; each cell has 2^12·13^14 strings. R=|S|²/8; Born cell mass R/104. Exact normalization/mask/classes asserted before floating color evaluation. |
| Fig.3 `fig:c15` | `data/sym1_external_spec.json/family_witness`; `results/rank_and_c15.json`; figure script | Checked signed images, physical cycle, prime multiplier5 modulo31, dimensions(4,2,2) and(11,10,10). Physical arrows are permutation arrows; local Clifford compensation required. |
| Fig.4 `fig:capacity` | `data/o4_lp_certificates.json`, `results/rank_and_c15.json`, binary rank16 certificate and original p17 specification | Rank≥9 without spectrum assumptions; capacity K≤p uses written entropy argument. Rank9..13 at p13 remains unresolved. No unrestricted AME nonexistence claim. |
| Fig.5 `fig:weights` | `data/o3_binary_certificates.json`; `results/o3_verification.json`; figure script independently re-enumerates generator spans | First occupied weights7,8,9; totals511,4095,2047 excluding identity, common vertical scale. Uniformity is of normalized projector, not every supported pure vector. |

`figures/validation.json` records exact figure assertions and PDF hashes. The
matplotlib PDFs are reproducible from `figures/build.py` with the separate
`requirements-figures.txt`; the two TikZ diagrams reside only in the article.
The optional (N,d) lineage map and candidates B,F,G were not built.
