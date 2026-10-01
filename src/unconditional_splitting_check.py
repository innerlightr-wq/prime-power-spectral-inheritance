"""
unconditional_splitting_check.py — verifies the UNCONDITIONAL form of the
intertwining/splitting theorems (paper/main.tex, Theorems 'Pullback
intertwining' and 'Splitting'), which hold at EVERY prime-power step with
NO hypothesis on multiplicative-order lifting, by separating the ladder
growth c_e = r_{e+1}/r_e from the fiber size m_e = |K_{e+1}|/|K_e|.

Covers every "Targeted controls" example named in paper/main.tex Sec. 6,
plus the p=1093 sampled-entry check (the full matrix there is far too
large to build -- entries are sampled directly from the definitions).
"""
import numpy as np
from math import gcd
from operator_lib import mult_order, build_K
from independent_reimplementation import L_matrix, order, group


def check_full(p, a, b, e, x, t_lo, label):
    """Full matrix check: intertwining, splitting, eigenvalue-union formula."""
    q_lo, q_hi = p ** e, p ** (e + 1)
    t_hi = p * t_lo
    M_lo, K_lo, pos_lo = L_matrix(q_lo, t_lo, x, a, b)
    M_hi, K_hi, pos_hi = L_matrix(q_hi, t_hi, x, a, b)
    n_lo, n_hi = len(K_lo), len(K_hi)
    r_lo, r_hi = order(b, q_lo), order(b, q_hi)
    c_e = r_hi // r_lo if r_hi % r_lo == 0 else None
    m_e = n_hi // n_lo

    J = np.zeros((n_hi, n_lo))
    for i, u in enumerate(K_hi):
        J[i, pos_lo[u % q_lo]] = 1.0
    S = J.T.copy()
    resid_pull = np.max(np.abs(M_hi @ J - J @ M_lo))
    resid_push = np.max(np.abs(S @ M_hi - M_lo @ S))

    if m_e == 1:
        # degenerate case (paper's remark): J is a permutation matrix, full unitary
        # equivalence, no "new sector" to speak of.
        recon = J @ M_lo @ J.T
        resid_unitary = np.max(np.abs(M_hi - recon))
        print(f"{label}: p={p} (a,b)=({a},{b}) e={e} t_lo={t_lo}  c_e={c_e} m_e={m_e} (TRIVIAL new sector)  "
              f"pull={resid_pull:.2e} push={resid_push:.2e} unitary_equiv_residual={resid_unitary:.2e}")
        assert resid_pull < 1e-9 and resid_push < 1e-9 and resid_unitary < 1e-9
        return

    Jn = J / np.sqrt(m_e)
    P_Z = np.eye(n_hi) - Jn @ Jn.conj().T
    Q, R = np.linalg.qr(P_Z)
    order_idx = np.argsort(-np.abs(np.diag(R)))
    Z = Q[:, order_idx[: n_hi - n_lo]]
    U = np.hstack([Jn, Z])
    Mt = U.conj().T @ M_hi @ U
    offdiag = max(np.max(np.abs(Mt[:n_lo, n_lo:])), np.max(np.abs(Mt[n_lo:, :n_lo])))
    N = Mt[n_lo:, n_lo:]
    rho_hi = max(abs(np.linalg.eigvals(M_hi)))
    rho_lo = max(abs(np.linalg.eigvals(M_lo)))
    rho_N = max(abs(np.linalg.eigvals(N))) if N.size else 0.0
    formula_err = abs(rho_hi - max(rho_lo, rho_N))

    print(f"{label}: p={p} (a,b)=({a},{b}) e={e} t_lo={t_lo}  c_e={c_e} m_e={m_e}  "
          f"pull={resid_pull:.2e} push={resid_push:.2e} offdiag={offdiag:.2e} formula_err={formula_err:.2e}")
    assert resid_pull < 1e-9 and resid_push < 1e-9 and offdiag < 1e-9 and formula_err < 1e-9


def check_p1093_sampled(n_samples=900, seed=0):
    """Entrywise-sampled check for the Collatz pair at p=1093, e=1->2, where the
    full matrix (dimension ~398,000) cannot be built. Samples (source, target)
    pairs directly from the group-walk definitions, per Lemma 'increment ladder'."""
    import random
    random.seed(seed)
    p, a, b = 1093, 3, 2
    q_lo, q_hi = p, p * p
    r_lo, r_hi = mult_order(b, q_lo), mult_order(b, q_hi)
    assert r_hi == r_lo, "expected the base-2 Wieferich stall at this step"
    c_e = r_hi // r_lo
    a_inv_lo, a_inv_hi = pow(a, -1, q_lo), pow(a, -1, q_hi)

    def d0(u, uprime, q, r, a_inv):
        cur = u
        for d in range(1, r + 1):
            cur = (cur * b) % q
            if (cur * a_inv) % q == uprime:
                return d
        return None

    def rand_elt_hi():
        i = random.randint(0, r_hi - 1)
        j = random.randint(0, 50)
        return (pow(b, i, q_hi) * pow(a, j, q_hi)) % q_hi

    mismatches = 0
    for _ in range(n_samples):
        u = rand_elt_hi()
        ubar = u % q_lo
        ubar_prime = rand_elt_hi() % q_lo
        d_coarse = d0(ubar, ubar_prime, q_lo, r_lo, a_inv_lo)
        cur = u
        hits = []
        for d in range(1, r_hi + 1):
            cur = (cur * b) % q_hi
            tgt = (cur * a_inv_hi) % q_hi
            if tgt % q_lo == ubar_prime:
                hits.append(d)
        if d_coarse is None:
            if hits:
                mismatches += 1
        else:
            if len(hits) != c_e or (hits and hits[0] % r_lo != d_coarse % r_lo):
                mismatches += 1
    print(f"p=1093 sampled check: {n_samples} (source, target-fiber) pairs, "
          f"c_e={c_e} (stall confirmed), mismatches={mismatches}")
    assert mismatches == 0


if __name__ == "__main__":
    x = 0.375  # matches the exact-arithmetic audit value (3/8) used in the paper

    print("=== Targeted controls (paper, Section 6) ===")
    check_full(13, 3, 2, 1, x, 1, "generic Collatz")
    check_full(11, 2, 3, 1, x, 1, "role swap (stall, c_e=1,m_e=11)")
    check_full(11, 2, 3, 2, x, 1, "role swap (resumed, primitive)")
    check_full(11, 2, 3, 2, x, 11, "role swap (resumed, non-primitive)")
    b_deep = 7 ** 5
    for e in [1, 2, 3]:
        check_full(5, 2, b_deep, e, x, 1, f"depth-3 control b=7^5 (e={e})")
    check_full(7, 5, 2, 1, x, 1, "multiplier-5 control")
    check_full(5, 7, 18, 1, x, 1, "double stall (trivial new sector)")

    print("\n=== p=1093 sampled-entry check ===")
    check_p1093_sampled()

    print("\nAll unconditional splitting checks passed.")
