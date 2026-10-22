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
