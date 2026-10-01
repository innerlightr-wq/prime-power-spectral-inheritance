"""
operator_lib.py — shared construction of the affine-cocycle transfer operator
family L_{e,t,x} (Definition 1 of the paper), for general coprime (a,b) and
prime p, not only the Collatz instance (a,b)=(3,2).

Used by all other scripts in this directory.
"""
import sympy as sp
import numpy as np


def mult_order(g, q):
    """Multiplicative order of g mod q."""
    g %= q
    x, k = g, 1
    while x != 1:
        x = (x * g) % q
        k += 1
    return k


def build_K(q, a, b):
    """K = <a,b> as a subgroup of (Z/qZ)^x, returned as a sorted list."""
    S = {1}
    frontier = [1]
    while frontier:
        nf = []
        for s in frontier:
            for g in (a, b):
                v = (s * g) % q
                if v not in S:
                    S.add(v)
                    nf.append(v)
        frontier = nf
    return sorted(S)


def build_M_exact(q, t, x, a=3, b=2):
    """
    Exact (sympy) construction of M_{t}(x) on K = <a,b> mod q, following
    Definition 1: (M_t(x))_{u',u} = e_q(t u) x^{d0(u,u')} / (1 - x^r),
    r = ord_q(b), d0(u,u') = least d in [1,r] with u' = u * b^d * a^{-1} mod q.
    """
    K = build_K(q, a, b)
    idx = {u: i for i, u in enumerate(K)}
    n = len(K)
    r = mult_order(b, q)
    inv_a = pow(a, -1, q)
    M = sp.zeros(n, n)
    powb = [pow(b, d, q) for d in range(r + 1)]
    for u in K:
        seen = {}
        for d in range(1, r + 1):
            up = (u * powb[d] * inv_a) % q
            if up not in seen:
                seen[up] = d
        for up, d in seen.items():
            M[idx[up], idx[u]] += sp.exp(2 * sp.pi * sp.I * t * u / q) * x**d / (1 - x**r)
    return M, K, idx


def build_M_numeric(q, t, x, a=3, b=2):
    """Same construction, numpy/complex128, for speed on larger cases."""
    K = build_K(q, a, b)
    idx = {u: i for i, u in enumerate(K)}
    n = len(K)
    r = mult_order(b, q)
    inv_a = pow(a, -1, q)
    M = np.zeros((n, n), dtype=complex)
    powb = [pow(b, d, q) for d in range(r + 1)]
    for u in K:
        seen = {}
        for d in range(1, r + 1):
            up = (u * powb[d] * inv_a) % q
            if up not in seen:
                seen[up] = d
        for up, d in seen.items():
            M[idx[up], idx[u]] += np.exp(2j * np.pi * t * u / q) * (x**d) / (1 - x**r)
    return M, K, idx
