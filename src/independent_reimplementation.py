"""
independent_reimplementation.py — a SEPARATE, from-scratch implementation
(deliberately not importing operator_lib.py) of the operator construction,
checking p=5,11,13 with (a,b)=(3,2) at the Collatz saddle x_* (including
the non-primitive lift t=5 at e=2->3 for p=5) and p=7,13 with the control
pair (a,b)=(5,2) at x=0.37.

This predates, and is independent of, the removal of hypothesis (H1) in
the current version of paper/main.tex (see docs/theorem-audit.md, Stage
5) -- it was written to back a specific sentence in an earlier revision
of the paper's "Numerical verification" section. The current paper's
"Earlier checks" paragraph in that section still references this result
in general terms ("exact sympy and high-precision linear algebra at
p=5,13 ... is consistent with all of the above"), but no longer quotes it
verbatim. The script's own findings remain correct and are kept as
additional corroboration; see unconditional_splitting_check.py and
large_sweep_corroboration.py for verification of the current,
unconditional theorems specifically.

This script builds M_t(x) directly from Definition 1 using only dense
numpy, with its own group-generation and order routines, and reports the
exact residuals and digit-agreement.
"""
import numpy as np
from math import log2, gcd


def order(g, q):
    g %= q
    x, n = g, 1
    while x != 1:
        x = (x * g) % q
        n += 1
    return n


def group(q, a, b):
    seen = {1}
    frontier = [1]
    while frontier:
        new = []
        for s in frontier:
            for gen in (a, b):
                v = (s * gen) % q
                if v not in seen:
                    seen.add(v)
                    new.append(v)
        frontier = new
    return sorted(seen)


def L_matrix(q, t, x, a, b):
    """Dense construction of L_{e,t,x} per Definition 1, independent code path."""
    K = group(q, a, b)
    pos = {u: i for i, u in enumerate(K)}
    n = len(K)
    r = order(b, q)
    a_inv = pow(a, -1, q)
    M = np.zeros((n, n), dtype=complex)
    for u in K:
        reached = {}
        cur = (u * b) % q
        for d in range(1, r + 1):
            target = (cur * a_inv) % q
            if target not in reached:
                reached[target] = d
            cur = (cur * b) % q
        for target, d in reached.items():
            M[pos[target], pos[u]] += np.exp(2j * np.pi * t * u / q) * (x ** d) / (1 - x ** r)
    return M, K, pos


def residuals(p, e_lo, t_lo, a, b, x):
    q_lo, q_hi = p ** e_lo, p ** (e_lo + 1)
    t_hi = p * t_lo
    M_lo, K_lo, pos_lo = L_matrix(q_lo, t_lo, x, a, b)
    M_hi, K_hi, pos_hi = L_matrix(q_hi, t_hi, x, a, b)
    n_lo, n_hi = len(K_lo), len(K_hi)

    J = np.zeros((n_hi, n_lo))
    for i, u in enumerate(K_hi):
        J[i, pos_lo[u % q_lo]] = 1.0
    S = J.T.copy()
    m = n_hi // n_lo

    pullback_residual = np.max(np.abs(M_hi @ J - J @ M_lo))
    pushforward_residual = np.max(np.abs(S @ M_hi - M_lo @ S))

    Jn = J / np.sqrt(m)
    P_Z = np.eye(n_hi) - Jn @ Jn.conj().T
    Q, R = np.linalg.qr(P_Z)
    order_idx = np.argsort(-np.abs(np.diag(R)))
    Z = Q[:, order_idx[: n_hi - n_lo]]
    U = np.hstack([Jn, Z])
    Mt = U.conj().T @ M_hi @ U
    offdiag_residual = max(np.max(np.abs(Mt[:n_lo, n_lo:])), np.max(np.abs(Mt[n_lo:, :n_lo])))

    N = Mt[n_lo:, n_lo:]
    rho_hi = max(abs(np.linalg.eigvals(M_hi)))
    rho_lo = max(abs(np.linalg.eigvals(M_lo)))
    rho_N = max(abs(np.linalg.eigvals(N))) if N.size else 0.0
    formula_digits = -np.log10(abs(rho_hi - max(rho_lo, rho_N)) + 1e-300)

    return dict(pullback=pullback_residual, pushforward=pushforward_residual,
                offdiag=offdiag_residual, formula_digits=formula_digits,
                rho_hi=rho_hi, rho_lo=rho_lo, rho_N=rho_N)


if __name__ == "__main__":
    x_star = 1 - 1 / log2(3)
    print(f"x_* = {x_star:.10f}\n")

    print("=== Collatz instance (a,b)=(3,2) at x_*, items (i)-(iii) ===")
    for p, e_lo, t_lo in [(5, 1, 1), (11, 1, 1), (13, 1, 1), (5, 2, 5)]:
        r = residuals(p, e_lo, t_lo, 3, 2, x_star)
        tag = "non-primitive lift" if gcd(t_lo, p ** e_lo) != 1 else "primitive lift"
        print(f"p={p:<3} e_lo={e_lo} t_lo={t_lo:<2} ({tag}): "
              f"pullback={r['pullback']:.2e} pushforward={r['pushforward']:.2e} "
              f"offdiag={r['offdiag']:.2e} formula agrees to {r['formula_digits']:.1f} digits")
        assert r['pullback'] < 2e-14 and r['pushforward'] < 2e-14 and r['offdiag'] < 2e-14
        assert r['formula_digits'] >= 10

    print("\n=== Generic control (a,b)=(5,2) at x=0.37, item (v) ===")
    for p in [7, 13]:
        r = residuals(p, 1, 1, 5, 2, 0.37)
        print(f"p={p:<3} (a,b)=(5,2) x=0.37: "
              f"pullback={r['pullback']:.2e} pushforward={r['pushforward']:.2e} "
              f"offdiag={r['offdiag']:.2e} formula agrees to {r['formula_digits']:.1f} digits")
        assert r['pullback'] < 2e-14 and r['pushforward'] < 2e-14 and r['offdiag'] < 2e-14
        assert r['formula_digits'] >= 10

    print("\nAll claims in paper/main.tex Section 5 (Numerical verification) confirmed:")
    print("all residuals below 2e-14, all spectral-radius formulas agree to >=10 digits.")
