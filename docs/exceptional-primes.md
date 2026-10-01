# Exceptional Primes: Wieferich-Type Order Stalling

## The condition, precisely

For `p ∤ a`, standard lifting-the-exponent theory gives `ord_{p²}(a) ∈ {ord_p(a), p·ord_p(a)}` — exactly one of the two. Since `ord_p(a) | p−1` (Fermat) and `p·ord_p(a) ≥ p > p−1`, only the first option can divide `p−1`. Hence:

> **`a^(p−1) ≡ 1 (mod p²)` ⟺ `ord_{p²}(a) = ord_p(a)`.**

These are the same condition (the classical "Fermat quotient" form, and the "order-stall" form), proved equivalent in general — not just checked to coincide for a specific prime. Verified directly in `src/wieferich_check.py`, including negative controls (primes that are *not* Wieferich for a given base, to confirm the check correctly distinguishes the exceptional cases).

## `p = 11`, Wieferich base 3

`3^10 ≡ 1 (mod 121)`. One of exactly two known base-3 Wieferich primes (the other, `1006003`, is far too large for the computational framework used here). `ord_11(3) = 5`; this order **fails to lift** from level 1 to level 2 (`ord_121(3) = 5`, not `55`), then **resumes generic lifting** from level 2 onward (`ord_1331(3) = 55 = 11×5`, etc.).

**Does this threaten the paper's main theorems?** No. Hypothesis (H1) is specifically about `ord_{p^e}(2)` — and at `p=11`, `2`'s order lifts generically at *every* tested level (`10 → 110 → 1210 → 13310 → 146410`, each exactly `×11`). The splitting and monotonicity theorems apply to `p=11` unconditionally throughout. The Wieferich-3 anomaly instead perturbs the internal structure of the *primitive*-stratum operator (which has no inherited part to split against, since it doesn't reduce to any lower level) — it is the reason the specific numerical values `P_11(e)` show an unusual multi-level rise-then-fall pattern before freezing, a phenomenon the splitting theorem does not explain (and was not trying to).

## `p = 1093`, Wieferich base 2

`2^1092 ≡ 1 (mod 1093²)`. The smallest known base-2 Wieferich prime (the next, `3511`, is also known but not used here). `ord_1093(2) = 364`; **this order fails to lift** from level 1 to level 2 (`ord_1093²(2) = 364`, not `364 × 1093`).

**Does this threaten the theorems?** Yes, precisely at the step `e=1 → 2`, and this is the paper's worked example of the hypothesis genuinely failing. A subtlety worth recording: the *group* `K_e = ⟨2,3⟩` still grows by the generic factor `p = 1093` at this step (`|K_2| = 364 × 1093`, confirmed directly) — because `3` is not simultaneously anomalous and compensates for `2`'s stall. **This does not rescue the splitting theorem's proof**, because the geometric-series telescoping at the heart of the proof is tied specifically to `ord(2)`'s own lifting (the weight denominator `1 − x^r`, `r = ord(2)`), not to the group's overall size. This is exactly the distinction the paper's Section 6 makes: hypothesis (H1) is the correct, minimal, non-redundant condition — not a stand-in for "the group doesn't shrink."

## What was *not* pursued

Whether an alternative proof of the splitting/monotonicity theorems exists at `p=1093` using a combined `2`-and-`3` shift structure (since `3` is not itself anomalous there) is a natural follow-up question, explicitly left open. It would require re-deriving the core telescoping argument in a genuinely two-generator (non-cyclic-in-`2`-alone) setting — a different and nontrivial undertaking, out of scope for this repository.
