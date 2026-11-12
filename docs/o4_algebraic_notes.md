All statements below are exact mathematical deductions. They are not numerical evidence, and no novelty claim is made.

**The general-rank LP used here.** For a density matrix rho, set a_j=sum_{wt E=j}(tr E rho)^2 and b_j=sum_{wt E=j}tr(E rho E rho), with Hermitian, unsigned Pauli E. Then a_0=1, a_j>=0, b=2^-13 a(x+3y,x-y). The shadow transform 2^-13 a(x+3y,y-x) is nonnegative: it is the analogous sum of overlaps between rho and Pauli-conjugates of its positive spin-flip. If rank(rho)<=r, Cauchy-Schwarz on the support gives (tr E rho)^2 <= r tr(E rho E rho). For any subset S, purifying rho into an r-dimensional reference and applying the Hilbert-Schmidt partial-trace bound gives tr rho_{S^c}^2 <= r tr rho_S^2. Summing these inequalities over equal-sized subsets produces the exact rows in o4_lp_certificates.json. The remaining constraints are tr rho^2<=1 and tr rho_S^2<=1. The rational Farkas sums exclude r=8 and r=5. Because these necessary inequalities weaken with increasing r, the r=8 certificate excludes all ranks 1,...,8, without a flat-spectrum assumption. Consequently any six-uniform stabilizer projector has rank at least 16.

**Nine-qubit certificate (for Appendix F.3).** Every four-uniform nine-qubit density matrix has rank at least four, without a flat-spectrum assumption. Here is a certificate that can be checked without the JSON or an LP solver.

For unsigned Hermitian Pauli strings E, define
\[
a_i=\sum_{\operatorname{wt}(E)=i}(\operatorname{tr}E\rho)^2,
\qquad b_j=\sum_{\operatorname{wt}(E)=j}\operatorname{tr}(E\rho E\rho).
\]
Four-uniformity gives a_0=1 and a_1=...=a_4=0. Set
\[
K_j(i)=[z^j](1+3z)^{9-i}(1-z)^i,
\qquad b_j=2^{-9}\sum_{i=0}^9K_j(i)a_i,
\qquad s_j=2^{-9}\sum_{i=0}^9(-1)^iK_j(i)a_i.
\]
The shadow coefficients s_j are nonnegative: they equal sums of
tr(E rho E tilde(rho)), where tilde(rho)=Y^{\otimes9} rho^T Y^{\otimes9}
is positive. If rank(rho)<=3, Cauchy-Schwarz on its support gives
3b_j-a_j>=0. Also, purification into a reference of dimension at most
three gives tr(rho_{S^c}^2)<=3 tr(rho_S^2). Summing this last inequality
over all seven-site subsets, and multiplying by 2^7, gives
\[
T_7=3\sum_{i=0}^7\binom{9-i}{7-i}a_i
       -\sum_{j=0}^7\binom{9-j}{7-j}b_j\ge0.
\]
Consequently the following six quantities are nonnegative:
\[
\begin{aligned}
g_1=512s_0&=1-a_5+a_6-a_7+a_8-a_9,\\
g_2=512(3b_1)&=81+21a_5+9a_6-3a_7-15a_8-27a_9,\\
g_3=512s_1&=27-7a_5+3a_6+a_7-5a_8+9a_9,\\
g_4=128(3b_2)&=243+3a_5-9a_6-9a_7+3a_8+27a_9,\\
g_5=128s_2&=81-a_5-3a_6+3a_7+a_8-9a_9,\\
g_6=T_7&=-1044+18a_5+9a_6+3a_7.
\end{aligned}
\]
But direct addition gives the contradiction
\[
0\le27g_1+g_2+9g_3+5g_4+18g_5+4g_6=-1152.
\]
Thus rank(rho)>=4. In the zero-based row ordering of
`coupled_ame/general_rank.py`, this is the certificate supported on rows
1,2,3,4,5,35, with multipliers (3456,128,1152,160,576,1)/5473;
all five combined variable coefficients vanish and the combined right-hand
side is -288/5473. These rows also agree with the original research record
`lambda13_20261021/n04_results/binary9_rank_bound.json`.
The exact point (a_5,...,a_9)=(18,36,36,27,10) satisfies the necessary
inequalities at rank four; feasibility alone does not establish a state.
Replay with `python -m coupled_ame.general_rank`.

**Parent and coupling.** Let G be a symmetric, zero-diagonal prime-field graph on 14 vertices. A graph state's reduction across a cut S is maximally mixed exactly when G[S,S^c] has full row rank. This follows by summing the complementary coordinates in the graph-state density matrix: finite-field character orthogonality kills every nonzero difference on S precisely when the cross map has trivial kernel. All 7|7 cuts of the displayed p=13 graph pass exact elimination, so the parent is AME(14,13).

Write |G>=p^-1/2 sum_a |a>|v_a>, conditioning vertex 0 in the computational basis. The reduction on reference vertex 0 and any physical six-set S equals I/p^7. Comparing its (a,b) matrix blocks gives Tr_{S^c}|v_a><v_b|=delta_ab I/p^6, including normalization and orthogonality. For arbitrary normalized binary u_a, not assumed orthogonal, and nonnegative weights summing to one, the coupled state's S reduction is rho_S tensor I/p^6, where rho=sum_a lambda_a|u_a><u_a|. Thus coupling is AME iff rho is six-uniform. Conversely any rho of rank at most p has a spectral decomposition using at most p branches, so the verified p=13 parent supplies the converse needed for this particular coupling route. Quantum Singleton gives K<=p for any pure ((13,K,7))_p code: the reference entropy is at most the log-dimension of the single site remaining after two disjoint six-site erasures. The exact finite parent suffices; no separate Reed-Solomon existence theorem is needed.

**Graph diagonal states and affine support.** For graph generators g_i=X_i product_j Z_j^{G_ij}, graph-basis label x has eigenvalue (-1)^{w.x} on g_w. Every Pauli outside this maximal stabilizer group has zero diagonal in this basis. Therefore six-uniformity is exactly lambda_hat(w)=0 for all nonzero w whose physical g_w has weight at most six. If the positive support is contained in x0+L, each w in L^perp has lambda_hat(w)=(-1)^{w.x0}. Hence L^perp has no nonzero low-weight word and defines a rank-2^m six-uniform stabilizer code, m=dim L. The rank LP implies m>=4.

For each coset modulo L^perp, a low-weight representative forces the corresponding Fourier coefficient on L to vanish (the shift and stabilizer signs multiply it by a nonzero sign). Call a coset clean if it contains no nonzero weight-1,...,6 word. A subspace H of clean cosets lifts to a commuting subgroup of dimension 13-m+dim H, still with minimum weight at least seven. Thus dim H<=m-4. At m=4 every nonzero coset is dirty, so Fourier inversion forces all 16 probabilities to be 1/16. This includes arbitrary real nonnegative weights. A uniform selection has even cardinality because at least one low-weight graph stabilizer exists and its zero expectation requires equal numbers of +/- signs.

In fact, for *any* six-uniform rank-16 stabilizer code, its maximally mixed state is the only six-uniform density matrix supported in its code space. If a nonidentity logical Pauli coset were clean, adjoining its representative would give a forbidden rank-8 six-uniform stabilizer code. Thus every logical Pauli coefficient is forced to zero, even for non-diagonal density matrices.
