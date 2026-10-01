# Computational Notes: What Worked, What Didn't, and Why

This research relied on computation for two distinct purposes — **verifying exact algebraic identities** (small cases, exact arithmetic, which worked reliably) and **pushing numerical chronologies to larger prime-power levels** (which repeatedly ran into real, instructive failures). Both are recorded honestly here, since the failures shaped the final theoretical results.

## What worked reliably

- **Exact symbolic verification** (`sympy`, rational/exact arithmetic) of the splitting theorem, the intertwining identity, and the generic-multiplier control — all in `src/`. These scale to matrix dimensions of a few hundred in reasonable time; beyond roughly `n≈500`, `sympy.simplify` on dense symbolic matrices becomes impractical (see the trimmed test case in `splitting_theorem_check.py`).
- **Dense LAPACK eigendecomposition** (`numpy.linalg.eigvals`) for numerical cross-checks up to `n≈2000–6000`, at the cost of real wall-clock time (a single `n≈6500` case took over 7 minutes and was abandoned as impractical in an earlier phase of this research).
- **Exact modular arithmetic** (Python's built-in arbitrary-precision integers) for every number-theoretic claim (Wieferich conditions, multiplicative orders) — these are exact, not floating point, and have no precision caveats.

## What failed, and why — recorded because the failure was informative, not just an obstacle

**Naive single-vector power iteration** failed outright, even at the smallest nontrivial case (`p=11, e=1`, dimension 10), converging to a visibly wrong value after 3000 iterations. Diagnosis: the dominant eigenvalue at this instance is an **exact-magnitude, non-real complex-conjugate pair** — a textbook obstruction to power iteration, since the iterate's direction rotates indefinitely around the two-dimensional dominant eigenspace instead of converging.

**Block subspace iteration** (a hand-rolled mini-Arnoldi method, block size 8) was built specifically to handle this degeneracy. It reproduced the correct value at the smallest case but **degraded badly at larger sizes** — even the *exactly known* untwisted eigenvalue `λ_0 = log₂3 − 1` (true at every level, by a closed-form proof) came back wrong by level `e=3–5`, indicating the iteration had not converged within the budget used, not that the method is wrong in principle.

**`scipy.sparse.linalg.eigs` (ARPACK)**, requesting several eigenvalues simultaneously (better-suited to resolving a degenerate pair than single-vector iteration), still showed unreliable convergence at matrix dimensions in the low thousands for this specific non-normal operator family.

**The methodological lesson, stated for anyone extending this work**: *a numerical method can produce a plausible-looking, non-obviously-wrong floating-point number and still be completely incorrect.* The only reason this was caught was that one quantity in this problem (`λ_0`) has an independent closed-form value to check against. **Always validate a new numerical method against a quantity with a known closed form before trusting its output on quantities that do not have one.** No value from power iteration or subspace iteration beyond the smallest verified cases is reported anywhere in this repository's claims — they were computed, found unreliable, and discarded rather than reported with a caveat.

## Practical ceiling, as of this work

Reliable (dense, exact, or properly-converged sparse) spectral computation for this operator family tops out, in practice, around matrix dimension `10,000–15,000` within a single working session on ordinary hardware. Extending the numerical chronologies (e.g. `p=11` beyond `e=4`) would require either a correctly-tuned, degeneracy-aware eigensolver (shift-invert Arnoldi targeting a known approximate eigenvalue region, with explicit deflation of known degenerate pairs) or substantially more compute time — neither was pursued further, since the theoretical results in `paper/main.tex` resolve the question (monotonicity of `g_0`) that the numerical chronology was originally being extended to answer.
