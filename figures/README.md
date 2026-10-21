# Article figures

From the repository root, with the verifier requirements and the separate
`requirements-figures.txt` installed in an isolated environment:

```sh
./run_all.sh .venv/bin/python
.venv/bin/python figures/build.py
```

The script produces vector `support.pdf` and `pauli_weights.pdf`, plus
`validation.json`. Copy the PDFs to the article's `figures/` directory.
Matplotlib is not required by the verifier suite.

The support plot uses the exact polynomial coefficients exported by
`coupled_ame.support` to `results/support.json`. The export covers all eight
original states; the full cell array is retained for the plotted `15_26` state.
Integer checks establish the zero mask, normalization and 50 equality classes;
complex floating arithmetic only sets the colors. The color scale is linear,
and crosses distinguish exact zeros from small positive values. Syndrome bit
labels are written most significant bit first, matching the integer row index.

The Pauli plot re-enumerates the generator spans and checks the exact counts
against both the certificates and `results/o3_verification.json`. All panels
use the same count scale. The identity is omitted.

The C15 and rank-capacity figures are TikZ within the separate manuscript.
The script also asserts their signed column images, multiplicities, permutation,
prime multiplier and numerical rank boundaries against checked data. No article
TeX is included here. Analytic all-primes and entropy arguments remain written
proofs, not numerical tests. See `docs/CLAIM_MAP.md` for scope.
