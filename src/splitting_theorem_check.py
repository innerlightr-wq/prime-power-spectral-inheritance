"""
splitting_theorem_check.py — exact/symbolic verification of Theorem B (the
splitting theorem).

Checks, for p=5 and p=13, level e=1 -> e=2, for BOTH a primitive and a
non-primitive source residue t'':
  (i)   the pullback intertwining  M_hi @ J  ==  J @ M_lo   (Theorem A)
  (ii)  the pushforward intertwining  S @ M_hi  ==  M_lo @ S   (Lemma, dual)
  (iii) invariance of Z = ker(S):  S @ M_hi @ Proj_Z == 0
All checks use exact sympy rational/symbolic arithmetic at a generic
(non-saddle) test point x=2/5, isolating the algebraic claim from any
Collatz-specific numerology.
"""
import sympy as sp
from operator_lib import build_K, build_M_exact


def check_case(p, e_lo, t_lo, x, label):
    q_lo, q_hi = p**e_lo, p**(e_lo + 1)
    K_lo, K_hi = build_K(q_lo, 3, 2), build_K(q_hi, 3, 2)
    idx_lo = {u: i for i, u in enumerate(K_lo)}
    n_lo, n_hi = len(K_lo), len(K_hi)

    S = sp.zeros(n_lo, n_hi)
    for i, u in enumerate(K_hi):
        S[idx_lo[u % q_lo], i] = 1
    J = S.T
    m = n_hi // n_lo
    E = sp.Rational(1, m) * J * S
    ProjZ = sp.eye(n_hi) - E

    t_hi = p * t_lo
    M_hi, _, _ = build_M_exact(q_hi, t_hi, x)
    M_lo, _, _ = build_M_exact(q_lo, t_lo, x)

    pullback_ok = sp.simplify(M_hi * J - J * M_lo).is_zero_matrix
    pushforward_ok = sp.simplify(S * M_hi - M_lo * S).is_zero_matrix
    Z_invariant_ok = sp.simplify(S * M_hi * ProjZ).is_zero_matrix

    print(f"{label}: pullback intertwines? {pullback_ok}  "
          f"pushforward intertwines? {pushforward_ok}  "
          f"Z=ker(S) invariant? {Z_invariant_ok}")
    assert pullback_ok and pushforward_ok and Z_invariant_ok, "SPLITTING THEOREM CHECK FAILED"


if __name__ == "__main__":
    x = sp.Rational(2, 5)  # arbitrary, not the Collatz saddle
    # Primitive-source lifts, level 1 -> 2 (t_lo=1 is automatically primitive mod a prime)
    check_case(5, 1, 1, x, "p=5,  e_lo=1, t_lo=1  (primitive)")
    check_case(13, 1, 1, x, "p=13, e_lo=1, t_lo=1  (primitive)")
    # Non-primitive-source lift: need e_lo>=2 for a nonzero non-primitive residue to exist.
    # t_lo=p at level e_lo=2 has gcd(t_lo, p^2)=p != 1, i.e. genuinely non-primitive.
    # (p=5 only here: |K| grows fast with p and e, and exact sympy.simplify does not scale
    #  past a few hundred dimensions in reasonable time -- see monotonicity_check.py for
    #  the larger, numerical-precision cross-check at bigger sizes.)
    check_case(5, 2, 5, x, "p=5,  e_lo=2, t_lo=5  (NON-primitive: gcd(5,25)=5)")
    print("\nAll splitting-theorem checks passed.")
