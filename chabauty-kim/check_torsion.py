"""Check the second weight-two digit at the published conductor-3 and -4 exceptions."""


def torsion_digits(p, order, residue):
    """Return (M₂ mod p², ℓ₄ mod p) at the indicated Teichmüller root."""
    modulus = p * p
    root = pow(residue, p, modulus)
    assert root % p != 1 and pow(root, order, modulus) == 1
    powers = [pow(root, j, modulus) for j in range(order)]
    # The derivative of the finite geometric sum gives sum_b b * root^b.
    linear = (p - 1) * root * pow(root - 1, -1, modulus) % modulus
    correction = 2 * p * linear % modulus
    weight_two = weight_four = 0
    for u in range(1, p):
        inv = pow(u, -1, modulus)
        square = inv * inv % modulus
        power = powers[u % order]
        weight_two += power * square * (1 - correction * inv % modulus)
        weight_four += power * (square % p) ** 2
    return weight_two * pow(1 - root, -1, modulus) % modulus, weight_four % p


if __name__ == "__main__":
    for p, order, root, digit, ell4 in (
        (149, 4, 44, 85, 143),
        (241, 4, 64, 103, 105),
        (2946901, 4, 722077, 1795894, 1422053),
        (205129, 3, 81187, 170025, 30238 * (1 - 81187) % 205129),
    ):
        moment, fourth = torsion_digits(p, order, root)
        assert (moment, fourth) == (digit * p, ell4)
        print(f"p={p} order={order} residue={root} M2/p={moment // p} ell4={fourth}")
