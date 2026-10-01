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

## Stage 5 — Removing the order-lifting hypothesis entirely

Stages 2–4 all carried a standing hypothesis ("H1"): the order of the resolution base `b=2` lifts generically, `ord_{p^{e+1}}(2) = p·ord_{p^e}(2)`, at every step considered. This was known to fail at a concrete prime (`p=1093`, Section on exceptional primes), and the theorems were understood to apply only where it held.

Re-examining the proof's actual mechanism — specifically, separating two quantities that coincide *generically* but are logically independent: the **ladder growth** `c_e := r_{e+1}/r_e` (how much the order of `b` itself lifts) and the **fiber size** `m_e := |K_{e+1}|/|K_e|` (how much the whole group grows) — showed that the geometric-series telescoping underlying the intertwining proof only ever uses the identity `r_{e+1} = c_e·r_e`, which holds **by definition of `c_e`, unconditionally**, regardless of whether `c_e` equals `m_e` (the generic case, `H1`) or `c_e=1<m_e` (a stall). A new, more general lemma ("Increment ladder") shows the same telescoping sum collapses to the correct coarse weight in *either* case — when `c_e=1`, each target simply receives one fine increment carrying the full weight directly, instead of `p` increments summing geometrically.

**Consequence: the intertwining theorem, the splitting theorem, and the monotonicity theorem all hold unconditionally, at every prime-power step, for every prime `p∤ab` — hypothesis (H1) is not needed at all.** This was independently verified (not merely accepted on the strength of the proof): a from-scratch combinatorial check of the core lemma found zero mismatches on every spot-tested case, including the key `p=11` role-swap stall (`c_e=1, m_e=11`); a large sweep across thousands of `(p,a,b,e)` combinations (`src/large_sweep_corroboration.py`) found zero mismatches and reproduced all three realizable `(c_e,m_e)` types (`(p,p)`, `(1,p)`, `(1,1)` — never `(p,1)`, confirmed as a proved impossibility); and a sampled entrywise check at `p=1093` (too large to build in full) found zero mismatches across 900 sampled entries.

This is a strengthening, not merely a correction: the earlier conditional theorems were not wrong, only unnecessarily narrow — the extra hypothesis was never actually load-bearing in the proof, once the right quantity (`c_e`, not `m_e`) was identified as the one the telescoping argument depends on.

## What remains genuinely open after Stage 5

The *fine-grained* version of dominance — does a **specific** non-primitive stratum's new-sector operator ever exceed its **own local** inherited value? — is not resolved, and is not needed for the monotonicity theorem (which only needs one safe witness, not dominance at every stratum). This is recorded as the paper's Open Problem, unaffected by the removal of (H1).

## Lessons drawn from this history

A claim ("not reducing") was asserted in Stage 2 based on a general fact about block-upper-triangular matrices, without checking whether the specific off-diagonal block here was actually nonzero. It was not. The lesson, stated plainly: **check specific structural claims directly, even when a general heuristic argument suggests they should be true or false — the heuristic was wrong here.**

A second, independent lesson from Stage 5: a hypothesis (H1) was carried through three stages of this research as apparently load-bearing, because it held in every case actually computed and because the natural first proof of the telescoping identity used it directly. It was not, in fact, necessary — only a *particular instance* (`c_e=m_e`) of a more general identity (`r_{e+1}=c_e r_e`) that holds unconditionally. **A hypothesis that happens to hold in every tested case is not evidence that the hypothesis is necessary** — it is worth periodically asking, of any standing assumption in a proof, whether the argument actually uses the full strength of the assumption or only a weaker consequence of it that might hold more generally.
