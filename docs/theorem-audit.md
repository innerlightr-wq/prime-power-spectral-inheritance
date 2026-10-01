# Theorem Audit Trail

This document records the derivation history honestly, including a self-correction, so a reader can see exactly how the final theorems were reached rather than only their final form.

## Stage 1 — Numerical motivation

The `amgap` instrument (companion to `Fixed-Prime Equidistribution of Accelerated Collatz Carry Sums`) reported `g_0(11,1)=0.3340`, `g_0(11,2)=0.3225` and flagged the prime-power generalization (`e > 1`) as an open "central experiment." Independent extension computed `g_0(11,3)≈0.305`, apparently continuing a downward trend.

## Stage 2 — First structural analysis (superseded in part)

A first pass found that characters `t` with `gcd(t,p^e)=p^j` factor exactly through the quotient `ℤ/p^eℤ → ℤ/p^{e-j}ℤ`, and that the fiber-constant subspace is **invariant** under the finer-level operator. This gave a one-directional inequality: the inherited eigenvalue is a lower bound on the stratum's full spectral radius, but **not** necessarily an equality — the possibility that the orthogonal complement might contribute a *larger* eigenvalue was flagged as open ("Hypothesis D: dominance"), and the resulting monotonicity claim for `g_0(p,e)` was downgraded from "proved" to "conditional on an unproven hypothesis."

**At this stage it was also asserted, without being directly checked, that the invariant subspace is "not reducing"** — i.e. that the orthogonal complement is not itself invariant. This claim turned out to be wrong (Stage 3).

## Stage 3 — The splitting theorem (this repository's central result)

Investigating the fiber decomposition directly (rather than reasoning generically about non-normal operators), a **dual pushforward intertwining** was found: the fiber-sum map `S_e` also intertwines exactly, `S_e L_{e+1} = L_e S_e`. This was *not* a new computation in substance — it is the same telescoping identity used for the original pullback intertwining, read for a different fixed index — but it had not been noticed to also prove invariance of `Z_{e+1} = ker(S_e)`, the **exact orthogonal complement** of the inherited subspace.

Verifying this directly (exact symbolic arithmetic, `src/splitting_theorem_check.py`) confirmed it holds for primitive *and* non-primitive source residues, for multiple primes, and for a non-Collatz control multiplier. The consequence is an **exact orthogonal direct-sum splitting**, not merely an invariant-subspace embedding — correcting Stage 2's "not reducing" claim.

## Stage 4 — Monotonicity resolved unconditionally

With the exact formula `ρ(L_{e+1,pt)}) = max(ρ(L_{e,t}), ρ(N_{e+1,pt}))` (not an inequality) in hand, a direct argument proves `B_p(e+1) ≥ B_p(e)` unconditionally: lift *whichever* residue achieved the historical maximum at level `e`; the exact formula guarantees the lift's spectral radius is at least that maximum. No dominance hypothesis is needed — the earlier open problem (Stage 2) is bypassed, not solved by a separate proof of dominance.

## What remains genuinely open after Stage 4

The *fine-grained* version of dominance — does a **specific** non-primitive stratum's new-sector operator ever exceed its **own local** inherited value? — is not resolved, and is not needed for the monotonicity theorem (which only needs one safe witness, not dominance at every stratum). This is recorded as the paper's Open Problem.

## Lesson drawn from this history

A claim ("not reducing") was asserted in Stage 2 based on a general fact about block-upper-triangular matrices, without checking whether the specific off-diagonal block here was actually nonzero. It was not. The lesson, stated plainly: **check specific structural claims directly, even when a general heuristic argument suggests they should be true or false — the heuristic was wrong here.**
