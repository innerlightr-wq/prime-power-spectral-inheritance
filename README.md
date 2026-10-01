# prime-power-spectral-inheritance

**Exact spectral inheritance in prime-power resolution towers: a splitting theorem for affine-cocycle transfer operators, with application to the Collatz carry sum.**

Elias De Jesús · Independent Researcher · ORCID [0009-0007-0190-9143](https://orcid.org/0009-0007-0190-9143) · `dejesuselias10@gmail.com`

## What this is

For a prime power `q = p^e`, the accelerated Collatz carry sum generates a multiplicative walk on `K_e = ⟨2,3⟩ ≤ (ℤ/qℤ)ˣ` and a family of phase-twisted transfer operators `L_{e,t,x}` whose dominant twisted eigenvalue controls the rate of equidistribution of carry-sum residues at a fixed prime `p` (see the `amgap` instrument and the two prior technical notes cited in `paper/main.tex`). This repository contains a self-contained proof that the natural resolution map between consecutive prime-power levels `p^e → p^{e+1}` doesn't just embed the coarser operator inside the finer one — it **splits it exactly, as an orthogonal direct sum**. That upgrades a previously-conditional monotonicity claim about the equidistribution spectral gap `g_0(p,e)` to a theorem, proved at every step satisfying one precisely-characterized arithmetic hypothesis (H1).

The theorem and its proof are stated and proved for a **generic affine-cocycle operator family** (any coprime `a,b ≥ 2`, any prime `p ∤ ab`, one checkable hypothesis on multiplicative-order lifting) — the Collatz instance `(a,b)=(3,2)` is the motivating case, not a hypothesis of anything proved here.

## Main results

| | Statement | Status |
|---|---|---|
| Theorem (intertwining) | `L_{e+1} J_e = J_e L_e`, under hypothesis (H1) | Proved (generic) |
| Theorem (splitting) | Exact orthogonal splitting `L_{e+1} ≅ L_e ⊕ N_{e+1}` | Proved (generic) — corrects an earlier, weaker "invariant but not reducing" claim |
| Theorem (monotonicity) | `g_0(p,e)` is non-increasing, hence convergent, at every step where (H1) holds | Proved (generic, under (H1)) |
| Proposition (where (H1) holds) | By lifting-the-exponent: `ord_{p^e}(b)` lifts generically for all `e ≥ w_p(b) := v_p(b^{p-1}-1)`; monotonicity therefore holds eventually for *every* prime `p ∤ 6`, and from `e=1` for every non-Wieferich prime | Proved |
| Open Problem | Does a non-primitive stratum's new-sector operator ever exceed its own local inherited eigenvalue? | **Open** |

See `paper/main.tex` / `paper/main.pdf` for the full statements and proofs, `docs/theorem-audit.md` for the full derivation trail (including a documented self-correction), `docs/exceptional-primes.md` for the number-theoretic content (Wieferich primes base 2 and base 3), and `docs/computational-notes.md` for an honest account of what numerical methods worked and which failed.

## Repository layout

```
paper/        main.tex, main.pdf  — the technical note (self-contained inline bibliography)
src/          verification scripts (exact/symbolic + numerical), all reproducible
docs/         theorem-audit.md, computational-notes.md, exceptional-primes.md
```

## Reproducing the verification

Requires Python 3 with `numpy`, `scipy`, `sympy`. From `src/`:
```
python3 splitting_theorem_check.py        # exact/symbolic verification of the splitting theorem
python3 monotonicity_check.py             # verification of the monotonicity theorem's eigenvalue-union formula
python3 wieferich_check.py                # Fermat-quotient ⟺ order-stall equivalence, p=11 and p=1093, order-lifting tables
python3 generic_multiplier_control.py     # splitting theorem for a non-Collatz control, (a,b)=(5,2)
python3 independent_reimplementation.py   # separate from-scratch implementation backing paper Sec. 5's
                                           # specific numerical claims (p=5,11,13 at x*; p=7,13 at x=0.37)
```
All scripts print their own pass/fail checks; none requires more than a few seconds to run.

## Scope — what is *not* claimed

This note is about the statistical/spectral structure of the carry-sum residue system only. **It says nothing about Collatz cycle closure, divergence, or the Collatz conjecture itself.** The underlying negative result for those questions (that prime-power residue layers only ever give a one-sided necessary filter, never a sufficient one, for exact Collatz closure) was established in earlier, separate work and is not revisited here.

## License

Apache License 2.0 — see `LICENSE`. Please cite via `CITATION.cff`.
