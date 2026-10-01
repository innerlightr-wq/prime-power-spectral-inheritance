"""
monotonicity_check.py — numerical verification of Corollary 2 / Theorem C's
core formula: rho(L_hi) = max(rho(L_lo), rho(N)) exactly, via a correctly
UNITARY change of basis adapted to the orthogonal splitting W + Z.

(An earlier, now-corrected attempt used a non-orthonormal basis change and
appeared to show singular values NOT matching the union -- that was a basis
artifact, not a refutation; this script does it correctly and documents the
pitfall in a comment, since it is an easy mistake to repeat.)
"""
import numpy as np
from operator_lib import build_K, build_M_numeric


def splitting_test(p, e_lo, t_lo, x, label):
    q_lo, q_hi = p**e_lo, p**(e_lo + 1)
    t_hi = p * t_lo
    K_lo, K_hi = build_K(q_lo, 3, 2), build_K(q_hi, 3, 2)
    idx_lo = {u: i for i, u in enumerate(K_lo)}
    n_lo, n_hi = len(K_lo), len(K_hi)

    M_hi, _, _ = build_M_numeric(q_hi, t_hi, x)
    M_lo, _, _ = build_M_numeric(q_lo, t_lo, x)

    J = np.zeros((n_hi, n_lo))
    for i, u in enumerate(K_hi):
        J[i, idx_lo[u % q_lo]] = 1
    m = n_hi // n_lo
    Jn = J / np.sqrt(m)  # orthonormalize columns -- PITFALL: skipping this breaks the SVD check below

    P_W = Jn @ Jn.conj().T
    P_Z = np.eye(n_hi) - P_W
    Q, R = np.linalg.qr(P_Z)
    diag = np.abs(np.diag(R))
    order = np.argsort(-diag)
    Zbasis = Q[:, order[: n_hi - n_lo]]

    U = np.hstack([Jn, Zbasis])
    assert np.allclose(U.conj().T @ U, np.eye(n_hi), atol=1e-8), "basis change not unitary"

    Mt = U.conj().T @ M_hi @ U
    off1 = np.max(np.abs(Mt[0:n_lo, n_lo:]))
    off2 = np.max(np.abs(Mt[n_lo:, 0:n_lo]))
    N = Mt[n_lo:, n_lo:]

    rho_hi = max(abs(np.linalg.eigvals(M_hi)))
    rho_lo = max(abs(np.linalg.eigvals(M_lo)))
    rho_N = max(abs(np.linalg.eigvals(N))) if N.size else 0.0
    formula_ok = abs(rho_hi - max(rho_lo, rho_N)) < 1e-6

    sv_hi = sorted(np.linalg.svd(M_hi, compute_uv=False), reverse=True)
    sv_union = sorted(list(np.linalg.svd(M_lo, compute_uv=False)) +
                       list(np.linalg.svd(N, compute_uv=False)), reverse=True)
    sv_ok = np.allclose(sv_hi, sv_union, atol=1e-6)

    print(f"{label}:")
    print(f"   off-diagonal blocks: {off1:.2e}, {off2:.2e}  (should be ~0)")
    print(f"   rho(L_hi)={rho_hi:.6f}   max(rho(L_lo),rho(N))={max(rho_lo,rho_N):.6f}   "
          f"formula exact? {formula_ok}")
    print(f"   singular values of L_hi match union of L_lo and N? {sv_ok}")
    assert formula_ok and sv_ok, "MONOTONICITY-FORMULA CHECK FAILED"


if __name__ == "__main__":
    x = 0.4  # arbitrary, not the Collatz saddle -- structural check only
    splitting_test(5, 1, 1, x, "p=5, e_lo=1, t_lo=1 (primitive lift)")
    splitting_test(5, 2, 5, x, "p=5, e_lo=2, t_lo=5 (non-primitive lift)")
    splitting_test(13, 1, 1, x, "p=13, e_lo=1, t_lo=1 (primitive lift)")
    print("\nAll monotonicity-formula checks passed.")
