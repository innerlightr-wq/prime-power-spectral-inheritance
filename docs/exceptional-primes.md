# Exceptional Primes: Wieferich-Type Order Stalling

**Updated for the unconditional theorem.** An earlier version of this document described Wieferich-prime order-stalling as a condition that could make the paper's main theorems *fail* at a specific prime-power step. That is no longer correct, and is not a claim this document repeats. The current paper (`paper/main.tex`) proves the intertwining and splitting theorems **unconditionally, at every step, for every prime `p ∤ ab`** — no order-lifting hypothesis is needed at all (see `theorem-audit.md`, Stage 5, for how this was discovered). Wieferich-type order stalling now plays a purely **descriptive** role: it determines the *shape* of the increment ladder (how many fine increments combine to reproduce one coarse matrix entry), not whether the theorems hold.

## The condition, precisely

For `p ∤ a`, standard lifting-the-exponent theory gives `ord_{p²}(a) ∈ {ord_p(a), p·ord_p(a)}` — exactly one of the two. Since `ord_p(a) | p−1` (Fermat) and `p·ord_p(a) ≥ p > p−1`, only the first option can divide `p−1`. Hence:

> **`a^(p−1) ≡ 1 (mod p²)` ⟺ `ord_{p²}(a) = ord_p(a)`.**

These are the same condition (the classical "Fermat quotient" form, and the "order-stall" form), proved equivalent in general. The paper's Proposition ("Order-lifting schedule") extends this with the lifting-the-exponent lemma to give the *exact* schedule at every level: writing `w_p(b) := v_p(b^{p-1}-1)` for the "Wieferich depth," `ord_{p^e}(b) = ord_p(b)` for `e ≤ w_p(b)` and `= ord_p(b)·p^{e-w_p(b)}` for `e ≥ w_p(b)`. Equivalently, in the paper's notation `c_e := r_{e+1}/r_e`: `c_e = 1` for `e < w_p(b)` and `c_e = p` for `e ≥ w_p(b)`.

## The key structural insight: separate `c_e` from `m_e`

The paper's Lemma ("Ladder versus fiber") shows `c_e = |B_{e+1} ∩ ker π_e|`, a divisor of the fiber size `m_e = |ker π_e| ∈ {1,p}`, with exactly three realizable combinations: `(c_e,m_e) = (p,p)`, `(1,p)`, `(1,1)` — never `(p,1)`. **The old (superseded) version of this research assumed `c_e=m_e=p` always** (hypothesis "H1"), which only holds generically. The new Lemma ("Increment ladder") shows the geometric-series telescoping that proves intertwining works identically regardless of which case obtains: when `c_e=1`, each target simply receives **one** fine increment carrying the full coarse weight directly, instead of `p` increments summing geometrically — the coarse entry is still reproduced exactly either way (see the paper's Remark "Stalled steps").

## `p = 11`, Wieferich base 3

`3^10 ≡ 1 (mod 121)`. One of exactly two known base-3 Wieferich primes (the other, `1006003`). `ord_11(3) = 5`; `ord_121(3) = 5` (stall, `w_11(3)=2`), then resumes generic lifting (`ord_1331(3) = 55`, etc.).

At `p=11`, `w_11(2)=1`, so the *resolution-base* ladder (`c_e` for `b=2`) grows generically at every level — this prime's anomaly is entirely in the *multiplier* channel (`a=3`), which does not enter the hypothesis of any theorem (the theorems now have no hypothesis at all, and in the earlier, conditional version, the hypothesis was specifically about `ord(2)`, never `ord(3)`). The anomaly may still influence the internal numerical values of the primitive-stratum operators — the previously observed multi-level transient in `P_11(e)` before freezing is consistent with this — but it was never a threat to inheritance, under either the old or new form of the theorem.

## `p = 1093`, Wieferich base 2

`2^1092 ≡ 1 (mod 1093²)`. The smaller of the two known base-2 Wieferich primes (`1093`, `3511`). `ord_1093(2) = ord_1093²(2) = 364` (stall at `e=1→2`, `w_1093(2)=2`); `ord_1093³(2) = 364×1093` (resumes).

**This is now the paper's worked example of a genuine `c_e=1` step — not a counterexample or a boundary of validity.** The group `K_2=⟨2,3⟩` still grows by the generic factor `1093` at this step (`|K_1|=364`, `|K_2|=397,852`), so `(c_e,m_e)=(1,1093)` — exactly the middle case of Lemma "Ladder versus fiber," and the kernel of the reduction map is identified exactly: `3^7 = 2187 = 2·1093+1 ≡ 1 (mod 1093)` but `3^7 ≢ 1 (mod 1093²)`, so `3^7` is a nontrivial element of the (prime-order, hence cyclic) kernel, and generates it. The splitting and monotonicity theorems hold at this step exactly as at every other — confirmed by a direct, from-scratch, 900-sample entrywise check (`src/unconditional_splitting_check.py`), since the full `397,852`-dimensional matrix is too large to build outright.

## Doubly anomalous primes

A prime anomalous in *both* channels of the Collatz pair would need `w_p(2) ≥ 2` and `w_p(3) ≥ 2`. Checked directly: `w_1093(3) = w_3511(3) = 1` (neither known base-2 Wieferich prime below `6.7×10^15` is also anomalous for base 3). This is a search bound, not an impossibility proof — but by the unconditional theorem, no doubly anomalous prime (if one exists) would threaten inheritance in any case.

## What was *not* pursued

Whether the same mechanism extends beyond odd prime powers (the paper's final numerical remark notes supporting exact checks on towers of powers of `2` and on composite moduli, without formulating or proving the general statement) is left as a natural, explicitly flagged open direction.
