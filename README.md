# Coupled-branch AME states

Code, data and exact verification for **Explicit absolutely maximally entangled
states in dimensions twice a prime power**, by Palash Pandya (manuscript in preparation).

The repository contains finite-field constructions, rank certificates and
reconstruction tools for coupled-branch absolutely maximally entangled (AME)
states. It includes prime and prime-power examples, symmetry checks and
independent verification routines. The manuscript is maintained separately.

**Stable snapshot:** [v1.0](https://github.com/palashpandya/coupled-branch-ame/releases/tag/v1.0).

## Run the checks

Requires Python 3.10 or newer on Linux or macOS. From the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
./run_all.sh .venv/bin/python
```

The runner checks the bundled certificates and writes logs and summaries to
`results/`. No Sage, LP solver, Lean, GPU or network connection is needed after
installing dependencies. Do not use Python `-O`: the verifiers use assertions.

Kitamura’s external input is downloaded separately and checked against a pinned
SHA-256 hash. Without it, that check reports `NOT_RUN`.
See [retrieval instructions](docs/R10-prime-powers.md) and the
[optional independent all-cut check](docs/R11-audit.md).

## Find the details

- [Claim map](docs/CLAIM_MAP.md): what each certificate establishes and its limits.
- [Verification guide](docs/VERIFICATION_GUIDE.md): constructions, conventions, provenance and detailed checks.
- [Rank certificates](docs/o4_algebraic_notes.md): includes the self-contained nine-qubit rank bound.
- [Symmetry notes](docs/sym1_notes.md) and [figure reproduction](figures/README.md).

`coupled_ame/` holds the verifiers, `data/` the inputs and certificates,
`results/` the reference outputs, and `docs/` the supporting notes.
Exact computational checks support the stated finite claims; analytic family
statements also require the written arguments identified in the claim map.

## Cite and reuse

Cite the [v1.0 release](https://github.com/palashpandya/coupled-branch-ame/releases/tag/v1.0)
and the accompanying article when published. Machine-readable citation metadata
is in [CITATION.cff](CITATION.cff).

Code: [MIT](LICENSE). Data and results: [CC BY 4.0](LICENSE-DATA.md).
Third-party constructions and inputs are credited in the supporting documentation.
Codex and Claude assisted with development, verification and documentation.

Maintainer: [Palash Pandya](https://github.com/palashpandya),
Center for Theoretical Physics, Polish Academy of Sciences · ppandya@cft.edu.pl.
