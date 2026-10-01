"""
large_sweep_corroboration.py — an independent large-scale sweep of the
intertwining identities, corroborating (not reproducing bit-for-bit) the
scale of the audit described in paper/main.tex Section 6 ("exact
intertwining audit... 3,134 steps... zero mismatches").

HONESTY NOTE: this script's own parameter choices (exactly which (a,b)
pairs and which group-size cutoff) were reconstructed from the paper's
prose description and do NOT reproduce the author's reported counts
exactly -- three reasonable interpretations tried during development gave
totals of 2108, 3212, and 3316 steps (all with zero mismatches), none
exactly 3134. This is most likely a difference in exact boundary
conventions (e.g. whether a,b are required coprime to each other, and
whether the size cutoff applies to the modulus or the group order), not
evidence against the paper's reported figure. This script is included as
ADDITIONAL independent corroboration at a comparable scale, not as a
bit-exact replication of the paper's own count.

Run with: python3 large_sweep_corroboration.py
"""
from math import gcd
import numpy as np
from independent_reimplementation import L_matrix, order, group

PRIMES = [3, 5, 7, 11, 13]
X = 0.375
MAX_GROUP_SIZE = 400


def sweep(require_ab_coprime: bool):
    count = 0
    mismatches = 0
    type_counts = {}
    for p in PRIMES:
        max_e = 3 if p <= 5 else 2
        for a in range(2, 26):
            for b in range(2, 26):
                if a == b:
                    continue
                if require_ab_coprime and gcd(a, b) != 1:
                    continue
                if gcd(p, a * b) != 1:
                    continue
                for e in range(1, max_e + 1):
                    q_lo, q_hi = p ** e, p ** (e + 1)
                    K_hi = group(q_hi, a, b)
                    if len(K_hi) > MAX_GROUP_SIZE:
                        continue
                    K_lo = group(q_lo, a, b)
                    n_lo, n_hi = len(K_lo), len(K_hi)
                    r_lo, r_hi = order(b, q_lo), order(b, q_hi)
                    if r_hi % r_lo != 0:
                        continue
                    c_e, m_e = r_hi // r_lo, n_hi // n_lo

                    t_lo = 1
                    M_lo, _, pos_lo = L_matrix(q_lo, t_lo, X, a, b)
                    M_hi, K_hi2, _ = L_matrix(q_hi, p * t_lo, X, a, b)
                    J = np.zeros((n_hi, n_lo))
                    for i, u in enumerate(K_hi2):
                        J[i, pos_lo[u % q_lo]] = 1.0
                    S = J.T.copy()
                    resid_pull = np.max(np.abs(M_hi @ J - J @ M_lo))
                    resid_push = np.max(np.abs(S @ M_hi - M_lo @ S))

                    count += 1
                    key = (c_e, m_e)
                    type_counts[key] = type_counts.get(key, 0) + 1
                    if resid_pull > 1e-9 or resid_push > 1e-9:
                        mismatches += 1
                        print(f"MISMATCH p={p} a={a} b={b} e={e}: pull={resid_pull} push={resid_push}")
    return count, mismatches, type_counts


if __name__ == "__main__":
    for require_coprime in (False, True):
        count, mismatches, types = sweep(require_coprime)
        oneone = types.get((1, 1), 0)
        onep = sum(v for k, v in types.items() if k == (1, k[1]) and k[1] != 1)
        pp = sum(v for k, v in types.items() if k[0] == k[1] and k[0] != 1)
        assert pp + onep + oneone == count, "categorization must partition the total exactly"
        tag = "gcd(a,b)=1 enforced" if require_coprime else "gcd(a,b)=1 NOT enforced"
        print(f"[{tag}] total={count}  mismatches={mismatches}  "
              f"(p,p)-type={pp}  (1,p)-type={onep}  (1,1)-type={oneone}")
        assert mismatches == 0

    print("\nBoth parameter interpretations: zero mismatches across thousands of steps,")
    print("including every realizable (c_e, m_e) combination identified by Lemma")
    print("'Ladder versus fiber' -- (p,p), (1,p), (1,1) -- and never (p,1), as proved.")
