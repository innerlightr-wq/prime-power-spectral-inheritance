# prime-power-spectral-inheritance

**Exact spectral inheritance in prime-power resolution towers: a splitting theorem for affine-cocycle transfer operators, with application to the Collatz carry sum.**

Elias De Jesús · Independent Researcher · ORCID [0009-0007-0190-9143](https://orcid.org/0009-0007-0190-9143) · `dejesuselias10@gmail.com`

## What this is

For a prime power `q = p^e`, the accelerated Collatz carry sum generates a multiplicative walk on `K_e = ⟨2,3⟩ ≤ (ℤ/qℤ)ˣ` and a family of phase-twisted transfer operators `L_{e,t,x}` whose dominant twisted eigenvalue controls the rate of equidistribution of carry-sum residues at a fixed prime `p` (see the `amgap` instrument and the two prior technical notes cited in `paper/main.tex`). This repository contains a self-contained proof that the natural resolution map between consecutive prime-power levels `p^e → p^{e+1}` doesn't just embed the coarser operator inside the finer one — it **splits it exactly, as an orthogonal direct sum, at every step, for every prime, with no arithmetic hypothesis**. That upgrades a previously-conditional monotonicity claim about the equidistribution spectral gap `g_0(p,e)` to an unconditional theorem, valid from `e=1`.

The theorem and its proof are stated and proved for a **generic affine-cocycle operator family** (any coprime `a,b ≥ 2`, any prime `p ∤ ab`) — the Collatz instance `(a,b)=(3,2)` is the motivating case, not a hypothesis of anything proved here. An earlier version of this result needed an extra hypothesis on multiplicative-order lifting; it was removed by separating two quantities (the order-lifting ratio `c_e` and the fiber size `m_e`) that coincide generically but are logically independent — see `docs/theorem-audit.md`, Stage 5.

## Main results

| | Statement | Status |
|---|---|---|
| Lemma (ladder vs. fiber) | `c_e := r_{e+1}/r_e` divides `m_e := |K_{e+1}|/|K_e|`; both lie in `{1,p}`; `(c_e,m_e)=(p,1)` never occurs | Proved |
| Theorem (intertwining) | `L_{e+1} J_e = J_e L_e`, at **every** step `e≥1`, no hypothesis | Proved (generic) |
| Theorem (splitting) | Exact orthogonal splitting `L_{e+1} ≅ L_e ⊕ N_{e+1}`, at every step | Proved (generic) — corrects an earlier, weaker "invariant but not reducing" claim |
| Theorem (monotonicity) | `g_0(p,e)` is non-increasing from `e=1`, hence convergent, for every prime `p ∤ ab` | Proved (generic, unconditional) |
| Proposition (order-lifting schedule) | By lifting-the-exponent: `ord_{p^e}(b) = ord_p(b)` for `e ≤ w_p(b)` and `×p^{e-w_p(b)}` beyond, where `w_p(b):=v_p(b^{p-1}-1)` — this governs the *shape* of the increment ladder, not whether the theorems hold | Proved |
| Open Problem | Does a non-primitive stratum's new-sector operator ever exceed its own local inherited eigenvalue? | **Open** |

See `paper/main.tex` / `paper/main.pdf` for the full statements and proofs, `docs/theorem-audit.md` for the full derivation trail (including a documented self-correction), `docs/exceptional-primes.md` for the number-theoretic content (Wieferich primes base 2 and base 3), and `docs/computational-notes.md` for an honest account of what numerical methods worked and which failed.

## Repository layout

```
paper/        main.tex, main.pdf, LICENSE (CC BY 4.0)  — the technical note (self-contained inline bibliography)
src/          verification scripts (exact/symbolic + numerical), all reproducible — Apache 2.0
docs/         theorem-audit.md, computational-notes.md, exceptional-primes.md
```

## Reproducing the verification

Requires Python 3 with `numpy`, `scipy`, `sympy`. From `src/`:
```
python3 splitting_theorem_check.py        # exact/symbolic verification of the splitting theorem
python3 monotonicity_check.py             # verification of the monotonicity theorem's eigenvalue-union formula
python3 wieferich_check.py                # Fermat-quotient ⟺ order-stall equivalence, p=11 and p=1093, order-lifting tables
python3 generic_multiplier_control.py     # splitting theorem for a non-Collatz control, (a,b)=(5,2)
python3 independent_reimplementation.py   # separate from-scratch implementation backing an earlier revision's
                                           # specific numerical claims (p=5,11,13 at x*; p=7,13 at x=0.37)
python3 unconditional_splitting_check.py  # all "Targeted controls" of paper Sec. 6 (role swap / stalled steps,
                                           # a depth-3 synthetic stall, the trivial-new-sector m_e=1 case, and
                                           # the p=1093 sampled-entry check, since its full matrix is too large to build)
python3 large_sweep_corroboration.py      # independent large-scale sweep (thousands of (p,a,b,e) steps, zero
                                           # mismatches, all three realizable (c_e,m_e) types) corroborating —
                                           # though not reproducing bit-for-bit, see the script's own header — the
                                           # scale of the paper's reported 3,134-step exact-arithmetic audit
```
All scripts print their own pass/fail checks; the two large sweeps take up to a few minutes, the rest run in seconds.

## Scope — what is *not* claimed

This note is about the statistical/spectral structure of the carry-sum residue system only. **It says nothing about Collatz cycle closure, divergence, or the Collatz conjecture itself.** The underlying negative result for those questions (that prime-power residue layers only ever give a one-sided necessary filter, never a sufficient one, for exact Collatz closure) was established in earlier, separate work and is not revisited here.

## License

This repository is dual-licensed, matching the author's standard convention for software-plus-manuscript deposits:
- **Manuscript** (`paper/main.tex`, `paper/main.pdf`): [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) (CC BY 4.0) — see `paper/LICENSE`.
- **Code** (`src/`, and the repository infrastructure generally): [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) — see `LICENSE`.

Please cite via `CITATION.cff`. The manuscript is additionally deposited on Zenodo; the DOI will be added here and to `CITATION.cff` once assigned.
