"""
wieferich_check.py — verifies Proposition (Fermat-quotient <=> order-stall
equivalence) and the two named instances: p=11 (Wieferich base 3) and
p=1093 (Wieferich base 2), including the order-lifting data showing exactly
when hypothesis (H1) holds/fails.
"""


def mult_order(a, q):
    a %= q
    x, k = a, 1
    while x != 1:
        x = (x * a) % q
        k += 1
    return k


def check_wieferich(p, a, label):
    fermat_quotient = pow(a, p - 1, p * p)
    d = mult_order(a, p)
    order_stall = pow(a, d, p * p)
    equivalent = (fermat_quotient == 1) == (order_stall == 1)
    print(f"{label}: {a}^({p}-1) mod {p}^2 = {fermat_quotient}   "
          f"ord_{p}({a})={d}, {a}^{d} mod {p}^2 = {order_stall}   "
          f"both forms agree? {equivalent}   "
          f"=> {'WIEFERICH' if fermat_quotient == 1 else 'not Wieferich'}")
    assert equivalent, "Fermat-quotient and order-stall forms disagree -- Proposition would be false!"
    return fermat_quotient == 1


def order_lifting_table(p, base, levels, label):
    print(f"\n{label}: order-lifting of {base} across levels")
    prev = None
    for e in range(1, levels + 1):
        q = p**e
        r = mult_order(base, q)
        ratio = r / prev if prev else None
        print(f"   e={e} q={q}: ord_q({base})={r}" +
              (f"   ratio to previous level = {ratio:.3f}" if ratio else ""))
        prev = r


if __name__ == "__main__":
    print("=== Wieferich / order-stall equivalence, verified on known examples ===")
    check_wieferich(11, 3, "p=11, a=3")
    check_wieferich(1093, 2, "p=1093, a=2")
    # negative controls: primes NOT Wieferich for the given base
    check_wieferich(13, 3, "p=13, a=3 (control, expect NOT Wieferich)")
    check_wieferich(11, 2, "p=11, a=2 (control, expect NOT Wieferich)")

    order_lifting_table(11, 2, 5, "p=11, base 2 (needed for hypothesis H1)")
    order_lifting_table(11, 3, 5, "p=11, base 3 (NOT needed for H1; stall visible here)")
    order_lifting_table(1093, 2, 2, "p=1093, base 2 (H1 FAILS at e=1->2)")

    print("\nAll Wieferich checks passed.")
