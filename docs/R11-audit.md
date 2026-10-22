# R11 optional all-cut root-of-unity verifier

`kitamura96_exact.py` adapts Claude's independent matrix parser and physical-axis
state construction from `workspace:research/lambda13_20261021/claude/check_kitamura96_exact.py`.
It uses the same pinned external-data policy as `kitamura96.py`: no matrices or
Lean file redistributed, SHA-256 checked before parsing, NOT_RUN without
KITAMURA96_DATA. It is optional and not in the fast default runner.

```bash
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 \
KITAMURA96_DATA="$PWD/.external/kitamura96-Data.lean" \
.venv/bin/python -m coupled_ame.kitamura96_exact
```

The verifier constructs exponent tensors in memory and writes only a small JSON
summary with126 cut records per case. No dense tensors or large intermediate
files are written. A few hundred MB of RAM are required. Existing documented
external-data retrieval applies; no network operation is built into this module.

For w=exp(i*pi/3), every unnormalized marginal entry belongs to Z[w];
|a+b*w|²=a²+ab+b² is an integer, so nonzero entries have modulus>=1.
A floating residual<1/2 proves zero only together with a sufficient arithmetic
error bound. Claude's historical floating check reported a largest residual
4.249045559845399e-12 and18 failing negative-control cuts. We strengthen its
acceptance calculation to exact integer coefficients rather than rely on an
unproved BLAS/transcendental error estimate.

Represent each root as (r+i*sqrt(3)*s)/2 with
r=(2,1,-1,-2,-1,1), s=(0,1,1,0,-1,-1). On a cut,
4R=rr^T+3ss^T+i*sqrt(3)*(sr^T-rs^T).
The float64 matrix products now multiply/add only integers: each dot product
has7776 terms of magnitude<=4, hence every product and partial sum is exactly
representable in IEEE binary64 (well below2^53), including FMA evaluation.
All subsequent combinations are also small integers. Thus this computation is
exact integer arithmetic implemented with binary64 BLAS, not tolerance-based
acceptance. Positive cuts require real coefficient4*7776*I and imaginary
coefficient0 exactly; the negative control must fail18 cuts. This is a direct
coefficient version of the Z[w] gap certificate, independent of the existing
826560 signed-difference acceptance mechanism. No Lean build is claimed.

The article audit's small-instance symbolic checks corroborate, but do not
replace, general Cauchy/RS arguments, Rains identities or attributed results.
Clifford lift signs and completeness remain scoped to the original companion
certificates and factorwise Clifford class. The nine-party proof now primarily
uses the independently checked six graph inputs plus the general RS argument;
Grassl–Rötteler is attribution/consistency, not a required premise.
